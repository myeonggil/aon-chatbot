from pymongo import AsyncMongoClient
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
        self.client = AsyncMongoClient(MONGO_URI)
        self.db = self.client['chatbot']
        self.collection = self.db['chat_history']

    async def close(self):
        await self.client.close()

    async def insert_chat(self, data: dict[str, ]):
        pass

    async def search_chat(self, data: str):
        pass

    async def _create_rag_documents(self, documents: list[dict[str, str | list]]):
        result = await self.collection.insert_many(documents=documents)
        return result

    async def get_context_string_from_docs(self, query: str) -> str:
        context_docs = await self._search_vector(query=query)
        context_string = " ".join([doc["text"] for doc in context_docs])
        return context_string

    async def _search_vector(self, query: str):
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
        array_of_results = []
        async for doc in await self.collection.aggregate(pipeline=pipeline):
            array_of_results.append(doc)
        return array_of_results
