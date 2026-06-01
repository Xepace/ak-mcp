FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

ENV SECRET_KEY=""
ENV MCP_TRANSPORT=streamable-http
ENV FASTMCP_PORT=8000

EXPOSE ${FASTMCP_PORT}

CMD ["python", "server.py"]
