import os
import sys
from typing import List

from cozepy import (
    AsyncCoze,
    AsyncTokenAuth,
    COZE_CN_BASE_URL,
    BotPromptInfo,
    Bot,
    Message,
    ChatEventType,
    Voice,
    User,
)
from mcp.server import FastMCP
from pydantic import BaseModel


class Config(BaseModel):
    api_token: str
    api_base: str

    @staticmethod
    def build():
        api_base = os.getenv("COZE_API_BASE") or COZE_CN_BASE_URL
        api_token = os.getenv("COZE_API_TOKEN") or ""

        for idx, val in enumerate(sys.argv):
            if val == "--coze-api-base" and idx + 1 < len(sys.argv):
                api_base = sys.argv[idx + 1]
            elif val == "--coze-api-token" and idx + 1 < len(sys.argv):
                api_token = sys.argv[idx + 1]
            elif val.startswith("--coze-api-base="):
                api_base = val.split("--coze-api-base=")[1]
            elif val.startswith("--coze-api-token="):
                api_token = val.split("--coze-api-token=")[1]

        return Config(
            api_base=api_base,
            api_token=api_token,
        )


class CozeServer(object):
    def __init__(self, api_base: str, api_token: str):
        self.coze = AsyncCoze(auth=AsyncTokenAuth(token=api_token), base_url=api_base)

    async def bot_chat(self, bot_id: str, content: str) -> str:
        stream = self.coze.chat.stream(
            bot_id=str(bot_id),
            user_id="coze-mcp-server",
            additional_messages=[Message.build_user_question_text(content)],
        )
        msg = ""
        async for event in stream:
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                msg += event.message.content
        return msg

    async def workflow_chat(self, bot_id: str, workflow_id: str, content: str) -> str:
        conversation = await self.coze.conversations.create()
        stream = self.coze.workflows.chat.stream(
            workflow_id=str(workflow_id),
            user_id="coze-mcp-server",
            additional_messages=[Message.build_user_question_text(content)],
            bot_id=bot_id,
            conversation_id=conversation.id,
        )
        msg = ""
        async for event in stream:
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                msg += event.message.content
        return msg


mcp = FastMCP("coze-mcp")
conf = Config.build()
server = CozeServer(conf.api_base, conf.api_token)


@mcp.tool(description="get self user info")
async def get_me() -> User:
    return await server.coze.users.me()


@mcp.tool(description="list coze workspaces")
async def list_workspaces():
    res = await server.coze.workspaces.list()
    return [item async for item in res]


@mcp.tool(description="list bots in workspaces")
async def list_bots(workspace_id: int | str):
    res = await server.coze.bots.list(space_id=str(workspace_id))
    return res.items


@mcp.tool(description="retrieve bot")
async def retrieve_bot(bot_id: int | str) -> Bot:
    return await server.coze.bots.retrieve(bot_id=str(bot_id))


@mcp.tool(description="create bot in workspaces")
async def create_bot(
    workspace_id: int | str,
    name: str,
    description: str | None = None,
    prompt: str | None = None,
) -> Bot:
    return await server.coze.bots.create(
        space_id=str(workspace_id),
        name=name,
        description=description,
        prompt_info=None if not prompt else BotPromptInfo(prompt=prompt),
    )


@mcp.tool(description="update bot info")
async def update_bot(
    bot_id: int | str,
    name: str | None = None,
    description: str | None = None,
    prompt: str | None = None,
):
    await server.coze.bots.update(
        bot_id=str(bot_id),
        name=name,
        description=description,
        prompt_info=None if not prompt else BotPromptInfo(prompt=prompt),
    )


@mcp.tool(description="publish bot info")
async def publish_bot(bot_id: int | str) -> Bot:
    return await server.coze.bots.publish(
        bot_id=str(bot_id),
    )


@mcp.tool(description="chat with bot")
async def chat_with_bot(
    bot_id: int | str,
    content: str,
) -> str:
    return await server.bot_chat(
        bot_id=str(bot_id),
        content=content,
    )


@mcp.tool(description="chat with bot")
async def chat_with_workflow(
    bot_id: int | str,
    workflow_id: int | str,
    content: str,
) -> str:
    return await server.workflow_chat(
        bot_id=str(bot_id),
        workflow_id=str(workflow_id),
        content=content,
    )


@mcp.tool(description="list my all voice")
async def list_voices() -> List[Voice]:
    res = await server.coze.audio.voices.list()
    items = [item async for item in res]
    return items
