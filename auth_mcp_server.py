JWT_SECRET_KEY='1d3b13ad-2b77-47e3-ade7-cc1bc0cc3806'
JWT_ALGO='HS256'
JWT_ISSUER='http://localhost:8001'
JWT_EXPIRE_HOURS=1
JWT_AUDIENCE='my-mcp-server'

from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token


verifier=JWTVerifier(
    public_key=JWT_SECRET_KEY,
    algorithm=JWT_ALGO,
    issuer=JWT_ISSUER,
    audience=JWT_AUDIENCE
)

mcp=FastMCP(
    'Secure MCP Server',
    auth=verifier
)

@mcp.tool
def whoami()->dict:
    """Returns the user id of current authenticated user"""
    token=get_access_token()
    print("\n\n,token,\n\n")
    return {'client_id':token.client_id,'email':token.claims.get('emails',' ')}


mcp.run(transport='streamable-http')