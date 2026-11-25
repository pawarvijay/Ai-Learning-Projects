import asyncio
import json
from typing import Any
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context

# Initialize full-fledged FastMCP server
mcp = FastMCP("EnterprisePrimitivesServer")

# ==============================================================================
# 1. TOOLS: Model-Controlled Actions (With Structured Pydantic Parameters)
# ==============================================================================

class OrderItem(BaseModel):
    sku: str = Field(description="Stock Keeping Unit ID")
    quantity: int = Field(gt=0, description="Number of items to purchase")
    unit_price: float = Field(gt=0.0, description="Price per unit in USD")

@mcp.tool()
def calculate_order_total(items: list[OrderItem], discount_code: str = "") -> dict[str, Any]:
    """Calculates discounted line-item totals and tax for an enterprise e-commerce order."""
    subtotal = sum(item.quantity * item.unit_price for item in items)
    discount = 0.15 if discount_code.upper() == "SAVE15" else 0.0
    discounted_subtotal = subtotal * (1 - discount)
    tax = discounted_subtotal * 0.08  # 8% tax
    total = discounted_subtotal + tax
    
    return {
        "item_count": sum(item.quantity for item in items),
        "subtotal": round(subtotal, 2),
        "discount_applied": f"{int(discount * 100)}%",
        "tax": round(tax, 2),
        "final_total": round(total, 2)
    }

# ==============================================================================
# 2. RESOURCES: Application-Controlled Read-Only Data Feeds (URI Schemes)
# ==============================================================================

# Static configuration resource
@mcp.resource("config://app/settings")
def get_app_settings() -> str:
    """Returns application configuration parameters in JSON format."""
    return json.dumps({
        "environment": "production",
        "api_version": "v2.1",
        "auth_provider": "OAuth2.0 / JWT",
        "supported_locales": ["en-US", "es-ES", "fr-FR"]
    })

# Dynamic parameterized resource (e.g., database schema inspection)
@mcp.resource("schema://database/{table_name}")
def get_table_schema(table_name: str) -> str:
    """Exposes real-time database schema information for a requested table."""
    schemas = {
        "users": "CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE, created_at TIMESTAMP);",
        "orders": "CREATE TABLE orders (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), amount NUMERIC(10, 2));",
        "products": "CREATE TABLE products (sku VARCHAR(50) PRIMARY KEY, title TEXT, stock_count INT);"
    }
    return schemas.get(table_name.lower(), f"-- Table '{table_name}' does not exist in database schema.")

# ==============================================================================
# 3. PROMPTS: User/Host-Controlled Standardized Reusable Workflows
# ==============================================================================

@mcp.prompt()
def triage_customer_ticket(ticket_body: str, customer_tier: str = "Standard") -> str:
    """Standardized enterprise prompt template for support ticket triage."""
    return f"""You are a tier-1 customer success engineer.
Customer Tier: {customer_tier}
Analyze the following customer ticket:
<ticket>
{ticket_body}
</ticket>

Instructions:
1. Identify the core user frustration in 1 sentence.
2. Determine if escalation is required (Tier == 'Enterprise' always escalates to P1).
3. Draft a polite, concise response acknowledging their issue.
"""
