import sys
from mcp_server_v2 import mcp

def main():
    print("=" * 65, file=sys.stderr)
    print(" [SERVER] Starting Standalone MCP v2 Server Daemon on streamable-http...", file=sys.stderr)
    print(f" [SERVER] Registered Server: {mcp.name}", file=sys.stderr)
    print(" [SERVER] Endpoint: http://127.0.0.1:6162/mcp", file=sys.stderr)
    print("=" * 65, file=sys.stderr)

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",               # Default - Bind to all network interfaces for remote machines
        port=6162,                    # Default - Custom port
        streamable_http_path="/mcp"   # Default - Custom endpoint path
    )

if __name__ == "__main__":
    main()
