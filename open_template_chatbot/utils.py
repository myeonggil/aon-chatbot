
import os
import toml
os.environ["TOKENIZERS_PARALLELISM"] = "true"

# Load the embedding model
# from sentence_transformers import SentenceTransformer
# from langchain_community.document_loaders import PyPDFLoader
# model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)


def update_streamlit_config(
    browser_gatherUsageStats: bool,
    server_headless: bool,
    server_enableXsrfProtection: bool,
    server_enableCORS: bool,
    server_address: str,
    server_port: int,
):
    if not os.path.isdir("./.streamlit"):
        os.mkdir('./.streamlit')
    with open('./.streamlit.default/config.toml', 'rb') as f:
        config = toml.loads(f.read().decode())
        config['browser']['gatherUsageStats'] = browser_gatherUsageStats
        config['server'] = {
            'headless': server_headless,
            'enableXsrfProtection': server_enableXsrfProtection,
            'enableCORS': server_enableCORS,
            'address': server_address,
            'port': server_port
        }
    with open('./.streamlit/config.toml', 'w') as f:
        _ = toml.dump(config, f)
