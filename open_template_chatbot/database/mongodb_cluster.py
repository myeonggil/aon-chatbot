from motor.motor_asyncio import AsyncIOMotorClient
from open_template_chatbot.utils import get_embedding
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

    async def insert_chat(self, data: dict[str, ]):
        pass

    async def search_chat(self, data: str):
        pass

    async def _create_rag_documents(self, documents: list[dict[str, str | list]]):
        _ = await self.collection.insert_many(documents=documents)

    async def search_vector(self, query: str):
        query_embedding = get_embedding(query)
        pipeline = [
            {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "queryVector": query_embedding,
                        "path": "embedding",
                        "exact": True,
                        "limit": 5
                    }
            }, {
                    "$project": {
                    "_id": 0,
                    "text": 1
                }
            }
        ]
        results = await self.collection.aggregate(pipeline=pipeline)
        array_of_results = []
        for doc in results:
            array_of_results.append(doc)
        return array_of_results
