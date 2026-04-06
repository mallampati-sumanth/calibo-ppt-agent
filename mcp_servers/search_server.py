"""
DeckGenius AI - Search MCP Server
Module: search_server.py

Description:
Provides live web search capabilities to the Groq LLM via the Model Context Protocol (MCP).
This server uses DuckDuckGo (via the `duckduckgo_search` library) to fetch real-time
information, ensuring the generated presentations contain accurate and up-to-date facts.
"""

from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS
import json

# Initialize the FastMCP server instance specifically for web search operations
mcp = FastMCP("WebSearchServer")

class WebSearchFetcher:
    """
    WebSearchFetcher: A utility class to encapsulate the DuckDuckGo search logic.
    Provides robust error handling and fallback mechanisms to ensure the LLM
    receives actionable data even if the network request fails.
    """
    
    @staticmethod
    def get_summary(query: str) -> str:
        """
        Executes a DuckDuckGo text search for the given query.
        
        Args:
            query (str): The search term provided by the LLM.
            
        Returns:
            str: A combined string of the top 3 search result snippets.
        """
        try:
            # Context manager ensures the DDGS session is closed properly
            with DDGS() as ddgs:
                # Fetch top 3 results for broad context
                results = list(ddgs.text(query, max_results=3))
                
                # Handle cases where search yields no results
                if not results:
                    return f"Could not find extensive data for '{query}'. Please generate plausible educational assumptions."
                
                # Extract the 'body' (snippet) from each search result and combine them
                combined_extracts = "\n".join([f"- {r.get('body', '')}" for r in results])
                return combined_extracts
                
        except Exception as e:
            # Fallback mechanism: If the search fails (e.g., network error, rate limit),
            # instruct the LLM to gracefully hallucinate or use its internal knowledge base.
            return f"Search service unavailable for '{query}'. Please generate plausible content using your internal knowledge. Error: {e}"

# Instantiate the fetcher
fetcher = WebSearchFetcher()

@mcp.tool()
def search_topic(query: str) -> str:
    """
    MCP Tool: search_topic
    Description: Search the live web via DuckDuckGo for factual data about a topic to use in a presentation.
    
    Args:
        query (str): The topic or question to research.
        
    Returns:
        str: Real-time search excerpts.
    """
    return fetcher.get_summary(query)

if __name__ == "__main__":
    # Start the MCP server using robust standard input/output streams.
    # The custom robust runner ensures empty lines/newlines over stdout don't break JSON-RPC parsing.
    from mcp_stdio_robust import run_fastmcp_with_robust_stdio
    run_fastmcp_with_robust_stdio(mcp)

