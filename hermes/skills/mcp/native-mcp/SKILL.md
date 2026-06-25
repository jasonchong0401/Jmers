---
name: native-mcp
description: "MCP client: connect servers, register tools (stdio/HTTP)."
version: 1.0.0
---

# Native MCP Client

Hermes Agent has a built-in MCP client that connects to MCP servers at startup, discovers their tools, and makes them available as first-class tools.

## Quick Start

Add MCP servers to `~/.hermes/config.yaml` under the `mcp_servers` key:

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

Restart Hermes Agent. Tools are auto-discovered with prefix `mcp_{server}_{tool}`.

## Configuration

### Stdio Transport

```yaml
mcp_servers:
  server_name:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "your_token_here"
    timeout: 120
    connect_timeout: 60
```

### HTTP Transport

```yaml
mcp_servers:
  server_name:
    url: "https://my-server.example.com/mcp"
    headers:
      Authorization: "Bearer your_token"
    timeout: 180
```

## Security

For stdio servers, Hermes does NOT pass your full shell environment. Only baseline vars (PATH, HOME, etc.) are inherited. API keys must be explicitly in `env:` config.

### Token must be in config.yaml, NOT just .env

Hermes filters the environment for MCP subprocesses. `.env` variables are NOT inherited. The token must be in `config.yaml` under `mcp_servers.<name>.env`.

## Troubleshooting

- `MCP SDK not available`: `pip install mcp`
- `No MCP servers configured`: Add at least one server to `mcp_servers` in config.yaml
- `ClosedResourceError` on MCP tools: Start a new Hermes session (`/quit` then `hermes`). `/reload-mcp` won't fix it.
- Server starts but 401: Token not in `env:` config — must be in config.yaml, not just .env

## Adding with hermes mcp command

```bash
hermes mcp add github --command npx --args "-y" --args "@modelcontextprotocol/server-github"
```

Then inject token into config.yaml `mcp_servers.github.env.GITHUB_PERSONAL_ACCESS_TOKEN` and restart Hermes.
