# 📄 Research Paper Assistant

An AI-powered **Research Paper Assistant** that allows users to upload research papers in PDF format, process their content, and interact with the papers using **Retrieval-Augmented Generation (RAG)**.

The project uses **OpenAI, LangChain, ChromaDB, and Streamlit** to provide an interactive way to search and understand research papers.

## ✨ Features

- 📑 Upload and process research papers in PDF format
- 🔍 Extract and clean text from PDFs
- ✂️ Split documents into meaningful chunks
- 🧠 Generate embeddings for document chunks
- 🗄️ Store and retrieve embeddings using ChromaDB
- 🤖 Ask questions about uploaded research papers
- 💬 Generate answers using an OpenAI model
- 🌐 Interactive Streamlit interface

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — Web interface
- **OpenAI API** — LLM and embeddings
- **LangChain** — RAG pipeline
- **ChromaDB** — Vector database
- **PyPDF** — PDF text extraction

## 📂 Project Structure

```text
research-paper-assistant/
│
├── .streamlit/
├── app.py
├── pdf_utils.py
├── rag_engine.py
├── requirements.txt
├── .gitignore
└── README.md
