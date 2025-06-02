import time
import feedparser
from typing import List, Dict

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_arxiv_papers(
    category: str = "cs.CL",
    max_results: int = 10,
    start_index: int = 0,
    sort_by: str = "submittedDate",
    sort_order: str = "descending"
) -> List[Dict]:
    """
    Fetches metadata for recent papers from arXiv using its public API.

    Returns:
        List of dicts with keys: title, authors, abstract, pdf_url, published, arxiv_id, categories
    """
    query = (
        f"{ARXIV_API_URL}?search_query=cat:{category}"
        f"&start={start_index}&max_results={max_results}"
        f"&sortBy={sort_by}&sortOrder={sort_order}"
    )

    print(f"Fetching: {query}")
    feed = feedparser.parse(query)
    papers = []

    for entry in feed.entries:
        arxiv_id = entry.id.split('/abs/')[-1]
        pdf_link = None
        for link in entry.links:
            if link.rel == 'related' and 'pdf' in link.type:
                pdf_link = link.href

        paper = {
            "title": entry.title.strip().replace('\n', ' '),
            "authors": [author.name for author in entry.authors],
            "abstract": entry.summary.strip().replace('\n', ' '),
            "pdf_url": pdf_link or f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            "published": entry.published,
            "arxiv_id": arxiv_id,
            "categories": entry.tags[0]['term'] if entry.tags else category
        }

        papers.append(paper)
        time.sleep(0.1)  # Safety delay (optional)

    return papers

import csv
from tqdm import tqdm  # <- for progress bars

def save_papers_to_csv(papers, filename="arxiv_papers.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "authors", "published", "pdf_url", "abstract"])
        writer.writeheader()
        for paper in tqdm(papers, desc="💾 Saving papers to CSV"):
            writer.writerow({
                "title": paper["title"],
                "authors": ", ".join(paper["authors"]),
                "published": paper["published"],
                "pdf_url": paper["pdf_url"],
                "abstract": paper["abstract"]
            })
    print(f"\n✅ Saved {len(papers)} papers to {filename}")

def load_papers_from_csv(filename="arxiv_papers.csv"):
    papers = []
    with open(filename, "r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in tqdm(reader, desc="📥 Loading papers from CSV"):
            papers.append({
                "title": row["title"],
                "authors": row["authors"].split(", "),
                "published": row["published"],
                "pdf_url": row["pdf_url"],
                "abstract": row["abstract"]
            })
    print(f"\n📄 Loaded {len(papers)} papers from {filename}")
    return papers

# Example usage
if __name__ == "__main__":
    papers = fetch_arxiv_papers(category="cs.CL", max_results=2000)
    save_papers_to_csv(papers)
    loaded = load_papers_from_csv()
