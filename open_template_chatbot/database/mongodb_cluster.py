from pymongo import AsyncMongoClient
from open_template_chatbot.configs import env_config as config

# 비동기 클라이언트 설정
MONGO_URI = config['MONGO_URI']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
MONGO_URI = MONGO_URI.replace(
    '<username>', USERNAME
).replace(
    '<password>', PASSWORD
)
