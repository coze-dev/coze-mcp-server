import asyncio

from .server import mcp


def main():
    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
