# ?? DoPPT: The Autonomous AI Presentation Agent

![DoPPT Banner](https://img.shields.io/badge/DoPPT-AI%20Agent-8A2BE2?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203-f37b1d?style=for-the-badge)
![MCP](https://img.shields.io/badge/Architecture-MCP-blue?style=for-the-badge)

**DoPPT** is a full-stack, AI-powered presentation generation agent. It utilizes a custom **Model Context Protocol (MCP)** router to seamlessly integrate web searching, data synthesis, and PowerPoint formatting into a single, ChatGPT-style web interface.

---

## ?? Features

- **?? ChatGPT-Style UI:** A premium, glassmorphism-inspired chat interface for interacting with the agent.
- **?? Groq-Powered Intelligence:** Runs on the lightning-fast llama-3.3-70b-versatile model.
- **?? Real-Time Web Search:** Uses DuckDuckGo to research up-to-date information before drafting slides.
- **?? Automated PPTX Creation:** Generates fully styled .pptx files with titles, content, and structured bullet points.
- **??? Custom MCP Orchestrator:** Implements a native Python MCP Client to route tool calls to standalone server processes.

---

## ??? Architecture & How It Works

The project follows a modular, agentic architecture. 

`	ext
[ Frontend UI ] <--> [ FastAPI Backend ]
                            |
                    [ Groq LLM (Brain) ]
                            |
                 [ Custom MCP Orchestrator ]
                           /                      [ Web Search Tool ]    [ PPT Generator Tool ]
              (DuckDuckGo)            (python-pptx)
`

1. **The Request:** The user types a prompt into the modern web UI.
2. **The Brain:** The FastAPI backend forwards this to the Groq LLM.
3. **The Tools:** If the LLM needs information, it tells the MCP Orchestrator to trigger the Web Search server.
4. **The Assembly:** Once the research is complete, the LLM triggers the PPT Generator server, which builds the actual .pptx file.
5. **The Delivery:** The path to the downloaded presentation is returned to the user in the chat UI.

---

## ?? Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- A Groq API Key

### 2. Installation
`ash
git clone https://github.com/your-repo/DoPPT.git
cd DoPPT
pip install -r requirements.txt
`

### 3. Add Your API Key
Open ackend/agent_mcp.py and replace the placeholder API key with your actual Groq key:
`python
GROK_API_KEY = "your_groq_api_key_here"
`

### 4. Run the Servers
`ash
python backend/main.py
`
Once running, open your browser and navigate to: http://localhost:8000

---

## ?? Project Structure

- rontend/index.html: The premium chat interface.
- ackend/main.py: The FastAPI application.
- ackend/agent_mcp.py: The core LLM and MCP routing logic.
- mcp_servers/search_server.py: The DuckDuckGo search integration.
- mcp_servers/ppt_server.py: The presentation generation engine using python-pptx.
- generated_presentations/: Output directory for the .pptx files.
