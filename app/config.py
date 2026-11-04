import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def get_client():
    from openai import OpenAI
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("请在 .env 中配置 DEEPSEEK_API_KEY；检索评估不需要 Key")
    return OpenAI(api_key=key, base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"), timeout=60, max_retries=0)
