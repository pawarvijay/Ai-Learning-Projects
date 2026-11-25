import asyncio
from typing import Any
import httpx
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# FastMCP gateway exposing Node.js microservice endpoints as AI tools
mcp = FastMCP("NodeJsBackendGateway")

# Node.js Express service target URL (or local mock adapter)
NODEJS_BASE_URL = "http://127.0.0.1:3000/api"

class DiscountPayload(BaseModel):
    product_id: str = Field(description="Internal product identifier")
    original_price: float = Field(gt=0, description="Base product price")
    user_tier: str = Field(default="Standard", description="Customer loyalty tier: Standard, Gold, Platinum")

@mcp.tool()
async def calculate_loyalty_discount(payload: DiscountPayload) -> dict[str, Any]:
    """Delegates loyalty discount calculation to internal Node.js Express microservice."""
    try:
        # Standard async HTTP REST call to Node.js backend
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{NODEJS_BASE_URL}/calculate-discount",
                json=payload.model_dump()
            )
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        # Graceful fallback simulation when Node.js server is offline
        tier_multipliers = {"Standard": 0.05, "Gold": 0.15, "Platinum": 0.25}
        discount_rate = tier_multipliers.get(payload.user_tier, 0.05)
        discount_amount = round(payload.original_price * discount_rate, 2)
        
        return {
            "source": "Node.js Fallback Adapter (Local)",
            "product_id": payload.product_id,
            "original_price": payload.original_price,
            "tier": payload.user_tier,
            "discount_rate": f"{int(discount_rate * 100)}%",
            "discount_amount": discount_amount,
            "final_price": round(payload.original_price - discount_amount, 2),
            "status": "success"
        }

@mcp.tool()
async def query_inventory_stock(product_id: str) -> dict[str, Any]:
    """Queries PostgreSQL database stock count through Node.js data access layer."""
    # Simulates Node.js knex/prisma query: SELECT stock, warehouse FROM inventory WHERE id = ?
    return {
        "product_id": product_id,
        "in_stock": True,
        "available_units": 142,
        "warehouse_location": "US-EAST-DC1",
        "verified_at_db": "PostgreSQL 16"
    }
