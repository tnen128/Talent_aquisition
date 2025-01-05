import re
import tiktoken  # for text splitting if you want more control, or you can use LangChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

# Example: stella_en_400M_v5 (or replace with your local model path)
EMBEDDING_MODEL = "YourLocalPath/stella_en_400M_v5"

# Connect to Milvus
connections.connect(alias="default", host="milvus", port="19530")

# Define a schema for the CV embeddings
fields = [
    FieldSchema(name="pk_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768), # adjust dimension
    FieldSchema(name="text_chunk", dtype=DataType.VARCHAR, max_length=65535),
]
schema = CollectionSchema(fields, "CV embeddings")
collection_name = "cv_collection"
if collection_name not in connections.get_connection_addr("default"):
    cv_collection = Collection(name=collection_name, schema=schema)
else:
    cv_collection = Collection(collection_name)

# Create an embeddings object
hf_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def chunk_text(text: str, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    return chunks

def embed_and_store(text: str):
    # 1. Chunk text
    chunks = chunk_text(text)

    # 2. Create embeddings for each chunk
    chunk_embeddings = []
    chunk_texts = []
    for chunk in chunks:
        emb = hf_embeddings.embed_documents([chunk])[0]
        chunk_embeddings.append(emb)
        chunk_texts.append(chunk)

    # 3. Insert into Milvus
    cv_collection.insert(
        [
            chunk_embeddings,
            chunk_texts,
        ]
    )
    # You might need to call flush or load
    cv_collection.flush()
    return len(chunks)

