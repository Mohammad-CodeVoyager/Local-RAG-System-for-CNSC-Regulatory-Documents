from imports import *   

# =============================================================================
# Cell 3: Vector Database (The Brain)
# =============================================================================
# This cell converts text chunks into numerical vectors (embeddings) and stores
# them in a FAISS index.  FAISS lets us do lightning-fast similarity search so
# the retriever can find the most relevant passages for any question.
#
# The index is saved to disk — on subsequent runs you can reload it instead of
# re-embedding everything (saves time when the PDF hasn't changed).
# =============================================================================

# --- Initialize the embedding model ------------------------------------------
# "all-MiniLM-L6-v2" is a small, fast, CPU-friendly sentence-transformer.
def get_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},          # Explicitly use CPU
    )
    print("Embedding model loaded (all-MiniLM-L6-v2 on CPU).")
    return embeddings


def create_vectorstore(chunks, embeddings):
    # --- Convert text chunks into vectors and build the FAISS index ---------------
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print(f"FAISS vector store created with {vectorstore.index.ntotal} vectors.")
    return vectorstore

def save_vectorstore(vectorstore):
    vectorstore.save_local(FAISS_DIR)
    print(f"FAISS index saved to '{FAISS_DIR}'.")