"""Prompt client operations."""

from mcp import ClientSession
from mcp.types import GetPromptResult, ListPromptsResult


async def fetch_prompts(session: ClientSession) -> ListPromptsResult:
    """Discovers all reusable prompt templates exposed by the server."""
    return await session.list_prompts()


async def render_prompt(
    session: ClientSession, name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    """Renders a prompt template with provided arguments."""
    return await session.get_prompt(name=name, arguments=arguments or {})
