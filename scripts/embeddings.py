# scripts/reembed_voyage.py
import time
import voyageai
from pymongo import MongoClient, UpdateOne
from aon_chatbot.configs import config

MONGO_URI = config['MONGO_URI']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
MONGO_URI = MONGO_URI.replace(
    '<username>', USERNAME
).replace(
    '<password>', PASSWORD
)

vo = voyageai.Client(api_key=config["VOYAGE_API_KEY"])
client = MongoClient(MONGO_URI)
col = client["chatbot"]["chat_history"]

MODEL = "voyage-4-lite"
BATCH = 64

docs = list(col.find({}, {"_id": 1, "text": 1}))
print(f"총 {len(docs)}건")

for i in range(0, len(docs), BATCH):
    batch = docs[i:i + BATCH]
    texts = [d["text"] for d in batch]

    res = vo.embed(texts, model=MODEL, input_type="document")

    ops = [
        UpdateOne({"_id": d["_id"]}, {"$set": {"embedding": emb}})
        for d, emb in zip(batch, res.embeddings)
    ]
    col.bulk_write(ops)
    print(f"{i + len(batch)} / {len(docs)} 완료")

    time.sleep(1)  # 결제수단 미등록 시 rate limit 걸리면 늘리기