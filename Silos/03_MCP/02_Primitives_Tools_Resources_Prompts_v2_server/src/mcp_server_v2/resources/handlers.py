from mcp_server_v2.instance import mcp

@mcp.resource("config://app/settings")
def get_app_settings() -> str:
    """Static configuration resource via MCP v2."""
    return '{"version": "v2.0", "engine": "MCPServer", "auth": "OAuth2.0"}'

@mcp.resource("schema://database/{table_name}")
def get_table_schema(table_name: str) -> str:
    """Dynamic parameterized database schema resource."""
    schemas = {
        "users": "CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(255));",
        "orders": "CREATE TABLE orders (id SERIAL PRIMARY KEY, total NUMERIC(10,2));"
    }
    return schemas.get(table_name.lower(), f"-- Table {table_name} not found.")
