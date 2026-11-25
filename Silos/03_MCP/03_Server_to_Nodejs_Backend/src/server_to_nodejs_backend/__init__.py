from mock_mcp import mock_mcp_tool_execute

def main():
    result = mock_mcp_tool_execute("calculate_discount", {"price": 100})
    print(f"Final MCP Tool Result from Node.js: {result['data']}")

if __name__ == "__main__":
    main()
