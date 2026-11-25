"""Completion client operations."""

from mcp import ClientSession
from mcp.types import CompleteResult, PromptReference, ResourceTemplateReference


async def request_completion(
    session: ClientSession,
    ref: PromptReference | ResourceTemplateReference,
    argument: dict[str, str],
) -> CompleteResult:
    """Requests auto-complete options from the server for a prompt argument or resource template."""
    return await session.complete(ref=ref, argument=argument)
