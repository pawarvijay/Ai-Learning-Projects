from mcp_server_v2.instance import mcp

@mcp.prompt()
def triage_customer_ticket(ticket_body: str, customer_tier: str = "Standard") -> str:
    """Customer ticket triage prompt template."""
    return f"""[MCP v2 Prompt Template]
Customer Tier: {customer_tier}
Ticket Content: {ticket_body}
Action: Categorize urgency and provide root-cause summary.
"""
