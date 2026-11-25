# import json
# 
# def handle_stdio_rpc(raw_line: str):
#     msg = json.loads(raw_line)
#     if msg.get("method") == "tools/list":
#         return json.dumps({
#             "jsonrpc": "2.0",
#             "id": msg.get("id"),
#             "result": {"tools": [{"name": "ping", "description": "Returns pong"}]}
#         })
#     return json.dumps({"jsonrpc": "2.0", "id": msg.get("id"), "result": {}})
# 
# def run():
#     test_req = '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
#     res = handle_stdio_rpc(test_req)
#     print(f"MCP stdio response: {res}")
