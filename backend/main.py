from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio

# Import the custom MCP Orchestrator that replaces Claude Desktop's backend
from agent_mcp import run_agent_loop

# Initialize the FastAPI backend application
app = FastAPI(
    title="DeckGenius AI - Auto-PPT Full-Stack API",
    description="A custom backend that routes prompt requests to the Groq LLM & MCP Python servers.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the frontend (index.html) running on a different port/protocol 
# to communicate with this backend securely without browser security blocks.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for local development)
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

class PromptRequest(BaseModel):
    """
    Pydantic schema for defining the incoming JSON payload from the frontend.
    Expected format: {"prompt": "Create a presentation about Space"}
    """
    prompt: str

@app.post("/api/generate")
async def generate_presentation(request: PromptRequest):
    """
    API Endpoint: POST /api/generate
    
    Workflow:
    1. Receives the user's prompt string from the React/HTML frontend.
    2. Invokes the native MCP agent loop (`run_agent_loop`), passing the prompt.
    3. The agent loop coordinates the Groq LLM and physical python MCP servers.
    4. Returns the final LLM summary upon success or an error message on failure.
    """
    try:
        # Trigger the core LLM tool-calling orchestration loop
        result_message = await run_agent_loop(request.prompt)
        
        # Return the success payload to the frontend
        return {"status": "success", "message": result_message}
    except Exception as e:
        # Catch and return any errors (e.g. API limits, connection failures)
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Start the Uvicorn ASGI server hosting the FastAPI application
    # reload=True automatically restarts the server if main.py is edited
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)