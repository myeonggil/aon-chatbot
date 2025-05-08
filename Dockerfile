FROM python:3.13-slim

COPY ./ /var/task

WORKDIR /var/task

RUN pip install .

CMD ["streamlit", "run", "--browser.gatherUsageStats", "false", "--server.headless", "true", "--server.enableXsrfProtection", "false", "--server.enableCORS", "false", "--server.address", "0.0.0.0", "--server.port", "8000", "open_template_chatbot/interaction/chatbot_with_gui.py"]
