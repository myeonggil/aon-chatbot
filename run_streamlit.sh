#!/bin/bash

# docker build platform linux/amd64 or linux/arm64
# lima nerdctl build -t $image .

# docker run with mount
# lima nerdctl run -v /Users/jumyeonggil/.aws:/root/.aws -v ./:/var/task --network host --name $image -it base
docker run -p 8501:8000 -v ./config.yaml:/var/task/config.yaml -v ./.env:/var/task/open_template_chatbot/.env \
    --name treamlit -it mgju/open-template-chatbot:latest \
    streamlit run --browser.gatherUsageStats false --server.headless true --server.enableXsrfProtection false --server.enableCORS false --server.address 0.0.0.0 --server.port 8000 open_template_chatbot/interaction/chatbot_with_gui.py
