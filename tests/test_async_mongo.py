import pytest

from open_template_chatbot.database.mongodb_cluster import MongoDBCluster
from open_template_chatbot.utils import get_document_from_pdf, make_docs_data


@pytest.mark.asyncio(loop_scope='function')
async def test_create_search_intex():
    pass


@pytest.mark.asyncio(loop_scope='function')
async def test_insert_docs():
    # mongo_cluster = MongoDBCluster()
    # assert mongo_cluster.client.is_primary == True

    # # How to verify?
    # documents = get_document_from_pdf()
    # assert len(documents) > 0

    # # How to verify?
    # docs_to_insert = make_docs_data(documents=documents)
    # assert len(docs_to_insert) > 0

    # result = await mongo_cluster._create_rag_documents(documents=docs_to_insert)
    # assert len(result.inserted_ids) > 0
    pass
