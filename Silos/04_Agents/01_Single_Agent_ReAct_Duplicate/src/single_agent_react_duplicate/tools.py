from langchain_core.tools import tool


@tool
def calculate_discount(price: float, discount_pct: float) -> str:
    """Calculates discounted price given price and discount percentage."""
    final_price = price * (1 - discount_pct / 100)
    return f"Final discounted price is ${final_price:.2f}"


tools = [calculate_discount]
