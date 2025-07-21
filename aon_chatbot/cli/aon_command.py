import typer

from aon_chatbot.cli.run_web_server import web_server_app
from aon_chatbot.cli.run_socket import socket_app


app = typer.Typer()
app.add_typer(web_server_app)
app.add_typer(socket_app)


if __name__ == '__main__':
    app()
