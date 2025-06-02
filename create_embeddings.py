from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from tqdm import tqdm
import csv

# Load papers from CSV
def load_papers_from_csv(filename="arxiv_papers.csv"):
    papers = []
    with open(filename, "r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            papers.append({
                "title": row["title"],
                "abstract": row["abstract"],
                "metadata": {
                    "authors": row["authors"],
                    "published": row["published"],
                    "pdf_url": row["pdf_url"]
                }
            })
    return papers

# 1. Load papers
papers = load_papers_from_csv()

# 2. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast and decent

# 3. Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="arxiv-papers")

# 4. Embed and insert into ChromaDB
for i, paper in enumerate(tqdm(papers, desc="📦 Embedding and Storing")):
    doc_id = f"paper_{i}"
    content = f"{paper['title']} {paper['abstract']}"
    embedding = model.encode(content).tolist()
    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[paper["metadata"]]
    )

client.heartbeat()
print("✅ All papers embedded and stored in ChromaDB!")
