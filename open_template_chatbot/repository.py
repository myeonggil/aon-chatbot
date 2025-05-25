from open_template_chatbot.interfaces.chat_repository_interface import IChatRepository
from open_template_chatbot.interfaces.llm_repository_interface import ILLMRepository




class LLMRepository(ILLMRepository):

    async def insert_pdf_docs(self, docs):
        return await super().insert_pdf_docs(docs)

    async def search_vector_index(self):
        return await super().search_vector_index()
