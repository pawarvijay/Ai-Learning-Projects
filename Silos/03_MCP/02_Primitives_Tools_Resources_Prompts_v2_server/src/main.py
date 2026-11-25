import anyio
import sys
from mcp_server_v2 import mcp

def main():
    print("=" * 65, file=sys.stderr)
    print(" [SERVER] Starting Standalone MCP v2 Server Daemon on stdio...", file=sys.stderr)
    print(f" [SERVER] Registered Server: {mcp.name}", file=sys.stderr)
    print("=" * 65, file=sys.stderr)
    anyio.run(mcp.run_stdio_async)

if __name__ == "__main__":
    main()
