<div align="center">
  <h1>🪄 Auto-PPT Agent (DoPPT)</h1>
  <p><em>An Enterprise-Grade, Autonomous Model Context Protocol (MCP) Ecosystem</em></p>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Architecture-100%25%20Modular%20OOP-blue?style=for-the-badge" alt="Architecture" />
  <img src="https://img.shields.io/badge/Client-DoPPT%20Web%20UI-purple?style=for-the-badge" alt="Client" />
  <img src="https://img.shields.io/badge/Brain-Groq%20LLM-orange?style=for-the-badge" alt="Brain" />
</div>

<br>

## 🎥 Video Demonstration
Watch the agent autonomously research and generate a `.pptx` presentation in real-time, executing tools via MCP with no manual slide editing.
**[▶️ Click here to watch the full demo](https://drive.google.com/file/d/1eZVDDowfdvjuLnUFUZeoNPfBx6CZ1Sqb/view?usp=sharing)**

<br>

**Welcome to my Auto-PPT Agent ecosystem.**
I engineered this project as a clean, decentralized architecture where the **LLM Brain** never touches the filesystem directly.
Instead, it executes a strict **MCP toolchain** ("The Eyes" + "The Hands") to ground content in real data and write a `.pptx` safely to disk.

---

## 🌟 The Core Idea (How It Works in the Current Version)

**Your Prompt (from the DoPPT Web UI):**
*"Create a 6-slide presentation about Team Collaboration. Use live research, include a two-column comparison slide, and add an image placeholder slide."*

```text
                            ↓ [DoPPT Web UI]
      (served by FastAPI at /  — source is frontend/index.html)
                            ↓ [FastAPI Backend]
                  (backend/main.py — /api/generate)
                            ↓ [backend/agent_mcp.py]
            (Groq Llama 3.3 Brain + MCP Router / Tool Dispatcher)
                            ↓ [FastMCP + Robust Stdio Shield]
             (mcp_servers/mcp_stdio_robust.py — The Shield)
                            ↓
            ┌──────────────────────────────────────────────┐
            │           PARALLEL TOOL EXECUTION            │
            ├──────────────────┐        ┌──────────────────┤
 [mcp_servers/search_server.py]│        │[mcp_servers/ppt_server.py]
           (The Eyes)          │        │       (The Hands)
     DuckDuckGo live search ◄──┘        └──► python-pptx writes slides
            └──────────────────────────────────────────────┘
                            ↓
        [Output: generated_presentations/<your_file>.pptx saved locally]
```

---

## 💎 What Makes My Project Special?

1. **🧠 Grounded Content by Design:** In the DoPPT web stack, `mcp_servers/search_server.py` uses DuckDuckGo excerpts so the Brain can pull real-world context before writing slides.
2. **🛡️ The Custom Stdio Shield (Windows-Proof):** `mcp_servers/mcp_stdio_robust.py` filters whitespace-only stdin lines that can crash JSON-RPC parsing on Windows pipes.
3. **🏗️ Absolute Modularity (OOP):** The slide generator uses a strict `PPTManager` class (no messy global pipelines), and always saves output into `generated_presentations/`.
4. **📦 Two Run Modes:**
   - **DoPPT Web UI mode (current default):** `frontend/` + `backend/` + `mcp_servers/`.
   - **Standalone MCP demo mode:** legacy root scripts (`ppt_server.py`, `search_server.py`) are kept as a professor-friendly reference implementation.

5. **🎨 Better PPT Styling by Default:** The PPT tool server applies consistent background + accent + typography so decks look "designed" even without a template.
6. **🧩 Template Support (True Themes):** If you provide a `.pptx` template path, the agent can create the deck from it to inherit real PowerPoint themes.
7. **🖼️ Image Support (Local Files):** If you provide a local image path, the agent can place it on a slide.

---

## 🗺️ System Architecture (Current)

```mermaid
graph TD
    classDef ui fill:#A8C6FA,stroke:#333,stroke-width:2px,color:#000;
    classDef brain fill:#FDBA74,stroke:#333,stroke-width:2px,color:#000;
    classDef shield fill:#FDE047,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5,color:#000;
    classDef server fill:#86EFAC,stroke:#333,stroke-width:2px,color:#000;
    classDef external fill:#FCA5A5,stroke:#333,stroke-width:2px,color:#000;

    UI[DoPPT Web UI<br/>frontend/index.html]:::ui --> API[FastAPI<br/>backend/main.py]:::ui
    API --> Brain[Groq LLM Brain<br/>backend/agent_mcp.py]:::brain
    Brain --> Shield[mcp_stdio_robust.py<br/>The Shield]:::shield
    Shield --> Router{FastMCP Tool Router}

    Router -->|WebSearchServer| Search[mcp_servers/search_server.py<br/>The Eyes]:::server
    Search --> DDG[(DuckDuckGo Search)]:::external

    Router -->|PPTOperations| PPT[mcp_servers/ppt_server.py<br/>The Hands]:::server
    PPT --> Disk[(generated_presentations/*.pptx)]:::external
```

---

## 📁 Project Structure (Current)

```text
ppt_agent/
│
├── README.md
├── requirements.txt
├── setup.py
├── .env                         # local secrets (gitignored)
│
├── frontend/
│   └── index.html               # DoPPT ChatGPT-style UI
│
├── backend/
│   ├── main.py                  # FastAPI API server (/api/generate)
│   └── agent_mcp.py             # Groq Brain + MCP stdio orchestration
│
├── mcp_servers/
│   ├── mcp_stdio_robust.py       # The Shield (robust JSON-RPC stdio)
│   ├── search_server.py          # The Eyes (DuckDuckGo excerpts)
│   └── ppt_server.py             # The Hands (python-pptx slide writer)
│
└── generated_presentations/      # Output .pptx files land here
```

---

## 🚀 Setup (Current Web UI Version)

### Step 1: Install

```powershell
python setup.py
```

### Step 2: Add Your Groq Key

Create/edit `.env` at project root:

```bash
GROQ_API_KEY=your_key_here
```

### Step 3: Run

Terminal 1 (backend):

```powershell
# Recommended on Windows if port 8000 is busy:
$env:DOPPT_PORT=8001
python backend/main.py
```

Then open the web UI:

- http://localhost:8001/

Important: do NOT open the HTML using `file://...` (double-click). Browsers block `fetch()` from `file://` to `http://localhost`.

If you really want to open the HTML file directly, pass an API override:

- `frontend/index.html?api=http://localhost:8001`

---

## 🎨 PPT Styling, Templates, and Images

### Default Styling (No Template)
The slide tools apply a light design system (background + accent bar + typography) automatically.

### True Themes (Recommended)
Create a PowerPoint template `.pptx` in Microsoft PowerPoint and pass its path.
The agent can call `create_presentation_from_template(filename, template_path)` to inherit master slides, fonts, and colors.

### Images
If you provide a local image file path, the agent can place it using `add_image_slide_from_path(filename, title, image_path, caption)`.

---



<div align="center">
  <p><em>Architected and engineered for stable, tool-driven execution.</em></p>
</div>
