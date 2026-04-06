import sys
import os
import json
import asyncio
from openai import AsyncOpenAI
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

"""
DECKGENIUS AI ORCHESTRATOR
--------------------------
This script acts as the "Brain" of the operation. It replaces the Claude Desktop 
C++ backend completely. It uses the Groq API (running Llama 3.3) as its intelligence 
and natively spawns standard I/O (stdio) Python processes for the MCP tool servers.
"""

# ?? Authentication Layer
# The user provided a Groq API key to power the Llama 3.3 inference engine natively.
GROK_API_KEY = "your_groq_api_key_here"

# ?? Base Client Configuration
# We instantiate the OpenAI Python SDK but instruct it to hit Groq's custom OpenAI-compatible endpoint.
# This lets us seamlessly use the `tools` calling schema natively.
client = AsyncOpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# ?? Resource Paths
# Compute the absolute paths to the MCP python scripts physically existing in the `mcp_servers` directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(backend_dir)
ppt_server_path = os.path.join(parent_dir, "mcp_servers", "ppt_server.py")
search_server_path = os.path.join(parent_dir, "mcp_servers", "search_server.py")

async def run_agent_loop(prompt: str):
    """
    Core Execution Loop:
    Takes natural language string as input, sets up MCP connections, starts an infinite `while True`
    loop, and coordinates Groq's tool execution requests asynchronously.
    """
    print(f"User Prompt Received: {prompt}")

    # STEP 1: Process Definition
    # Configure StdioServerParameters to launch python passing the script files as arguments
    ppt_params = StdioServerParameters(command=sys.executable, args=[ppt_server_path])
    search_params = StdioServerParameters(command=sys.executable, args=[search_server_path])

    # STEP 2: Connection Initialization
    # Open streaming pipes directly to those independent python subprocesses. 
    # Use context managers to ensure everything closes successfully at the end.
    async with stdio_client(ppt_params) as (ppt_read, ppt_write), \
               stdio_client(search_params) as (search_read, search_write):
               
        # Establish Model Context Protocol logical sessions over the raw byte streams
        async with ClientSession(ppt_read, ppt_write) as ppt_session, \
                   ClientSession(search_read, search_write) as search_session:
            
            # Formally send the MCP `initialize` handshake protocol request
            await ppt_session.initialize()
            await search_session.initialize()

            # STEP 3: Capability Discovery
            # Query each server for their registered capabilities (tools)
            ppt_tools_result = await ppt_session.list_tools()
            search_tools_result = await search_session.list_tools()
            
            # Map tools to the OpenAI/Groq JSON schema format
            tools = []
            tool_map = {}
            
            # Map PPT tools (e.g. `create_presentation`, `add_slide_with_title_and_bullets`)
            for tool in ppt_tools_result.tools:
                tool_map[tool.name] = ppt_session
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
                
            # Map Search tools (e.g. `search_topic` powered by DuckDuckGo)
            for tool in search_tools_result.tools:
                tool_map[tool.name] = search_session
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })

            # Define System Instructions & Agent Rules
            messages = [
                {
                    "role": "system", 
                    "content": (
                        "You are the Auto-PPT Agent. "
                        "Step 1: Plan slide titles based on the user's topic. "
                        "Step 2: ALWAYS execute 'create_presentation' first with a filename like 'my_slides.pptx'. "
                        "Step 3: Call 'add_slide_with_title_and_bullets' sequentially for each slide. "
                        "You may use 'search_topic' for real data if needed, or hallucinate gracefully. "
                        "Provide exactly 3-5 bullet points per slide."
                    )
                },
                {"role": "user", "content": prompt}
            ]

            print("Starting True Agentic Loop with Tool Execution...")
            
            # STEP 4: The Agentic Control Loop
            while True:
                # Dispatch completion task to Groq LLM passing conversation state and available MCP tools
                response = await client.chat.completions.create(
                    model="llama-3.3-70b-versatile", # State of the art Llama 3 running on fast Groq silicon
                    messages=messages,
                    tools=tools, # Injected dynamically via MCP list_tools()
                    tool_choice="auto",
                    temperature=0.5
                )

                response_message = response.choices[0].message
                
                # Append Groq's reply into the ongoing conversation history appropriately
                message_to_append = {
                    "role": response_message.role,
                    "content": response_message.content or "",
                }
                
                # If Groq elected to call a tool, parse it into the schema history constraint
                if response_message.tool_calls:
                    message_to_append["tool_calls"] = [
                        {
                            "id": t.id,
                            "type": t.type,
                            "function": {
                                "name": t.function.name,
                                "arguments": t.function.arguments
                            }
                        } for t in response_message.tool_calls
                    ]
                messages.append(message_to_append)

                # Base Case: Break out of the loop when the LLM deems all tool actions completed
                if not response_message.tool_calls:
                    break

                # STEP 5: Tool Translation & Execution
                # Execute the actual tools the LLM requested locally
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    print(f"??? LLM Executing Tool: {tool_name}")
                    
                    # Decrypt LLM parameter strings into JSON objects
                    args = json.loads(tool_call.function.arguments)
                    
                    # Verify the tool actually exists in memory routing layer
                    if tool_name in tool_map:
                        session = tool_map[tool_name]
                        # Dispatch the tool via MCP native call_tool over the subprocess pipe
                        result = await session.call_tool(tool_name, arguments=args)
                        
                        # Extract the physical output text generated by the Python server script execution
                        result_text = "\n".join([c.text for c in result.content if c.type == "text"])
                        print(f"   ? Result: {result_text}")
                        
                        # Feedback Loop: Tell Groq that the tool succeeded or failed so it can proceed
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_name,
                            "content": result_text
                        })
                    else:
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_name,
                            "content": "Error: Tool not found."
                        })

            # STEP 6: Conclusion
            # Provide the user with the ultimate summary generated by Groq
            return messages[-1]["content"] if messages[-1]["content"] else "Finished successfully."


