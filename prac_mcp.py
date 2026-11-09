from fastmcp import FastMCP

mcp=FastMCP(
    'MCP Server'
)

@mcp.tool
def add(a:int, b:int)->int:
    """Takes two numbers and return their sum"""
    return a+b

mcp.run(transport='streamable-http')