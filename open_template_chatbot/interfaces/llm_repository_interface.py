from abc import ABCMeta, abstractmethod


class ILLMRepository(meta=ABCMeta):

    """
        How to create variable code.
        Interface and Repository version
    """

    @abstractmethod
    async def insert_pdf_docs(self, docs: list[dict[str, str]]):
        raise NotImplementedError()

    @abstractmethod
    async def search_vector_index(self):
        raise NotImplementedError()
