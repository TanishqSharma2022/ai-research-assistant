import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

# 1. Load and clean CSV using Pandas
def load_and_clean_papers(filename="arxiv_papers_v2.csv"):
    df = pd.read_csv(filename)
    df = df.drop_duplicates(subset="id")  # remove duplicates by ID
    df = df.dropna(subset=["title", "abstract"])  # optional: remove empty rows
    return df

# 2. Load the data
df = load_and_clean_papers()

# 3. Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="arxiv-papers-v2")

# 5. Embed and insert into ChromaDB
for i, row in tqdm(df.iterrows(), total=len(df), desc="📦 Embedding and Storing"):
    doc_id = f"paper_{row['id']}"  # use ArXiv ID directly to avoid overwriting
    content = f"{row['title']} {row['abstract']}"
    embedding = model.encode(content).tolist()
    
    # Metadata
    metadata = {
        "id": row["id"],
        "published": row.get("published", ""),
        "pdf_url": row.get("pdf_url", "")
    }
    
    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata]
    )

client.heartbeat()
print("✅ All unique papers embedded and stored in ChromaDB!")
