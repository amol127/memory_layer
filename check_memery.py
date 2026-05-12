# check_memories.py
from dotenv import load_dotenv
from mem0 import Memory
import os

load_dotenv()
os.environ.pop("OPENAI_API_KEY", None)
OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": "http://localhost:11434",
            "embedding_dims": 768
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4.1-mini",
            "openai_base_url": "https://openrouter.ai/api/v1"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 7000,
            "collection_name": "mem0_nomic",
            "embedding_model_dims": 768
        }
    }
}

mem_client = Memory.from_config(config)

memories = mem_client.get_all(filters={"user_id": "amolsawant"}) 
print(f"Total memories: {len(memories['results'])}")
for m in memories['results']:
    print(f"  ID: {m['id']}")
    print(f"  Memory: {m['memory']}")
    print()