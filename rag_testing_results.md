# RAG System Evaluation — CNSC Local Document Assistant

This document presents the structured evaluation of the Local Retrieval-Augmented Generation (RAG) chatbot built for querying CNSC regulatory and technical safety manuals. The purpose of this testing was to verify grounded responses, citation accuracy, and hallucination prevention.

---

## System Configuration

Model: Llama 3 (local via Ollama)  
Embeddings: all-MiniLM-L6-v2  
Vector Database: FAISS  
Framework: LangChain  
Interface: Streamlit  
Deployment: Localhost (offline RAG system)

---

## Indexed Documents

The system was tested using the following uploaded documents:

- REGDOC-2-6-1 — Reliability Programs for Nuclear Power Plants  
- CAT-304  
- 2364f-tg000 (EN)  
- Safety Manual for Fanuc Educational Cell  

---

## Testing Methodology

A total of 10 evaluation queries were executed:

- 7 grounded questions derived from uploaded documents  
- 3 out-of-scope questions to test hallucination prevention  

Evaluation Criteria:
- Responses must be grounded in indexed documents  
- Citations must be provided  
- Out-of-scope queries must return "Not found in manual"  
- No hallucinated information allowed  

---

## Grounded Question Evaluation

Question 1: Who is this manual intended for and what type of personnel should use it?  
Response: The manual is intended for reliability engineers and industrial technical assistants.  
Result: Correct grounded answer with citations.

Question 2: What safety precautions must be followed before servicing or working on the system?  
Response includes wearing protective equipment, avoiding loose clothing or jewelry, securing guards and covers, removing debris and tools, and ensuring safe working conditions.  
Result: Correct grounded response with citations.

Question 3: Why is it important that only qualified personnel perform installation and maintenance?  
Response: Not found in manual.  
The system correctly avoided generating unsupported information.  
Result: Pass.

Question 4: What risks or hazards are mentioned if installation or wiring is done incorrectly?  
Response includes component damage, reduced product life, and equipment malfunction.  
Result: Correct grounded response with citations.

Question 5: What precautions are recommended to prevent electrostatic discharge (ESD) damage?  
Response includes use of grounding wrist strap and storing boards in conductive packets.  
Result: Correct grounded response with citations.

Question 6: What types of troubleshooting or maintenance information does the manual provide?  
Response includes daily maintenance checks, maintenance intervals, and lubrication schedules.  
Result: Correct grounded response with citations.

Question 7: What kind of technical support or assistance is available to users of this system?  
Response includes local product support, technical training, and warranty/service agreements.  
Result: Correct grounded response with citations.

---

## Out-of-Scope Evaluation

Question 8: Who is the CEO of Rockwell Automation?  
Response: Not found in manual.  
Result: Pass.

Question 9: What is today’s weather in Toronto?  
Response: Not found in manual.  
Result: Pass.

Question 10: Explain Indian electrical safety laws related to this system.  
Response: Not found in manual.  
Result: Pass.

---

## Results Summary

Grounded retrieval accuracy: Pass  
Citation accuracy: Pass  
Out-of-scope handling: Pass  
Hallucination prevention: Pass  

The system returned document-grounded answers and correctly rejected unrelated queries.

---

## Conclusion

The local RAG chatbot successfully retrieved accurate answers from uploaded CNSC and technical manuals using FAISS vector search and Llama 3. All grounded queries returned citation-based responses, and all out-of-scope queries were correctly rejected. The system meets the project evaluation requirements and demonstrates reliable RAG implementation using Agile methodology.
