from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
import traceback


_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_FRONTEND_DIR = os.path.join(_ROOT, "frontend")
_FRONTEND_INDEX = os.path.join(_FRONTEND_DIR, "index.html")

# Import the custom MCP Orchestrator that replaces Claude Desktop's backend
from agent_mcp import run_agent_loop

# Initialize the FastAPI backend application
app = FastAPI(
    title="DeckGenius AI - Auto-PPT Full-Stack API",
    description="A custom backend that routes prompt requests to the Groq LLM & MCP Python servers.",
    version="1.0.0"
)

# Serve the frontend over HTTP to avoid `file://` browser restrictions.
# Open http://localhost:<port>/ instead of double-clicking the HTML file.
if os.path.isdir(_FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=_FRONTEND_DIR), name="frontend")


@app.get("/")
async def root():
    if os.path.isfile(_FRONTEND_INDEX):
        return FileResponse(_FRONTEND_INDEX)
    return {"status": "ok", "message": "Frontend not found. See /docs."}

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
        # Catch and return any errors (e.g. API limits, connection failures).
        # Note: AnyIO can wrap the real exception into an ExceptionGroup with the generic
        # message "unhandled errors in a TaskGroup", so we unwrap it for a useful response.

        def _flatten_exceptions(exc: BaseException):
            try:
                is_group = isinstance(exc, BaseExceptionGroup)  # type: ignore[name-defined]
            except NameError:
                is_group = False

            if is_group:
                for sub in exc.exceptions:  # type: ignore[attr-defined]
                    yield from _flatten_exceptions(sub)
            else:
                yield exc

        flattened = list(_flatten_exceptions(e))
        if flattened and (len(flattened) > 1 or flattened[0] is not e):
            details = " | ".join(f"{type(sub).__name__}: {sub}" for sub in flattened[:3])
            message = f"{type(e).__name__}: {e} (details: {details})"
        else:
            message = f"{type(e).__name__}: {e}"

        # Log full traceback to server console for local debugging.
        traceback.print_exc()
        return {"status": "error", "message": message}

if __name__ == "__main__":
    import uvicorn
    # Start the Uvicorn ASGI server hosting the FastAPI application
    # Note: reload spawns a reloader process; on Windows this can interfere with
    # stdio-based MCP subprocess task groups and surface as ClosedResourceError.
    port = int(os.getenv("DOPPT_PORT", "8000"))
    uvicorn.run("main:app", host="localhost", port=port, reload=False)