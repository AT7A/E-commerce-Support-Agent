import os
import urllib.request
import markdownify
from bs4 import BeautifulSoup
from langchain_text_splitters import MarkdownTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def run_ingestion():
    html_dir = "data/html"
    if not os.path.exists(html_dir):
        print("Error: Mock data not found. Run generate_mock_data.py first.")
        return

    # 1. Gather URLs
    import pathlib
    files = os.listdir(html_dir)
    urls = [pathlib.Path(os.path.abspath(os.path.join(html_dir, f))).as_uri() for f in files if f.endswith('.html')]

    documents = []
    
    # 2. Ingest
    for url in urls:
        try:
            req = urllib.request.urlopen(url)
            html_content = req.read().decode('utf-8')
            soup = BeautifulSoup(html_content, "html.parser")
            title = soup.title.string if soup.title else os.path.basename(url)
            article = soup.find('article') or soup.find('body')
            md_text = markdownify.markdownify(str(article), heading_style="ATX")
            
            documents.append({
                "page_content": md_text,
                "metadata": {"source": url, "title": title}
            })
        except Exception as e:
            print(f"Error reading {url}: {e}")

    # 3. Chunking
    text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=150)
    
    chunks = []
    metadatas = []
    for doc in documents:
        splits = text_splitter.split_text(doc["page_content"])
        for idx, split in enumerate(splits):
            section = "General"
            for line in split.split('\n'):
                if line.startswith("#"):
                    section = line.replace("#", "").strip()
                    break
            
            chunks.append(split)
            metadatas.append({
                "source": doc["metadata"]["title"],
                "section": section,
                "url": doc["metadata"]["source"]
            })

    # 4. Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db_dir = "./chroma_db"
    
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=db_dir
    )
    
    print("Ingestion complete. Vector store saved to", db_dir)

if __name__ == "__main__":
    run_ingestion()
