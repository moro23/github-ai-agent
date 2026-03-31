import chromadb
from chromadb.utils import embedding_functions
import json
import os

class SearchEngine:
    def __init__(self, collection_name="sklearn_docs"):
        # 1. Initialize local persistent DB
        self.client = chromadb.PersistentClient(path="./data/vector_db")
        
        # 2. Use a local embedding model (no API costs/rate limits)
        # 'all-MiniLM-L6-v2' is fast and very accurate for docs
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embed_fn
        )

    def index_chunks(self, chunks_path):
        """Only index if the collection is empty"""
        if self.collection.count() > 0:
            print(f"Collection already contains {self.collection.count()} chunks.")
            return

        with open(chunks_path, 'r') as f:
            chunks = json.load(f)

        print(f"Indexing {len(chunks)} chunks into Vector DB...")
        
        # Chroma expects lists of strings, ids, and metadatas
        documents = [c['content'] for c in chunks]
        metadatas = [c['metadata'] for c in chunks]
        ids = [f"chunk_{i}" for i in range(len(chunks))]

        # Process in batches of 100 to be safe
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )
        print("Indexing complete.")

    def search(self, query, n_results=5):
        """
        Performs semantic search. 
        Note: Chroma handles the hybrid aspect (Vector + Metadata filtering)
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results