"""Resource client operations."""

from pydantic import AnyUrl
from mcp import ClientSession
from mcp.types import ListResourcesResult, ListResourceTemplatesResult, ReadResourceResult


async def fetch_resources(session: ClientSession) -> ListResourcesResult:
    """Discovers all static resources exposed by the server."""
    return await session.list_resources()


async def fetch_resource_templates(session: ClientSession) -> ListResourceTemplatesResult:
    """Discovers all parameterized resource templates (URIs with variables) exposed by the server."""
    return await session.list_resource_templates()


async def read_resource_content(session: ClientSession, uri: str | AnyUrl) -> ReadResourceResult:
    """Reads static or templated resource contents from the server."""
    return await session.read_resource(uri)


async def subscribe_to_resource(session: ClientSession, uri: str | AnyUrl) -> None:
    """Subscribes to updates for a specific resource URI."""
    await session.subscribe_resource(uri)


async def unsubscribe_from_resource(session: ClientSession, uri: str | AnyUrl) -> None:
    """Unsubscribes from updates for a specific resource URI."""
    await session.unsubscribe_resource(uri)
