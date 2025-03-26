## Setting up the environment

create a virtual environment:

```shell
python -m venv ./.venv
```

active the virtual environment:

```shell
source ./.venv/bin/activate
```

We use [uv](https://docs.astral.sh/uv/) to manage dependencies, you can install it by:

```shell
python -m pip install uv 
```

And then install dependencies:

```shell
uv sync
```

## Pre Commit

```shell
pre-commit install
```

## Dev MCP Server

start mcp dev server:


```shell
export COZE_API_TOKEN=your_coze_token
mcp dev src/coze_mcp_server/server.py
```

## Prod MCP Server

```shell
uvx coze-mcp-server --coze-api-token=your_coze_token
```