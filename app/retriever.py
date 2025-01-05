from pymilvus import connections, Collection
from langchain.embeddings import HuggingFaceEmbeddings

EMBEDDING_MODEL = "YourLocalPath/stella_en_400M_v5"
hf_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
connections.connect(alias="default", host="milvus", port="19530")

collection_name = "cv_collection"
cv_collection = Collection(collection_name)

def retrieve_relevant_chunks(query: str, top_k=5):
    # 1. Embed query
    query_emb = hf_embeddings.embed_query(query)

    # 2. Milvus search
    results = cv_collection.search(
        data=[query_emb],
        anns_field="embedding",
        param={"metric_type": "IP", "params": {"nprobe": 10}},
        limit=top_k,
        output_fields=["text_chunk"]
    )

    # 3. Return best matched chunks
    best_chunks = []
    if results:
        for hit in results[0]:
            best_chunks.append(hit.entity.get("text_chunk"))
    return best_chunks
    