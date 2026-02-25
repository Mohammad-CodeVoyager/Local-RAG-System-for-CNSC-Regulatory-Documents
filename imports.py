# =============================================================================
# imports.py — Centralized imports for the CNSC RAG Assistant
# =============================================================================
# All libraries used across the project are imported here.
# In your notebook, simply run: from imports import *
# =============================================================================


# --- python libraries --------------
import os
import subprocess, sys
from pathlib import Path

# --- Streamlit ---------------------------------------------------------------
import streamlit as st

# --- LangChain Core ----------------------------------------------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# --- LangChain Chains --------------------------------------------------------
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# --- LangChain Community -----------------------------------------------------
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS

# --- Local LLM (Ollama) ------------------------------------------------------
from langchain_ollama import ChatOllama

# --- Embeddings (HuggingFace, CPU) -------------------------------------------
from langchain_huggingface import HuggingFaceEmbeddings

# --- Path Configuration ------------------------------------------------------
DATA_DIR  = os.path.join(os.getcwd(), "data")        # Folder that holds the PDF(s)
FAISS_DIR = os.path.join(os.getcwd(), "faiss_index") # Where the vector DB is saved

print(f"PDF folder : {DATA_DIR}")
print(f"FAISS index: {FAISS_DIR}")
print("All imports loaded successfully.")

# --- User defined Libraries ------------------------------------------------------
from retrival_chain import build_rag_chain
from text_splitter import load_and_process_pdfs
from model_n_embedding import get_embedding_model, create_vectorstore, save_vectorstore, load_vectorstore
