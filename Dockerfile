FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY ak_mcp/ ak_mcp/
RUN pip install --no-cache-dir .

ENV SECRET_KEY=""
ENV MCP_TRANSPORT=streamable-http
ENV FASTMCP_PORT=8000

EXPOSE ${FASTMCP_PORT}

CMD ["ak-mcp"]
