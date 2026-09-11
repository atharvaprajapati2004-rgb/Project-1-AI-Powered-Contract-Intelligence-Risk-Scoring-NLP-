# AI-Powered Contract Intelligence & Risk Scoring

An intelligent legal contract analysis platform that uses Natural Language Processing (NLP) to extract contract clauses, identify named entities, detect potential risks, calculate risk scores, and perform semantic search across contract content.

The system supports PDF, DOCX, and TXT contract documents and provides REST APIs through FastAPI, asynchronous processing through Celery and Redis, semantic search using embeddings and FAISS, and a responsive web interface for contract analysis.

---

## Project Overview

Legal contracts often contain complex clauses, obligations, liabilities, payment terms, termination conditions, confidentiality requirements, and other potentially risky provisions.

Manually reviewing large numbers of contracts can be time-consuming and error-prone.

This project provides an automated contract intelligence pipeline that:

- Accepts contract documents
- Extracts text from PDF, DOCX, and TXT files
- Uses OCR for scanned PDF documents
- Extracts contract clauses
- Identifies named entities such as organizations, dates, locations, and monetary values
- Detects potential contractual risks
- Calculates an overall risk score
- Performs semantic search using document embeddings
- Supports FAISS-based vector search
- Supports asynchronous contract analysis using Celery and Redis
- Provides REST APIs through FastAPI
- Provides a web-based frontend for contract analysis
- Supports Docker-based deployment

---

### Objectives

The main objectives of the project are:

1. Automate contract document processing.
2. Extract useful information from legal documents.
3. Identify important contract clauses.
4. Detect potentially risky contractual language.
5. Calculate an overall contract risk score.
6. Extract named entities from contract text.
7. Enable semantic search across contract content.
8. Support asynchronous document processing.
9. Provide APIs for integration with other applications.
10. Provide an easy-to-use web interface for contract analysis.
11. Containerize the backend and supporting services using Docker.

---

### System Architecture

```text
                    ┌───────────────────────┐
                    │      Web Frontend     │
                    │   React + Vite        │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │       FastAPI         │
                    │      REST API         │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
       ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
       │ Document    │   │   Contract  │   │  Semantic   │
       │   Loader    │   │   Analysis  │   │   Search    │
       └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
              │                 │                 │
              ▼                 ▼                 ▼
       ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
       │ PDF / DOCX  │   │   Clause    │   │ Sentence    │
       │ / TXT / OCR │   │  Extraction │   │ Transformers │
       └─────────────┘   └──────┬──────┘   └──────┬──────┘
                                │                 │
                                ▼                 ▼
                         ┌─────────────┐   ┌─────────────┐
                         │ Risk        │   │    FAISS    │
                         │ Detection   │   │ Vector DB   │
                         └──────┬──────┘   └─────────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │ Risk Scoring│
                         └─────────────┘

                    Background Processing
                              │
                              ▼
                    ┌──────────────────┐
                    │ Celery + Redis   │
                    └──────────────────┘
