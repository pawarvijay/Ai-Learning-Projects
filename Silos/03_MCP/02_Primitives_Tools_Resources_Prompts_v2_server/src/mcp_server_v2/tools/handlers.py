from pydantic import BaseModel, Field
from mcp_server_v2.instance import mcp

class OrderItem(BaseModel):
    sku: str = Field(description="Product SKU identifier")
    quantity: int = Field(gt=0, description="Quantity")
    unit_price: float = Field(gt=0.0, description="Unit Price USD")

@mcp.tool()
def calculate_order_total(items: list[OrderItem], discount_code: str = "") -> dict:
    """Calculates discounted order totals via MCP v2."""
    subtotal = sum(i.quantity * i.unit_price for i in items)
    discount = 0.15 if discount_code.upper() == "SAVE15" else 0.0
    discounted_subtotal = subtotal * (1 - discount)
    tax = discounted_subtotal * 0.08
    total = discounted_subtotal + tax
    return {
        "engine": "MCP v2 (MCPServer)",
        "item_count": sum(i.quantity for i in items),
        "subtotal": round(subtotal, 2),
        "discount_applied": f"{int(discount * 100)}%",
        "final_total": round(total, 2)
    }

def ping_server() -> str:
    """Simple ping tool registered programmatically."""
    return "pong"

# Programmatic tool registration
mcp.add_tool(ping_server)
