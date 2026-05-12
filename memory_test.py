# from dotenv import load_dotenv
# from mem0 import Memory

# from openai import OpenAI
# import os
# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY")
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# print("KEY =", OPENAI_API_KEY)
# client = OpenAI(  
    
#     api_key=OPENAI_API_KEY,
#     base_url="https://openrouter.ai/api/v1")



# config = {
#     "version":"v1.1",
#     "embedder":{
#         "provider": "ollama",
#         "config": {
#             "model": "nomic-embed-text",
#             "ollama_base_url": "http://localhost:11434",
#             "embedding_dims": 768 
#         }
#     },
#     "llm":{
#         "provider": "openai",
#         "config": {
#             "api_key": OPENAI_API_KEY,
#             "model": "gpt-4.1-mini"
#         }
#     },
#     "vector_store":{
#         "provider":"qdrant",
#         "config":{
#             "host":"localhost",
#             "port":7000,
#             "collection_name": "mem0_nomic"
#         }
#     }
# }


# mem_client = Memory.from_config(config)


# from dotenv import load_dotenv
# from mem0 import Memory
# from openai import OpenAI
# import os
# import json

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY")

# # ❌ Remove this line - it causes Mem0 to default to OpenAI embedder
# # os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# # ✅ Unset it in case it was set by dotenv or system
# os.environ.pop("OPENAI_API_KEY", None)

# client = OpenAI(
#     api_key=OPENAI_API_KEY,
#     base_url="https://openrouter.ai/api/v1"
# )

# config = {
#     "version": "v1.1",
#     "embedder": {
#         "provider": "ollama",
#         "config": {
#             "model": "nomic-embed-text",
#             "ollama_base_url": "http://localhost:11434",
#             "embedding_dims": 768
#         }
#     },
#     "llm": {
#         "provider": "openai",
#         "config": {
#             "api_key": OPENAI_API_KEY,
#             "model": "gpt-4.1-mini",
#             "openai_base_url": "https://openrouter.ai/api/v1"
#         }
#     },
#     "vector_store": {
#         "provider": "qdrant",
#         "config": {
#             "host": "localhost",
#             "port": 7000,
#             "collection_name": "mem0_nomic",
#             "embedding_model_dims": 768
#         }
#     }
# }

# mem_client = Memory.from_config(config)
# while True:
#     user_query = input(">>")

#     search_memory = mem_client.search(query=user_query, filters={"user_id": "amolsawant"})
#     memory_about_user = search_memory

#     memories = [
#         f"ID : {mem.get('id')}\nMemory: {mem.get('memory')}" for mem in search_memory.get("results")
#     ]
#     print("Found Memories", memories)
#     SYSTEM_PROMPTING = f"""
#             Here is the context about the user:
#             {json.dumps(memories)}
#         """
    
#     response = client.chat.completions.create(
#         model="openai/gpt-4.1-mini",
#         messages=[
#             {"role":"system", "content":SYSTEM_PROMPTING},
#             {"role":"user", "content":user_query}
#         ],
#         max_tokens=200
#     )

#     ai_response = response.choices[0].message.content

#     print("AI >",ai_response)

#     mem_client.add(
#         user_id = "amolsawant",
#         messages = [
            
#             {"role":"user", "content":user_query},
#             {"role":"assistant", "content":ai_response}
#         ]

#     )

#     print("Memory has been Saved")




# # # reset_qdrant.py
# # from qdrant_client import QdrantClient

# # client = QdrantClient(host="localhost", port=7000)

# # client.delete_collection("mem0_nomic")
# # client.delete_collection("mem0migrations")
# # print("✅ Both collections deleted. Now re-run memory_test.py")



from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY")
os.environ.pop("OPENAI_API_KEY", None)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

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

USER_ID = "amolsawant"
mem_client = Memory.from_config(config)


def clean_contradictions(query, threshold=0.3):
    """Delete old memories that are similar to the new input."""
    results = mem_client.search(query=query, filters={"user_id": USER_ID})
    deleted = []
    for mem in results.get("results", []):
        if mem["score"] >= threshold:
            mem_client.delete(mem["id"])
            deleted.append(mem["memory"])
            print(f"🗑️  Deleted: {mem['memory']}")
    return deleted


while True:
    user_query = input(">> ")

    # Search existing memories for context
    search_memory = mem_client.search(query=user_query, filters={"user_id": USER_ID})
    memories = [
        f"ID: {m.get('id')}\nMemory: {m.get('memory')}"
        for m in search_memory.get("results", [])
    ]
    print("Found Memories:", memories)

    SYSTEM_PROMPT = f"""
        You are a helpful assistant. Here is what you know about the user:
        {json.dumps(memories)}
        Always use the most recent information about the user.
    """

    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        max_tokens=200
    )
    ai_response = response.choices[0].message.content
    print("AI >", ai_response)

    # ✅ Delete contradicted memories BEFORE saving new one
    clean_contradictions(user_query)

    mem_client.add(
        user_id=USER_ID,
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )
    print("Memory has been Saved")