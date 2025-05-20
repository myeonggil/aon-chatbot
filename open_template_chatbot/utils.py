from huggingface_hub import login
from sentence_transformers import SentenceTransformer
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_core.documents.base import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from open_template_chatbot.configs import env_config as config

import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"
login(token=config["HUGGINGFACE_TOKEN"])

# Load the embedding model
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)

# Define a function to generate embeddings
def get_embedding(data: str, precision="float32") -> list[float | int]:
   return model.encode(data, precision=precision).tolist()


# def get_document_from_pdf():
#     # Load the PDF
#     # AWS cloud
#     loader = PyPDFLoader("https://docs.aws.amazon.com/ko_kr/whitepapers/latest/aws-overview/aws-overview.pdf")
#     data = loader.load()
#     # Split the data into chunks
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
#     documents = text_splitter.split_documents(data)
#     return documents


# def make_docs_data(documents: list[Document]) -> list[dict[str, list | str]]:
#     docs_to_insert = [{
#         "text": doc.page_content,
#         "embedding": get_embedding(doc.page_content)
#     } for doc in documents]
#     return docs_to_insert
