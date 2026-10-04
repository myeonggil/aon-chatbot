
import os
import toml
os.environ["TOKENIZERS_PARALLELISM"] = "true"

# Load the embedding model
# from sentence_transformers import SentenceTransformer
# from langchain_community.document_loaders import PyPDFLoader
# model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)

import re

TERM_MAP = {
    "테라폼": "Terraform",
    "에이더블유에스": "AWS",
    "아마존 웹 서비스": "AWS",
    "쿠버네티스": "Kubernetes",
    "도커": "Docker",
    "람다": "Lambda",
    "이씨투": "EC2",
    "에스쓰리": "S3",
    "브이피씨": "VPC",
    "클라우드포메이션": "CloudFormation",
    "아이에이엠": "IAM",
}

_pattern = re.compile("|".join(map(re.escape, sorted(TERM_MAP, key=len, reverse=True))))


def expand_query(query: str) -> str:
    found = {TERM_MAP[m] for m in _pattern.findall(query)}
    if not found:
        return query
    return f"{query} ({', '.join(sorted(found))})"

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
