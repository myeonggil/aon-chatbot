import os
import asyncio

from groq import AsyncGroq
from nomic import embed, login
from langchain_core.documents.base import Document

from open_template_chatbot.database.mongodb_cluster import AsyncMongoClient, MONGO_URI
from open_template_chatbot.interfaces.llm_repository_interface import ILLMRepository
from open_template_chatbot.interaction.chatbot_with_gui import ChatbotWithGUI
from open_template_chatbot.interaction.chatops import ChatOps
from open_template_chatbot.repository import llm_repository
from open_template_chatbot.configs import env_config as config
os.environ["TOKENIZERS_PARALLELISM"] = "true"
login(token=config["NOMIC_API_TOKEN"])


class LLMService:
    def __init__(self, llm_repository: ILLMRepository):
        self.llm_repository = llm_repository
        self.client = AsyncGroq(api_key=config["GROQ_API_KEY"])

    def _get_document_from_pdf(self):
        # loader = PyPDFLoader("https://docs.aws.amazon.com/ko_kr/whitepapers/latest/aws-overview/aws-overview.pdf")
        # loader = PyPDFLoader("https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/getting-started-terraform/getting-started-terraform.pdf")
        # data = loader.load()
        # # Split the data into chunks
        # text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
        # documents = text_splitter.split_documents(data)
        # return documents
        pass

    def _make_docs_data(documents: list[Document]) -> list[dict[str, list | str]]:
        # docs_to_insert = [{
        #    "text": doc.page_content,
        #    "embedding": get_embedding(doc.page_content)
        # } for doc in documents]
        # return docs_to_insert
        pass

    # Define a function to generate embeddings
    def _get_embedding(self, data: str, precision: str = "float32") -> list[float | int]:
        # return model.encode(data, precision=precision).tolist()
        response = embed.text([data])
        return response['embeddings'][0]

    async def groq_template_stream(self, query: str):
        await self.llm_repository.get_motor_client(AsyncMongoClient(MONGO_URI))
        embedded_query = self._get_embedding(query)
        context_string = await self.llm_repository.get_context_string_from_docs(
            embedded_query=embedded_query
        )
        prompt = f"""
            You are helpful assistant.

            Remember that you answer a question, you must check to see 
            if it complies with your mission above. If not, you must respond, 
            "I am not able to answer this question". But, you must translate to Korean

            Use the following pieces of context to answer the question at the end.
            {context_string}
            Question: {query}
        """
        # Let's understand how to make chaining chat completion?
        # We can give question and answer to chat completion
        # I think that It look like expect chatbot need to answer as my hope
        # Are messages chat chain?
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Keep all responses under 512 tokens."
                },
                # {
                #     "role": "assistant",
                # },
                {
                    "role": "user",
                    "content": prompt
                },
                # {
                #     "role": "user",
                #     "content": "Please answer smaller than 512 tokens"
                # }
            ],
            stream=True,
            timeout=5,
            temperature=0.05, # more lower focus on consistency, more higher focus on newer answer
            max_tokens=512, # response maximum token length(different by language) Between 512 and 1024
            top_p=1,    # random response match temperature 
            frequency_penalty=0,    # more lower use unique word
            presence_penalty=0  # more lower use similar and repeat word
        )

        # chat mode
        async for chunk in response:
            message = chunk.choices[0].delta.content
            # if message is None:
            #     break
            # data = f"data: {message} \n"
            # yield data.encode()
            if message is not None:
                yield message
            await asyncio.sleep(0.01)
        await self.llm_repository.close()

    async def groq_template_response(self, query: str):
        embedded_query = self._get_embedding(query)
        context_string = await self.llm_repository.get_context_string_from_docs(
            embedded_query=embedded_query)
        prompt = f"""
            You are helpful assistant.

            Remember that you answer a question, you must check to see 
            if it complies with your mission above. If not, you must respond, 
            "I am not able to answer this question". But, you must translate to Korean

            Use the following pieces of context to answer the question at the end.
            {context_string}
            Question: {query}
        """
        # Let's understand how to make chaining chat completion?
        # We can give question and answer to chat completion
        # I think that It look like expect chatbot need to answer as my hope
        # Are messages chat chain?
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Keep all responses under 512 tokens."
                },
                # {
                #     "role": "assistant",
                # },
                {
                    "role": "user",
                    "content": prompt
                },
                # {
                #     "role": "user",
                #     "content": "Please answer smaller than 512 tokens"
                # }
            ],
            stream=False,
            timeout=5,
            temperature=0.05, # more lower focus on consistency, more higher focus on newer answer
            max_tokens=512, # response maximum token length(different by language) Between 512 and 1024
            top_p=1,    # random response match temperature 
            frequency_penalty=0,    # more lower use unique word
            presence_penalty=0  # more lower use similar and repeat word
        )

        if response.choices:
            return response.choices[0].message.content
        else:
            return None

    def run_streamlit(self, chatbot_with_gui: ChatbotWithGUI):
        chatbot_with_gui.start_app(self.groq_template_stream)

    async def run_slack_socket(self, chatops: ChatOps):
        # subscribe message
        try:
            chatops.message(self.groq_template_response)
            await chatops.start_app()
        except Exception as err:
            print(err)
        finally:
            await self.close()

    async def close(self):
        await self.llm_repository.close()


llm_service = LLMService(llm_repository=llm_repository)
