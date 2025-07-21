from abc import ABC, abstractmethod

from pymongo import AsyncMongoClient


class ILLMRepository(ABC):

    """
        How to create variable code.
        Interface and Repository version
    """

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def set_motor_client(self, client: AsyncMongoClient) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def insert_chat(self, data: dict[str, any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def search_chat(self, data: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def create_rag_documents(self, documents: list[dict[str, str | list]]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_context_string_from_docs(self, embedded_query: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def search_vector(self, embedded_query: str) -> list[str]:
        raise NotImplementedError()
