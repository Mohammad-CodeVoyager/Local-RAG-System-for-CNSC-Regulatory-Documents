# =============================================================================
# app.py — Streamlit UI for the CNSC RAG Assistant
# =============================================================================
# Launch with:  streamlit run app.py
# Prerequisites:
#   1. FAISS index built (run: python vector_database_creator.py)
#   2. Ollama running (ollama serve) with llama3 pulled (ollama pull llama3)
# =============================================================================

from retrival_chain import build_rag_chain
from imports import *   # Centralized imports for the entire project


# --- Auto-install dependencies from requirements.txt if missing --------------
_req_path = Path(__file__).with_name("requirements.txt")
if _req_path.exists():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(_req_path)]
    )



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
    st.title("🔬 CNSC Regulatory Documents — RAG Assistant")
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
        )
        st.divider()
        st.markdown("**📂 Loaded Documents:**")
        st.markdown(
            "1. REGDOC-2-6-1 — Reliability Programs for Nuclear Power Plants\n"
            "2. CAT-304\n"
            "3. 2364f-tg000 (EN)\n"
            "4. Safety Manual for Fanuc Educational Cell"
        )
        st.divider()
        st.markdown("**💡 Try a question:**")
        sample_questions = [
            "What is the purpose of a reliability program?",
            "What does REGDOC-2.6.1 say about safety system testing?",
            "What safety procedures apply to the Fanuc educational cell?",
            "What are the reporting requirements?",
            "Summarize the key points of CAT-304.",
            "What are reliability targets for safety-important systems?",
        ]
        for q in sample_questions:
            if st.button(q, use_container_width=True):
                st.session_state["_sample_q"] = q

    # --- Chat history --------------------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- User input ----------------------------------------------------------
    # Pick up a sample question if one was clicked, otherwise use chat input
    question = st.session_state.pop("_sample_q", None) or st.chat_input("Ask a question about the loaded documents…")

    if question:
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
