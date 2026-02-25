# 🔬 Local RAG System for CNSC Regulatory Documents

AI-powered RAG chatbot that enables engineers to query CNSC REGDOC-2.6.1 regulatory documents using plain-language questions and receive precise, cited answers in real time. Hosted **100% locally** for security and privacy — no data leaves your machine.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-🦜-green)
![Ollama](https://img.shields.io/badge/LLM-Llama_3_(Ollama)-purple)
![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the App](#running-the-app)
- [Architecture](#architecture)
- [Key Components](#key-components)
- [Troubleshooting](#troubleshooting)

---

## How It Works

1. **PDF Ingestion** — Loads CNSC regulatory PDFs from the `data/` folder.
2. **Text Chunking** — Splits pages into overlapping 1000-character chunks for precise retrieval.
3. **Embedding** — Converts chunks into vector embeddings using `all-MiniLM-L6-v2` (runs on CPU, no API key).
4. **Vector Store** — Stores embeddings in a FAISS index for lightning-fast similarity search.
5. **Retrieval + LLM** — When you ask a question, the top-4 most relevant chunks are retrieved and fed to Llama 3 (running locally via Ollama), which generates a grounded answer with citations.

---

## Project Structure

```
Local-RAG-System-for-CNSC-Regulatory-Documents/
├── app.py                      # Streamlit UI (entry point)
├── imports.py                  # Centralized imports for the project
├── text_splitter.py            # PDF loading & text chunking
├── model_n_embedding.py        # Embedding model & FAISS vectorstore utilities
├── retrival_chain.py           # RAG chain: retriever → prompt → LLM
├── vector_database_creator.py  # One-time script to build the FAISS index
├── requirements.txt            # Python dependencies
├── data/                       # Drop your CNSC PDFs here
│   └── *.pdf
└── faiss_index/                # Auto-generated FAISS vector database
    ├── index.faiss
    └── index.pkl
```

---

## Prerequisites

| Requirement | Details |
|---|---|
| **Python** | 3.10+ (Conda recommended) |
| **Ollama** | Install from [ollama.com](https://ollama.com) |
| **Llama 3** | Auto-pulled on first run, or manually: `ollama pull llama3` |
| **PDFs** | Place CNSC regulatory documents in the `data/` folder |

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Mohammad-CodeVoyager/Local-RAG-System-for-CNSC-Regulatory-Documents.git
cd Local-RAG-System-for-CNSC-Regulatory-Documents
```

### 2. Create a Python environment (recommended)

```bash
conda create -n rag_project python=3.10 -y
conda activate rag_project
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Dependencies are also auto-installed when you run `app.py` for the first time.

### 4. Start Ollama

```bash
ollama serve
```

> Keep this running in a separate terminal. The app will auto-pull `llama3` if it's not already downloaded.

### 5. Build the FAISS index (one-time)

```bash
python vector_database_creator.py
```

This reads all PDFs from `data/`, chunks them, creates embeddings, and saves the FAISS index to `faiss_index/`. You only need to re-run this if you add or change PDFs.

---

## Running the App

```bash
streamlit run app.py
```

The app opens in your browser at **http://localhost:8501**. Type a question and get an answer grounded in the PDFs, with source citations.

> ⚠️ Do **not** run with `python app.py` — Streamlit requires its own runtime.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   OFFLINE (run once)                    │
│                                                         │
│  📂 data/*.pdf                                          │
│       │                                                 │
│       ▼                                                 │
│  text_splitter.py ──→ chunks (1000 chars, 200 overlap)  │
│       │                                                 │
│       ▼                                                 │
│  model_n_embedding.py ──→ FAISS index (faiss_index/)    │
│                                                         │
└─────────────────────────────────────────────────────────┘
                          │
                    load_vectorstore()
                          │
┌─────────────────────────▼───────────────────────────────┐
│                  ONLINE (every query)                    │
│                                                         │
│  👤 User Question (Streamlit UI)                        │
│       │                                                 │
│       ▼                                                 │
│  FAISS Retriever ──→ Top 4 relevant chunks              │
│       │                                                 │
│       ▼                                                 │
│  Prompt Template (Reliability Engineer persona)         │
│       │                                                 │
│       ▼                                                 │
│  Llama 3 via Ollama (temperature=0)                     │
│       │                                                 │
│       ▼                                                 │
│  💬 Answer + Source Citations                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Key Components

| File | Purpose |
|---|---|
| **`app.py`** | Streamlit chat interface with session history, sidebar, and source citations |
| **`imports.py`** | Single place for all library imports — avoids duplication across files |
| **`text_splitter.py`** | `load_and_process_pdfs()` — loads PDFs and splits into retrieval-friendly chunks |
| **`model_n_embedding.py`** | `get_embedding_model()`, `create_vectorstore()`, `load_vectorstore()`, `save_vectorstore()` |
| **`retrival_chain.py`** | `build_rag_chain()` — assembles the full retriever → prompt → LLM pipeline |
| **`vector_database_creator.py`** | Orchestrates the one-time index build: load → chunk → embed → save |

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `model 'llama3' not found (404)` | Run `ollama pull llama3` or make sure `ollama serve` is running |
| `FAISS index not found` | Run `python vector_database_creator.py` to build the index |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Session state does not function` | Use `streamlit run app.py`, not `python app.py` |
| Slow first query | Normal — the embedding model loads once on first run, then is cached |

---

## License

This project is for educational and internal use. CNSC regulatory documents are publicly available from the [Canadian Nuclear Safety Commission](https://nuclearsafety.gc.ca).
