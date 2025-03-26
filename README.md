# COZE MCP Server

A Model Context Protocol server that provides coze resource and tool.

### Available Tools

- `list_workspaces` - Get workspaces list
- `list_bots` - Get bots list
- `create_bot` - Create bot
- `get_me`: Get self user info
- `list_workspaces`: List workspaces
- `list_bots`: List bots
- `retrieve_bot`: Retrieve bot info
- `create_bot`: Create bot
- `update_bot`: Update bot
- `publish_bot`: Publish bot to API channel
- `chat_with_bot`: Chat with bot
- `chat_with_workflow`: Chat with workflow
- `list_voices`: List voice

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *coze-mcp-server*.

### Using PIP

Alternatively you can install `coze-mcp-server` via pip:

```bash
pip install coze-mcp-server
```

After installation, you can run it as a script using:

```bash
python -m coze_mcp_server
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "coze-mcp-server": {
    "command": "uvx",
    "args": ["coze-mcp-server"]
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
"mcpServers": {
  "coze-mcp-server": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "ghcr.io/coze-dev/coze-mcp-server"]
  }
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "coze-mcp-server": {
    "command": "python",
    "args": ["-m", "coze_mcp_server"]
  }
}
```
</details>

### Configure for Zed

Add to your Zed settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "coze-mcp-server": {
    "command": "uvx",
    "args": ["coze-mcp-server"]
  }
],
```
</details>

<details>
<summary>Using pip installation</summary>

```json
"context_servers": {
  "coze-mcp-server": {
    "command": "python",
    "args": ["-m", "coze_mcp_server"]
  }
},
```
</details>

## License

MIT License.
