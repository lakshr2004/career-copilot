import os
import asyncio
import platform
import logging
import requests
from dotenv import load_dotenv
from guards import log_audit

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("github_mcp")

def fetch_via_http(username: str) -> list:
    """
    Fallback method to fetch public repositories directly via public GitHub API.
    """
    logger.info(f"Using HTTP fallback to fetch public repos for user: {username}")
    url = f"https://api.github.com/users/{username}/repos?per_page=30&sort=updated"
    headers = {
        "User-Agent": "CareerCopilot-AI/1.0"
    }
    
    # Optional authentication if token exists
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            repos = response.json()
            parsed_repos = []
            for repo in repos:
                parsed_repos.append({
                    "name": repo.get("name"),
                    "description": repo.get("description") or "",
                    "language": repo.get("language") or "Unknown",
                    "stars": repo.get("stargazers_count", 0),
                    "url": repo.get("html_url")
                })
            log_audit("github_fetch", "SUCCESS", {"username": username, "method": "HTTP", "count": len(parsed_repos)})
            return parsed_repos
        else:
            logger.error(f"GitHub HTTP API error {response.status_code}: {response.text}")
            log_audit("github_fetch", "ERROR", {"username": username, "method": "HTTP", "status_code": response.status_code})
            return []
    except Exception as e:
        logger.error(f"GitHub HTTP API exception: {e}")
        log_audit("github_fetch", "EXCEPTION", {"username": username, "method": "HTTP", "error": str(e)})
        return []

async def fetch_via_mcp(username: str) -> list:
    """
    Connects to the official GitHub MCP server via stdio and retrieves repositories.
    """
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        logger.info("GitHub token not found. Skipping MCP and using HTTP.")
        return []
        
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from contextlib import AsyncExitStack

    # Windows command configuration
    is_windows = platform.system() == "Windows"
    command = "npx.cmd" if is_windows else "npx"
    args = ["-y", "@modelcontextprotocol/server-github"]
    
    env = os.environ.copy()
    env["GITHUB_PERSONAL_ACCESS_TOKEN"] = token
    env["GITHUB_TOKEN"] = token

    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=env
    )

    logger.info(f"Connecting to GitHub MCP server for user: {username}...")
    try:
        async with AsyncExitStack() as stack:
            # Connect via stdio transport
            transport = await stack.enter_async_context(stdio_client(server_params))
            session = await stack.enter_async_context(ClientSession(transport[0], transport[1]))
            
            # Initialize connection
            await session.initialize()
            
            # Search for tools
            tools_response = await session.list_tools()
            tools = [t.name for t in tools_response.tools]
            logger.info(f"Connected to MCP Server. Available tools: {tools}")
            
            # Look for list_repositories or search_repositories or search_code
            # The official server has search_repositories and get_file_contents, and search_code.
            # Let's check which repo listing tool is available
            target_tool = None
            if "search_repositories" in tools:
                target_tool = "search_repositories"
            elif "list_repositories" in tools:
                target_tool = "list_repositories"
                
            if not target_tool:
                logger.warning("No repository listing tool found in GitHub MCP server. Falling back.")
                return []
                
            if target_tool == "search_repositories":
                # Search repositories for user
                query = f"user:{username}"
                result = await session.call_tool("search_repositories", arguments={"query": query})
            else:
                # list_repositories
                result = await session.call_tool("list_repositories", arguments={"username": username})
            
            # Parse response
            # Typically result.content contains text
            content_text = ""
            if result and hasattr(result, "content"):
                for content in result.content:
                    if hasattr(content, "text"):
                        content_text += content.text
            
            # Since content is textual/markdown JSON, we will parse or extract repositories
            # Let's do a simple fallback if parsing fails, or parse JSON if formatted as such
            logger.info("Successfully fetched data via MCP client.")
            log_audit("github_fetch", "SUCCESS", {"username": username, "method": "MCP"})
            
            # We can parse the text or simply forward it as raw GitHub text summary to the prompt
            # For uniformity, we can return the text directly in a formatted dict structure
            return [{"raw_mcp_output": content_text}]
            
    except Exception as e:
        logger.error(f"Failed to fetch repositories via MCP client: {e}")
        log_audit("github_fetch", "ERROR", {"username": username, "method": "MCP", "error": str(e)})
        return []

async def get_github_summary(username: str) -> str:
    """
    Aggregates GitHub data into a readable textual summary for prompt enrichment.
    """
    if not username or len(username.strip()) == 0:
        return ""
        
    repos = []
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN") or os.getenv("GITHUB_TOKEN")
    
    # Attempt MCP first if token is present
    if token:
        try:
            mcp_repos = await fetch_via_mcp(username)
            if mcp_repos:
                if len(mcp_repos) == 1 and "raw_mcp_output" in mcp_repos[0]:
                    return f"GitHub repositories and technical profile (via MCP):\n{mcp_repos[0]['raw_mcp_output']}"
                repos = mcp_repos
        except Exception as e:
            logger.warning(f"MCP path failed: {e}. Falling back to direct HTTP.")
            repos = []
            
    # If MCP didn't return any repos (either token missing or server errored), use HTTP
    if not repos:
        repos = fetch_via_http(username)
        
    if not repos:
        return f"GitHub Profile for '{username}': No public repositories found or GitHub API rate limited."
        
    # Format repos list into a concise profile summary
    summary_lines = [f"GitHub Profile for '{username}' containing repositories:"]
    for repo in repos:
        desc = f" - {repo['description']}" if repo['description'] else ""
        summary_lines.append(
            f"- {repo['name']} ({repo['language']}) | Stars: {repo['stars']} | URL: {repo['url']}{desc}"
        )
    return "\n".join(summary_lines)

if __name__ == "__main__":
    # Small test script
    test_user = "octocat"
    print("Fetching profile for", test_user)
    print(asyncio.run(get_github_summary(test_user)))
