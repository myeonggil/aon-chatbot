import typer

from open_template_chatbot.utils import update_streamlit_config
from open_template_chatbot.interaction.chatbot_with_gui import run_streamlit


web_server_app = typer.Typer(name='streamlit')
@web_server_app.command(name='run')
def startup_gui(
    browser_gatherUsageStats: str = typer.Option('false', "--browser.gatherUsageStats", help="gather usage stats"),
    server_headless: str = typer.Option('true', "--server.headless", help="server without head"),
    server_enableXsrfProtection: str = typer.Option('true', "--server.enableXsrfProtection", help="server without head"),
    server_enableCORS: str = typer.Option('false', "--server.enableCORS", help="server without head"),
    server_address: str = typer.Option('0.0.0.0', "--server.address", help="server without head"),
    server_port: str = typer.Option('8501', "--server.port", help="server without head"),
):
    # run_command = ["streamlit", "run", "--browser.gatherUsageStats", browser_gatherUsageStats,
    #     "--server.headless", server_headless, "--server.enableXsrfProtection", server_enableXsrfProtection,
    #     "--server.enableCORS", server_enableCORS, "--server.address", server_address,
    #     "--server.port", server_port, "open_template_chatbot/interaction/chatbot_with_gui.py"]
    # subprocess.run(run_command)
    update_streamlit_config(
        browser_gatherUsageStats,
        server_headless,
        server_enableXsrfProtection,
        server_enableCORS,
        server_address,
        server_port
    )
    run_streamlit()
