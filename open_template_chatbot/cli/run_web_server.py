import typer
import subprocess

from open_template_chatbot.utils import update_streamlit_config


web_server_app = typer.Typer(name='streamlit')
@web_server_app.command(name='run')
def startup_gui(
    browser_gatherUsageStats: bool = typer.Option(False, "--browser.gatherUsageStats", help="gather usage stats"),
    server_headless: bool = typer.Option(True, "--server.headless", help="server without head"),
    server_enableXsrfProtection: bool = typer.Option(False, "--server.enableXsrfProtection", help="server without head"),
    server_enableCORS: bool = typer.Option(False, "--server.enableCORS", help="server without head"),
    server_address: str = typer.Option('0.0.0.0', "--server.address", help="server without head"),
    server_port: int = typer.Option(8501, "--server.port", help="server without head"),
):
    update_streamlit_config(
        browser_gatherUsageStats=browser_gatherUsageStats,
        server_headless=server_headless,
        server_enableXsrfProtection=server_enableXsrfProtection,
        server_enableCORS=server_enableCORS,
        server_address=server_address,
        server_port=server_port
    )
    run_command = ["streamlit", "run", "open_template_chatbot/main.py"]
    subprocess.run(run_command)
