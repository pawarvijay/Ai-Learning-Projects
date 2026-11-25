from mcp.types import Completion, CompletionArgument, PromptReference, ResourceTemplateReference
from mcp_server_v2.instance import mcp

@mcp.completion()
async def handle_completion(
    ref: PromptReference | ResourceTemplateReference,
    argument: CompletionArgument,
) -> Completion | None:
    """Provides autocomplete suggestions for prompt or resource template arguments."""
    if isinstance(ref, ResourceTemplateReference) and argument.name == "table_name":
        tables = ["users", "orders", "invoices", "audit_logs"]
        matches = [t for t in tables if t.startswith(argument.value)]
        return Completion(values=matches, hasMore=False)
    if isinstance(ref, PromptReference) and argument.name == "customer_tier":
        tiers = ["Standard", "Pro", "Enterprise"]
        matches = [t for t in tiers if t.lower().startswith(argument.value.lower())]
        return Completion(values=matches, hasMore=False)
    return None
