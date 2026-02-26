# RAG Test Execution Report
Local RAG System for CNSC Regulatory Documents

---

## 1. Objective

The purpose of this testing phase was to validate:

- Grounded document retrieval
- Citation accuracy
- Hallucination prevention
- Out-of-scope query handling

The RAG system was evaluated using controlled test queries executed through the Streamlit interface.

---

## 2. Test Environment

Application: Local Streamlit App  
URL: http://localhost:8501  
LLM: Llama 3 (Ollama - local)  
Embedding Model: all-MiniLM-L6-v2  
Vector Store: FAISS  
Framework: LangChain  

Indexed Documents:
- REGDOC-2-6-1 — Reliability Programs for Nuclear Power Plants
- CAT-304
- 2364f-tg000 (EN)
- Safety Manual for Fanuc Educational Cell

---

## 3. Test Execution Procedure

Step 1: Start Ollama server  
Step 2: Launch Streamlit application  
Step 3: Confirm documents loaded in sidebar  
Step 4: Enter predefined evaluation queries manually  
Step 5: Observe:
        - Retrieved answer
        - Citation sources
        - Out-of-scope handling behavior
Step 6: Capture screenshots as evidence

---

## 4. Test Cases

A total of 10 queries were executed.

- 7 grounded queries derived from indexed PDFs
- 3 intentionally unrelated queries to test hallucination control

---

## 5. Grounded Query Results

Test Case 1  
Query: Who is this manual intended for and what type of personnel should use it?  
Expected: Response grounded in document with citation  
Actual: Reliability engineers and industrial technical assistants  
Status: PASS

---

Test Case 2  
Query: What safety precautions must be followed before servicing or working on the system?  
Expected: Document-based response with citation  
Actual: Protective equipment, secured guards, debris removal, safe environmental conditions  
Status: PASS

---

Test Case 3  
Query: Why is it important that only qualified personnel perform installation and maintenance?  
Expected: Either grounded answer or "Not found in manual"  
Actual: Not found in manual  
Status: PASS

---

Test Case 4  
Query: What risks or hazards are mentioned if installation or wiring is done incorrectly?  
Expected: Document-based hazards  
Actual: Component damage, reduced product life, equipment malfunction  
Status: PASS

---

Test Case 5  
Query: What precautions are recommended to prevent electrostatic discharge (ESD) damage?  
Expected: ESD handling procedures  
Actual: Grounding wrist strap, conductive storage  
Status: PASS

---

Test Case 6  
Query: What types of troubleshooting or maintenance information does the manual provide?  
Expected: Maintenance-related content  
Actual: Daily checks, maintenance intervals, lubrication schedules  
Status: PASS

---

Test Case 7  
Query: What kind of technical support or assistance is available to users of this system?  
Expected: Support information from documentation  
Actual: Local product support, technical assistance, warranty services  
Status: PASS

---

## 6. Out-of-Scope Query Results (Hallucination Test)

Test Case 8  
Query: Who is the CEO of Rockwell Automation?  
Expected: Not found in manual  
Actual: Not found in manual  
Status: PASS

---

Test Case 9  
Query: What is today’s weather in Toronto?  
Expected: Not found in manual  
Actual: Not found in manual  
Status: PASS

---

Test Case 10  
Query: Explain Indian electrical safety laws related to this system.  
Expected: Not found in manual  
Actual: Not found in manual  
Status: PASS

---

## 7. Acceptance Criteria Validation

Grounded retrieval accuracy: PASS  
Citation-based responses: PASS  
Out-of-scope rejection: PASS  
Hallucination observed: NONE  

---

## 8. Conclusion

The RAG system successfully demonstrated:

- Accurate document retrieval using FAISS
- Controlled response generation using Llama 3
- Proper citation referencing
- Reliable rejection of unrelated queries

The system meets the defined testing requirements and confirms correct RAG pipeline implementation.
