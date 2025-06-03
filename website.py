import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb

# --- Setup ---
st.set_page_config(page_title="AI Research Paper Finder", layout="wide")
st.title("🧠 AI Research Paper Assistant")
st.markdown("Ask a question or enter a topic to find relevant papers from arXiv.")

# --- Load ChromaDB and model ---
@st.cache_resource
def load_model_and_db():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(name="arxiv-papers-v2")
    return model, collection

model, collection = load_model_and_db()

# --- Query Handler ---
def search_papers(query, top_k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results

# --- UI Form ---
with st.form("query_form"):
    query = st.text_input("🔎 Enter your research question or topic:", "")
    top_k = st.slider("Number of results:", 1, 10, 5)
    submitted = st.form_submit_button("Search")

# --- Results Display ---
if submitted and query:
    with st.spinner("Searching relevant papers..."):
        results = search_papers(query, top_k=top_k)

    st.markdown(f"### 📄 Top {top_k} Relevant Papers")
    for i in range(len(results["ids"][0])):
        title_abstract = results['documents'][0][i]
        metadata = results['metadatas'][0][i]

        st.markdown(f"#### {i+1}. {metadata['published']} — [{metadata['pdf_url']}]({metadata['pdf_url']})")
        st.write(f"**Title**: {title_abstract.split('.')[0]}")
        # st.write(f"**Authors**: {metadata['authors']}")
        st.write(f"**Abstract Snippet**: {title_abstract[:400]}...")
        st.markdown("---")
