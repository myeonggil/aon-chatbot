import typer
import asyncio

from aon_chatbot.services import llm_service
from aon_chatbot.interaction.chatops import chatops


socket_app = typer.Typer(name='slack')
@socket_app.command(name='run')
def connect_slack():
    try:
        asyncio.run(llm_service.run_slack_socket(chatops))
    except Exception as err:
        print(err)
    except KeyboardInterrupt as err:
        print(err)
    finally:
        pass
