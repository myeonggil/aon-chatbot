# slack message trigger
# telemetry apply
# something API? I don't know well...
# Go for DevOps.ref
from enum import StrEnum
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.context.say.async_say import AsyncSay
from open_template_chatbot.configs import env_config as config

from open_template_chatbot.llm_models import groq_template_response

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


app = AsyncApp(token=config["SLACK_BOT_TOKEN"])

# Listens to incoming messages that contain "hello"
@app.message("aon ")
async def message_hello(message: dict[str, str | list[dict[str, any]]], say: AsyncSay):
    # say() sends a message to the channel where the event was triggered
    _, prompt = message['text'].split('aon ')
    response = await groq_template_response(prompt)
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

@app.event("message")
async def handle_message_events(body, logger: logging.Logger):
    logger.info(body)

# @app.event("app_mention")
# async def who_am_i(event, client, message, say):
#     print("called")

# @app.action("button_click")
# async def action_button_click(body, ack, say):
#     # Acknowledge the action
#     await ack()
#     await say(f"<@{body['user']['id']}> clicked the button")


async def main():
    try:
        socket_handler = AsyncSocketModeHandler(app=app, app_token=config["SLACK_APP_TOKEN"])
        await socket_handler.start_async()
    except Exception as err:
        print(err)
    finally:
        await socket_handler.close_async()


# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except Exception as err:
#         print(err)
#     except KeyboardInterrupt as err:
#         print(err)
#     finally:
#         pass
