from pymongo import AsyncMongoClient
from aon_chatbot.configs import config

# 비동기 클라이언트 설정
MONGO_URI = config['MONGO_URI']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
MONGO_URI = MONGO_URI.replace(
    '<username>', USERNAME
).replace(
    '<password>', PASSWORD
)

def get_motor_client():
    return AsyncMongoClient(MONGO_URI)
