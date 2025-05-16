from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values

config = dotenv_values("open_template_chatbot/.env")
# 비동기 클라이언트 설정
MONGO_URI = config['MONGO_URI']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
MONGO_URI = MONGO_URI.replace(
    '<username>', USERNAME
).replace(
    '<password>', PASSWORD
)


# user email, llm model, chat, date
class MongoDBCluster:

    # vector search index
    """
    {
        "fields": [
            {
                "numDimensions": 1536,
                "path": "plot_embedding",
                "similarity": "euclidean",
                "type": "vector"
            }
        ]
    }
    """

    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client['chatbot']
        self.collection = self.db['chat_history']
