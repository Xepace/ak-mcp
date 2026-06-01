# AK MCP Server

MCP сервер для тестирования интеграции. Предоставляет один инструмент `encrypt`, который добавляет к входной строке значение из переменной окружения `SECRET_KEY` через разделитель `_`.

## Использование

### Локально (stdio)

```bash
pip install -r requirements.txt
SECRET_KEY=mysecret python server.py --transport stdio
```

### Локально (streamable-http)

```bash
SECRET_KEY=mysecret python server.py --transport streamable-http --port 8000 --json-response --stateless
```

### Docker

```bash
docker build -t ak-mcp .
docker run -e SECRET_KEY=mysecret -p 8000:8000 ak-mcp
```

Endpoint: `http://localhost:8000/mcp`

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SECRET_KEY` | Ключ, добавляемый к шифруемой строке | — |
| `MCP_TRANSPORT` | Транспорт: `stdio` или `streamable-http` | `streamable-http` |
| `MCP_PORT` | Порт для streamable-http | `8000` |
