<div align="center">
  <h1>✨ DoPPT (Full-Stack Auto-PPT Creator)</h1>
  <p><em>An Enterprise-Grade, Autonomous Model Context Protocol (MCP) Ecosystem</em></p>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Architecture-Full--Stack%20%2F%20OOP-blue?style=for-the-badge" alt="Architecture" />
  <img src="https://img.shields.io/badge/AI%20Engine-Groq%20Llama%203.3-purple?style=for-the-badge" alt="Engine" />
  <img src="https://img.shields.io/badge/Search-DuckDuckGo-brightgreen?style=for-the-badge" alt="Search" />
</div>

<br>

## 🎥 Video Demonstration
Watch DoPPT autonomously research and generate a .pptx presentation in real-time, executing its tools natively without relying on 3rd-party desktop clients!
**[▶️ Click here to watch the full demo](https://drive.google.com/file/d/1eZVDDowfdvjuLnUFUZeoNPfBx6CZ1Sqb/view?usp=sharing)**

<br>

**Welcome to the DoPPT ecosystem.** 
While standard MCP implementations rely heavily on the Anthropic/Claude Desktop App, I deliberately engineered a completely custom, full-stack architecture that implements the **Model Context Protocol (MCP)** natively. 

I architected this project from the ground up to demonstrate mastery of asynchronous Python APIs, custom UI development, and programmatic LLM tool orchestration.

---

## 🌟 The Core Idea (How I Built It Better)

**Your Prompt:** *"Create a 5-slide presentation on Artificial Intelligence trends."*

`	ext
                            ↓ [DoPPT Web UI (index.html)]
              (Captures user intent with a sleek ChatGPT-style interface)
                            ↓ [FastAPI Backend (main.py)]
                (Routes the HTTP request securely to the Python Agent)
                            ↓ [Native Orchestrator (agent_mcp.py)]
            ┌──────────────────────────────────────────────┐
            │           PARALLEL TOOL EXECUTION            │
            ├───────────────┐              ┌───────────────┤
  [search_server.py]        │              │  [ppt_server.py]
      (The Eyes)            │              │    (The Hands)
 Fetches DuckDuckGo data ◄──┘              └──► Boots PPTManager, 
   to eliminate AI                               formats slides,
    hallucination.                                writes to disk.
            └──────────────────────────────────────────────┘
                            ↓ 
           [Output: generated_presentations/my_slides.pptx saved securely!]
`

---

## 💎 What Makes My Project Special?

1. **🧠 Independent LLM Brain:** I bypassed Claude entirely, routing the intelligence through **Groq's Llama 3.3-70b**. It's incredibly fast and fully capable of parsing JSON-RPC tool schemas natively.
2. **🌐 Live Web Search Integration:** Replaced basic REST APIs with the duckduckgo-search library, giving the agent real-time access to the live internet to ensure strict factual accuracy.
3. **💻 Custom Premium Frontend:** Built a beautiful, responsive HTML/JS UI acting as the primary prompt engine, modeled in a clean **ChatGPT-style format**.
4. **⚙️ Native MCP Orchestration:** Used mcp.client.stdio natively. The Python backend programmatically establishes standard I/O byte streams matching directly with the local Python tool servers, removing the need for external desktop apps.
5. **🏗️ Absolute Modularity (OOP):** I banned global variables entirely inside the tool servers. My servers are wrapped in strict classes (PPTManager and WebSearchFetcher) with explicitly managed memory states and absolute file pathing.

---

## 🗺️ System Architecture

My architecture completely decouples the **Frontend UI**, the **LLM Brain**, and the **Filesystem Hands**.

`mermaid
graph TD
    classDef ui fill:#A8C6FA,stroke:#333,stroke-width:2px,color:#000;
    classDef api fill:#FDE047,stroke:#333,stroke-width:2px,color:#000;
    classDef server fill:#86EFAC,stroke:#333,stroke-width:2px,color:#000;
    classDef external fill:#FCA5A5,stroke:#333,stroke-width:2px,color:#000;

    UI[UI: index.html]:::ui -- POST /api/generate --> Backend(FastAPI: main.py):::api
    Backend -- Initiates workflow --> Orchestrator{agent_mcp.py<br/>MCP Loop}
    
    Orchestrator -- Prompt + Tools --> Groq[(Groq Llama 3.3 API)]:::external
    
    Orchestrator -->|WebSearchServer| Search[search_server.py<br/>The Eyes]:::server
    Search -- Fetches Real Data --> DDG[(DuckDuckGo)]:::external
    
    Orchestrator -->|PPTOperations| PPT[ppt_server.py<br/>The Hands]:::server
    PPT -- Generates Slides --> Disk[(Local .pptx Files)]:::external
`

---

## 📁 Project Structure

`	ext
ppt_agent/
│
├── README.md                      # Architectural case study (you are here)
├── requirements.txt               # Locked dependencies and libraries
│
├── frontend/
│   └── index.html                 # The beautiful ChatGPT-style UI
├── backend/
│   ├── main.py                    # The FastAPI web server
│   └── agent_mcp.py               # The core MCP orchestrator hooking to Groq
│
├── mcp_servers/
│   ├── ppt_server.py              # The Hands (PowerPoint Generator)
│   └── search_server.py           # The Eyes (DuckDuckGo Fact-Checker)
│
└── generated_presentations/       # Secure absolute-path output folder
`

---

## 🚀 Setup Complete in 3 Steps

**Prerequisites:** Python 3.10+

### Step 1: Install Dependencies
Open your terminal and install the required native dependencies:

`ash
pip install fastapi uvicorn pydantic mcp duckduckgo-search python-pptx openai
`

### Step 2: Start the Backend Server
Navigate to the ackend directory and start the FastAPI Uvicorn server.
*(Ensure your Groq API key is set inside ackend/agent_mcp.py!)*

`ash
cd backend
python -m uvicorn main:app
`
*(Ensure it runs on port 8000)*

### Step 3: Launch the UI & Generate
Simply open rontend/index.html in your favorite web browser. 

Type your request in the beautifully styled chat box:
> *"Create a 5-slide presentation on Artificial Intelligence trends."*

Sit back and watch DoPPT orchestrate the research, slide generation, and formatting completely autonomously!

---

## 👨‍💻 Development & Code Quality

*   **Error Handling:** Every single tool is wrapped in strict 	ry/except bounds. If a network request fails or formatting drops, it catches the error and returns a dynamic fallback string to the LLM (e.g., instructing it to use internal knowledge) rather than crashing the agent.
*   **Documentation:** Every .py file contains comprehensive, professional architectural docstrings outlining *why* it was engineered that way, alongside line-by-line intent inline comments.

**This ecosystem isn't just a script; it's a fully operational, decentralized full-stack AI platform.**

<div align="center">
  <p><em>Architected and Engineered meticulously for perfect execution metrics.</em></p>
</div>