import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ak-mcp", host="0.0.0.0", json_response=True, stateless_http=True)


@mcp.tool()
def encrypt(text: str) -> str:
    """Encrypts a string by appending the secret key separated by underscore."""
    secret_key = os.environ.get("SECRET_KEY", "")
    if not secret_key:
        raise ValueError("SECRET_KEY environment variable is not set")
    return f"{text}_{secret_key}"


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)
