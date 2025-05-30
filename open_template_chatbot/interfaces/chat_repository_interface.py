from abc import ABC, abstractmethod


class IChatRepository(ABC):

    """
        How to create variable code.
        Interface and Repository version
    """

    @abstractmethod
    async def insert_many(self, docs: list[dict[str, str]]):
        raise NotImplementedError()

    @abstractmethod
    async def insert_one(self, data: str | list | dict):
        raise NotImplementedError()

    @abstractmethod
    async def get_one(self):
        raise NotImplementedError()

    @abstractmethod
    async def get_many(self):
        raise NotImplementedError()

    @abstractmethod
    async def update_one(self):
        pass

    @abstractmethod
    async def update_many(self):
        pass
