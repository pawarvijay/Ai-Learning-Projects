import asyncio
from mock_mcp import run_nodejs_gateway_demo

def main():
    asyncio.run(run_nodejs_gateway_demo())

if __name__ == "__main__":
    main()
