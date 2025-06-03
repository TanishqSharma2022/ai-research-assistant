import requests
import time
import xml.etree.ElementTree as ET
import csv
import os

# =============================
# Configurable Parameters
# =============================
CATEGORIES = ["cs.CL", "cs.LG", "cs.AI", "cs.CV"]     # multiple categories
OUTPUT_CSV = "arxiv_papers_v2.csv"
BATCH_SIZE = 1000                             # max per request = 300
MAX_PER_CATEGORY = 10000                      # set this higher to get more
WAIT_SECONDS = 3                             # respect ArXiv rate limits

# =============================
# Functions
# =============================

def fetch_arxiv(category, start=0, max_results=100):
    url = (
        f"http://export.arxiv.org/api/query?search_query=cat:{category}"
        f"&start={start}&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    response = requests.get(url)
    time.sleep(WAIT_SECONDS)
    return response.text

def parse_response(xml_response):
    root = ET.fromstring(xml_response)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    entries = []
    for entry in root.findall('atom:entry', ns):
        arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
        published = entry.find('atom:published', ns).text.strip()
        pdf_url = None
        for link in entry.findall('atom:link', ns):
            if link.attrib.get('title') == 'pdf':
                pdf_url = link.attrib['href']
        if pdf_url:
            entries.append({
                'id': arxiv_id,
                'title': title,
                'abstract': abstract,
                'published': published,
                'pdf_url': pdf_url
            })
    return entries

def write_to_csv(entries, file_path):
    file_exists = os.path.exists(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'title', 'abstract', 'published', 'pdf_url'])
        if not file_exists:
            writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

# =============================
# Main Loop
# =============================

def scrape_arxiv():
    for category in CATEGORIES:
        print(f"\n== Fetching category: {category} ==")
        for start in range(0, MAX_PER_CATEGORY, BATCH_SIZE):
            try:
                print(f"Fetching {start}–{start + BATCH_SIZE}...")
                xml_data = fetch_arxiv(category, start=start, max_results=BATCH_SIZE)
                entries = parse_response(xml_data)
                if not entries:
                    print("No more results.")
                    break
                write_to_csv(entries, OUTPUT_CSV)
            except Exception as e:
                print(f"Error occurred: {e}")
                break

if __name__ == "__main__":
    scrape_arxiv()
