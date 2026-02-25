# =============================================================================
# app.py — Streamlit UI for the CNSC RAG Assistant
# =============================================================================
# Launch with:  streamlit run app.py
# Prerequisites:
#   1. FAISS index built (run: python vector_database_creator.py)
#   2. Ollama running (ollama serve) with llama3 pulled (ollama pull llama3)
# =============================================================================
from imports import *   # Centralized imports for the entire project
from imports import *   # Centralized imports for the entire project


# --- Auto-install dependencies from requirements.txt if missing --------------
_req_path = Path(__file__).with_name("requirements.txt")
if _req_path.exists():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(_req_path)]
    )

# --- Import the chain builder from retrival_chain.py -------------------------
from retrival_chain import build_rag_chain


# --- Cache the RAG chain so it loads once and persists across reruns ----------
@st.cache_resource(show_spinner="Loading RAG pipeline (embeddings + FAISS + LLM)…")
def get_rag_chain():
    return build_rag_chain()


# =============================================================================
# Streamlit UI
# =============================================================================
def main():
    st.set_page_config(
        page_title="CNSC RAG Assistant",
        page_icon="🔬",
        layout="wide",
    )

    # --- Header --------------------------------------------------------------
    st.title("🔬 CNSC REGDOC-2.6.1 — RAG Assistant")
    st.caption(
        "Ask plain-language questions about CNSC Reliability Programs. "
        "Answers are grounded **strictly** in the uploaded regulatory documents."
    )

    # --- Load chain (cached after first call) --------------------------------
    rag_chain = get_rag_chain()

    # --- Sidebar info --------------------------------------------------------
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown(
            "- **Model:** Llama 3 (local via Ollama)\n"
            "- **Embeddings:** all-MiniLM-L6-v2 (CPU)\n"
            "- **Vector DB:** FAISS\n"
            "- **Documents:** CNSC REGDOC-2.6.1"
        )
        st.divider()
        st.markdown("**Sample questions:**")
        st.markdown(
            "- What is the purpose of a reliability program?\n"
            "- What does REGDOC-2.6.1 say about safety system testing?\n"
            "- Define reliability targets for safety-important systems.\n"
            "- What are the reporting requirements?"
        )

    # --- Chat history --------------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- User input ----------------------------------------------------------
    if question := st.chat_input("Ask a question about CNSC REGDOC-2.6.1…"):
        # Show user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Run the RAG chain
        with st.chat_message("assistant"):
            with st.spinner("Searching documents & generating answer…"):
                result = rag_chain.invoke({"input": question})

            # --- Answer ------------------------------------------------------
            answer = result["answer"]
            st.markdown(answer)

            # --- Source citations --------------------------------------------
            sources_seen = set()
            citations = []
            for doc in result["context"]:
                source_file = os.path.basename(doc.metadata.get("source", "Unknown"))
                page_num = doc.metadata.get("page", "N/A")
                page_display = page_num + 1 if isinstance(page_num, int) else page_num
                citation = f"{source_file}, Page {page_display}"
                if citation not in sources_seen:
                    sources_seen.add(citation)
                    citations.append(citation)

            if citations:
                with st.expander("📄 Source Citations"):
                    for c in citations:
                        st.markdown(f"- {c}")

            # Build full response for chat history
            full_response = answer
            if citations:
                full_response += "\n\n**Sources:** " + " · ".join(citations)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )


if __name__ == "__main__":
    main()
