import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from crewai.tools import BaseTool

class PolicySearchTool(BaseTool):
    name: str = "Search E-commerce Policies"
    description: str = "Look up policies regarding returns, refunds, shipping, promotions, fraud, or final sale terms. Good queries look like 'return policy for electronics' or 'lost package rules'."
    
    def _run(self, query: str) -> str:
        if not os.path.exists("./chroma_db"):
            print("Chroma DB not found! Run ingestion first.", flush=True)
            return "DATABASE MISSING"
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        docs = db.similarity_search(query, k=5)
        
        result = ""
        for d in docs:
            # Enforce [Source | Section] format implicitly in the retrieved text
            source = d.metadata.get("source", "Unknown Policy")
            section = d.metadata.get("section", "General")
            result += f"\n--- [{source} | {section}] ---\n{d.page_content}\n"
        
        if not result.strip():
            return "No relevant information found in the policy docs."
        return result
