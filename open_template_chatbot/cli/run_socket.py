import typer
import asyncio

from open_template_chatbot.interaction.chatops import main


socket_app = typer.Typer(name='slack')
@socket_app.command(name='run')
def connect_slack():
    try:
        asyncio.run(main())
    except Exception as err:
        print(err)
    except KeyboardInterrupt as err:
        print(err)
    finally:
        pass
