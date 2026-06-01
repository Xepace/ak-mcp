FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

ENV SECRET_KEY=""
ENV MCP_TRANSPORT=streamable-http
ENV MCP_PORT=8000

EXPOSE ${MCP_PORT}

CMD ["sh", "-c", "python server.py --transport ${MCP_TRANSPORT} --port ${MCP_PORT} --json-response --stateless"]
