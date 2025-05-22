#!/bin/bash

# docker build platform linux/amd64 or linux/arm64
# lima nerdctl build -t $image .

# docker run with mount
# lima nerdctl run -v /Users/jumyeonggil/.aws:/root/.aws -v ./:/var/task --network host --name $image -it base
# docker run -p 8501:8000 -v ./config.yaml:/var/task/config.yaml -v ./.env:/var/task/open_template_chatbot/.env \
#     --name slack -it mgju/open-template-chatbot:latest \
#     python -m open_template_chatbot.interaction.chatops

python -m open_template_chatbot.interaction.chatops
