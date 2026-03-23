from src.core.server import mcp


def handler(event, context):
    return mcp.handler(event, context)
