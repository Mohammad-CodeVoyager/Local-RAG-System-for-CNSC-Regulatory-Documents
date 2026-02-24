from imports import *
# =============================================================================
# text_splitter.py — Load PDFs and split them into chunks for retrieval
# =============================================================================  
# 1. Verify the data folder exists.
# 2. Load every PDF inside it (PyPDFDirectoryLoader keeps page metadata).
# 3. Split loaded pages into smaller text chunks so the retriever can find
#    precise passages instead of returning full pages.
# =============================================================================
def load_and_process_pdfs():
    # --- Safety check: make sure the data folder is there ------------------------
    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError(f"'{DATA_DIR}' not found. Create it and drop your PDFs inside.")

    # --- Load all PDFs from the data/ folder -------------------------------------
    loader = PyPDFDirectoryLoader(DATA_DIR)
    raw_documents = loader.load()   # Each element = one page with metadata (source, page)
    print(f"Loaded {len(raw_documents)} pages from PDFs in '{DATA_DIR}'.")

    # --- Split pages into smaller, overlapping chunks ----------------------------
    # chunk_size  = 1000 chars → keeps enough context for an industrial paragraph
    # overlap     = 200 chars  → prevents cutting a sentence in half between chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(raw_documents)

    print(f"Split {len(raw_documents)} pages into {len(chunks)} chunks.")
    print(f"Example chunk (first 200 chars):\n{chunks[0].page_content[:200]}...")

    return chunks

