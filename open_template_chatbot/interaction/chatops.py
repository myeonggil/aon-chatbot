# slack message trigger
# telemetry apply
# something API? I don't know well...
# Go for DevOps.ref
from enum import StrEnum
from typing import Callable

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.context.say.async_say import AsyncSay
from open_template_chatbot.configs import env_config as config

# import asyncio
import logging


class AppMention(StrEnum):
    MESSAGE: str = "message"
    REACTION_ADDED: str = "reaction_added"
    REACTION_REMOVED: str = "reaction_removed"
    MEMBER_JOINED_CHANNEL: str = "member_joined_channel"
    MEMBER_LEFT_CHANNEL: str = "member_left_channel"
    APP_MENTION: str = "app_mention"
    USER_CHANGE: str = "user_change"
    CHANNEL_CREATED: str = "channel_created"
    CHANNEL_DELETED: str = "channel_deleted"
    FILE_SHARED: str = "file_shared"


class ChatOps:
    def __init__(self, app: AsyncApp):
        self.app = app

    def message(self, func: Callable):
        @self.app.message("aon ")
        async def message_something(message: dict[str, str | list[dict[str, any]]], say: AsyncSay):
            # say() sends a message to the channel where the event was triggered
            _, prompt = message['text'].split('aon ')
            response = await func(prompt)
            await say(
                # blocks=[
                #     {
                #         "type": "section",
                #         "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                #         "accessory": {
                #             "type": "button",
                #             "text": {"type": "plain_text", "text": "Click Me"},
                #             "action_id": "button_click"
                #         }
                #     }
                # ],
                # text=f"Hey there <@{message['user']}>!"
                text=response
            )

    def event(self):
        @self.app.event("message")
        async def handle_message_events(body, logger: logging.Logger):
            logger.info(body)

    def action(self):
        @self.app.action("button_click")
        async def action_button_click(body, ack, say):
            # Acknowledge the action
            await ack()
            await say(f"<@{body['user']['id']}> clicked the button")

    async def start_app(self):
        try:
            socket_handler = AsyncSocketModeHandler(app=app, app_token=config["SLACK_APP_TOKEN"])
            await socket_handler.start_async()
        except Exception as err:
            print(err)
        finally:
            await socket_handler.close_async()

app = AsyncApp(token=config["SLACK_BOT_TOKEN"])
chatops = ChatOps(app=app)
