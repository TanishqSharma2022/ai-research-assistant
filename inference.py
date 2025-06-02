from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Load ChromaDB and embedding model
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="arxiv-papers")
model = SentenceTransformer("all-MiniLM-L6-v2")

def query_papers(prompt, top_k=5):
    # Embed the prompt
    query_embedding = model.encode(prompt).tolist()

    # Search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Format results
    for i in range(len(results["ids"][0])):
        print(f"\n🔹 Result {i+1}")
        print(f"Title     : {results['documents'][0][i][:100]}...")
        print(f"Authors   : {results['metadatas'][0][i]['authors']}")
        print(f"Published : {results['metadatas'][0][i]['published']}")
        print(f"PDF       : {results['metadatas'][0][i]['pdf_url']}")


if __name__ == "__main__":
    query = "state-of-the-art transformer models for named entity recognition"
    query_papers(query, top_k=3)
