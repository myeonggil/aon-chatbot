from pymongo import AsyncMongoClient

from aon_chatbot.interfaces.chat_repository_interface import IChatRepository
from aon_chatbot.interfaces.llm_repository_interface import ILLMRepository


class LLMRepository(ILLMRepository):

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
            self.db = None
            self.collection = None

    async def set_motor_client(self, client: AsyncMongoClient):
        self.client = client
        self.db = self.client['chatbot']
        self.collection = self.db['chat_history']

    async def insert_chat(self, data: dict[str, any]):
        pass

    async def search_chat(self, data: str):
        pass

    async def create_rag_documents(self, documents: list[dict[str, str | list]]):
        result = await self.collection.insert_many(documents=documents)
        return result

    # async def get_context_string_from_docs(self, embedded_query: list[float]) -> str:
    #     context_docs = await self.search_vector(embedded_query=embedded_query)
    #     context_string = " ".join([doc["text"] for doc in context_docs])
    #     return context_string

    async def search_vector(self, embedded_query: list[float], min_score: float = 0.75):
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": embedded_query,
                    "path": "embedding",
                    "exact": True,
                    "limit": 5,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
            {"$match": {"score": {"$gte": min_score}}},
        ]
        results = []
        async for doc in await self.collection.aggregate(pipeline=pipeline):
            results.append(doc)
        return results

    async def get_context_string_from_docs(self, embedded_query: list[float]) -> str:
        context_docs = await self.search_vector(embedded_query=embedded_query)
        if not context_docs:
            return ""
        return "\n\n".join(doc["text"] for doc in context_docs)

    async def search_multi(self, vectors: list[list[float]], min_score: float = 0.75):
        best: dict[str, dict] = {}
        for vec in vectors:
            for doc in await self.search_vector(vec, min_score=min_score):
                key = doc["text"]
                if key not in best or doc["score"] > best[key]["score"]:
                    best[key] = doc
        return sorted(best.values(), key=lambda d: d["score"], reverse=True)[:5]

    async def get_context_string_from_multi(self, vectors: list[list[float]]) -> str:
        docs = await self.search_multi(vectors)
        if not docs:
            return ""
        return "\n\n".join(doc["text"] for doc in docs)


llm_repository = LLMRepository()
