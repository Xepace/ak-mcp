import os

import click
import anyio
from mcp.server import Server
from mcp import types

SERVER_NAME = "ak-mcp"


def create_server() -> Server:
    app = Server(SERVER_NAME, on_list_tools=handle_list_tools, on_call_tool=handle_call_tool)
    return app


async def handle_list_tools(
    ctx,
    params,
) -> types.ListToolsResult:
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="encrypt",
                description="Encrypts a string by appending the secret key",
                input_schema={
                    "type": "object",
                    "required": ["text"],
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The string to encrypt",
                        },
                    },
                },
            )
        ]
    )


async def handle_call_tool(
    ctx,
    params,
) -> types.CallToolResult:
    if params.name == "encrypt":
        args = params.arguments or {}
        text = args.get("text", "")
        secret_key = os.environ.get("SECRET_KEY", "")

        if not secret_key:
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text="Error: SECRET_KEY environment variable is not set",
                    )
                ],
                is_error=True,
            )

        encrypted = f"{text}_{secret_key}"
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=encrypted)]
        )

    raise ValueError(f"Unknown tool: {params.name}")


@click.command()
@click.option("--port", default=8000, help="Port for HTTP transport")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "streamable-http"]),
    default="stdio",
    help="Transport type",
)
@click.option("--json-response", is_flag=True, help="Use JSON responses for streamable-http")
@click.option("--stateless", is_flag=True, help="Run in stateless mode")
def main(port: int, transport: str, json_response: bool, stateless: bool) -> None:
    app = create_server()

    if transport == "streamable-http":
        import uvicorn

        uvicorn.run(
            app.streamable_http_app(
                streamable_http_path="/mcp",
                json_response=json_response,
                stateless_http=stateless,
            ),
            host="0.0.0.0",
            port=port,
        )
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0],
                    streams[1],
                    app.create_initialization_options(),
                )

        anyio.run(arun)


if __name__ == "__main__":
    main()
