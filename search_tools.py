from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from typing import List, Any

@tool("DuckDuckGoSearch")
def search(search_query: str) -> str:
    """Search the web for information using DuckDuckGo.
    
    Args:
        search_query: The search query string
    
    Returns:
        str: Search results from DuckDuckGo
    """
    try:
        search_tool = DuckDuckGoSearchRun()
        return search_tool.run(search_query)
    except Exception as e:
        return f"Search failed: {str(e)}"

def create_search_tools() -> List[Any]:
    """Create and return a list of search tools."""
    return [search]
