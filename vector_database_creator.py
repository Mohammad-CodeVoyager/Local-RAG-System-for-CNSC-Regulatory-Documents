import importlib
import subprocess
import sys
from pathlib import Path


def load_project_imports():
	requirements_path = Path(__file__).with_name("requirements.txt")

	try:
		return importlib.import_module("imports")
	except ModuleNotFoundError as missing_module_error:
		if not requirements_path.exists():
			raise RuntimeError(
				"Missing dependencies and requirements.txt was not found. "
				"Please install packages manually."
			) from missing_module_error

		print(
			f"Missing dependency detected ({missing_module_error.name}). "
			"Installing requirements..."
		)
		subprocess.check_call(
			[sys.executable, "-m", "pip", "install", "-r", str(requirements_path)]
		)
		return importlib.import_module("imports")


_imports_module = load_project_imports()
globals().update({name: value for name, value in vars(_imports_module).items() if not name.startswith("_")})


# =============================================================================
# main.py — Orchestrates the entire RAG pipeline
# =============================================================================
# This is the main script that ties everything together. It:
# 1. Loads and processes PDFs into text chunks.
# 2. Creates or loads the FAISS vector database of embeddings.
# 3. Sets up the retriever and the LLM for question-answering.          
# 4. Provides a simple interface to ask questions and get answers based on the
#    content of the PDFs.
# =============================================================================

chunks = load_and_process_pdfs()  
embeddings = get_embedding_model()  
vectorstore = create_vectorstore(chunks, embeddings)  
save_vectorstore(vectorstore) 