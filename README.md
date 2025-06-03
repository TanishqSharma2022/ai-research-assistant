# An AI-Research Assistant that can get the latest research papers from arxiv.org for NLP, AI, CV and ML Domains 


### Jun 2, 2025

- Made the basic prototype. 
- The pipeline is scraping the latest papers from the arxiv api. 
- Create embeddings from title+abstract. 
- Inference with query and find the top k papers. 
- Added a umap functon to visualize the embeddings.
- Scraped 2000 papers from cs.CL

### Jun 3, 2025

- Added a paginated web scraper. 
- Scraped in total 16k papers info for cs.AI, cs.CV, cs.LG, cs.CL. added v2. 
- did some data cleaning like removing duplicates before creating embeddings (16k to 12.7k ). 
- inspecting clusters with umap. some plotly vis as well.


