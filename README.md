# E-commerce-Support-Agent

This is a multi-agent AI system built using **CrewAI**, **ChromaDB**, and **LangChain**. It reads e-commerce policies and processes customer support tickets to generate grounded, policy-backed resolutions with strict hallucination controls.

## 🏗️ Architecture

This system relies on advanced LLMs (Google Gemini) to power the CrewAI agents, combined with a local vector store for fast, reliable, policy-grounded support resolution.

### 🤖 The Agents
There are 4 specialized agents involved in resolving every ticket:
1. **Support Ticket Triage Agent**: Classifies the issue type and detects missing critical information (like order status or delivery date).
2. **Policy Retriever Agent**: Queries the local ChromaDB vector store. It retrieves relevant policy excerpts and their exact source documents.
3. **Resolution Writer Agent**: Drafts the final customer-facing response. It is explicitly prompted to purely rely on the retrieved paragraphs and never invent rules.
4. **Compliance and Safety Auditor**: This is our **No Hallucination Control Mechanism**. The Auditor reviews the final draft. If it detects ungrounded refunds, missing citations, or hallucinated policies, it forces a rewrite or initiates an 'escalation' path.

### 📚 Document Pipeline
- **Ingestion**: The script converts synthetic policy documents into chunked text.
- **Chunking Strategy**: We use `RecursiveCharacterTextSplitter` with a `chunk_size` of `500` and `chunk_overlap` of `50`.
  - *Why?* A chunk size of 500 characters captures specific policy rules (like exceptions for perishable items) without diluting the semantic meaning. The overlap ensures context isn't lost between paragraphs.
- **Embeddings Model**: `sentence-transformers/all-MiniLM-L6-v2` runs locally via HuggingFace Embeddings. 
- **Vector Store**: `Chroma DB` persists the embedded vector data into a local `./chroma_db` folder.
- **Retriever Settings**: We retrieve the top-K most relevant chunks to provide enough context for overarching rules and corner-case exceptions without exceeding the LLM's context window.

---

## 🚀 Getting Started

You will need an environment variable file (`.env`) in the root directory of the project. Depending on which LLM you choose to power the agents, add the corresponding API keys. 

Create a file named `.env` and configure it like this:

```env
# Google Gemini (Primary setup)
GEMINI_API_KEY="your_gemini_key_here"
GOOGLE_API_KEY="your_gemini_key_here"  # LangChain often looks for this specific name

# OpenAI (Optional alternative)
OPENAI_API_KEY="your_openai_key_here"

# Anthropic (Optional alternative)
ANTHROPIC_API_KEY="your_anthropic_key_here"


### 1. Set up the Python Environment
```bash
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
