# =============================================================================
# The Retrieval Chain (The Logic)
# =============================================================================
# This cell wires everything together:
#   Retriever (FAISS)  ➜  Prompt Template  ➜  Local LLM (Llama 3 via Ollama)
#
# The prompt instructs the model to behave like a Reliability Engineer who
# answers ONLY from the provided context and says "Not found in manual" when
# the context doesn't contain the answer.
# =============================================================================


from imports import *   # Centralized imports for the entire project


def build_rag_chain():
    """
    Build and return the complete RAG chain.
    Loads embeddings, FAISS vectorstore, configures the LLM, prompt, and retriever.
    """
    # --- Load the embedding model and FAISS vectorstore ----------------------
    embeddings = get_embedding_model()
    vectorstore = load_vectorstore(embeddings)

    # --- 1. Configuring the local LLM via Ollama ----------------------------
    # Auto-pull the model if it hasn't been downloaded yet.
    MODEL_NAME = "llama3"
    try:
        subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, check=True
        )
    except FileNotFoundError:
        raise RuntimeError(
            "Ollama is not installed. Install it from https://ollama.com and run 'ollama serve'."
        )

    result = subprocess.run(
        ["ollama", "list"], capture_output=True, text=True
    )
    if MODEL_NAME not in result.stdout:
        print(f"Model '{MODEL_NAME}' not found locally. Pulling now (this may take a few minutes)...")
        subprocess.run(["ollama", "pull", MODEL_NAME], check=True)

    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=0,        # Deterministic answers — important for technical docs
    )
    print(f"ChatOllama ({MODEL_NAME}) ready.")

    # --- 2. Building the prompt template ------------------------------------
    # {context} will be filled with the retrieved document chunks.
    # {input}   will be filled with the user's question.
    system_prompt = (
        "You are a Reliability Engineer and Industrial Technical Assistant. "
        "Use the following pieces of retrieved context to answer the question. "
        "Answer based STRICTLY on the context provided. "
        "If the answer is not found in the context, respond with: "
        "'Not found in manual.' "
        "Always be precise and cite relevant details from the context.\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # --- 3. Creating the retrieval chain ------------------------------------
    # a) A "stuff documents" chain that injects retrieved docs into the prompt
    question_answer_chain = create_stuff_documents_chain(llm, prompt)

    # b) A retriever that pulls the top-4 most similar chunks from FAISS
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},    # Return top 4 most relevant chunks
    )

    # c) The full retrieval chain: question → retriever → LLM → answer
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    print("RAG retrieval chain is ready.")
    return rag_chain


# Allow direct execution for testing
if __name__ == "__main__":
    rag_chain = build_rag_chain()