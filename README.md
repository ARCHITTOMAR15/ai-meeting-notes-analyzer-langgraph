
<<<<<<< HEAD
#  AI Meeting Notes Analyzer using LangGraph
=======
# 🎙️ AI Meeting Notes Analyzer using LangGraph
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)

> AI-powered meeting transcript analyzer built with **LangGraph, LangChain, Qwen2.5-0.5B, ChromaDB, and Streamlit**.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-red?style=for-the-badge&logo=streamlit)](https://ai-meeting-notes-analyzer-langgraph-9pdygevpezzwaav8qrm63l.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/ARCHITTOMAR15/ai-meeting-notes-analyzer-langgraph)

---

## 📌 Overview

This project converts **TXT, PDF, and DOCX meeting transcripts** into structured meeting reports using an **Agentic AI workflow** built with LangGraph.

The application automatically generates:

- 📝 Meeting Summary
- 📚 Key Discussion Topics
- ✅ Action Items
- 👤 Task Owners
- 🎯 Priority Classification
<<<<<<< HEAD


---

##  Features

| Feature | Description |
|---------|-------------|
| Meeting Summary | Generates a concise executive summary. |
|  Topic Extraction | Identifies the main discussion topics. |
|  Action Items | Extracts tasks and responsible owners. |
|  Priority Classification | Classifies tasks into High, Medium, or Low priority. |
| 📥 Multi-format Upload | Supports TXT, PDF, and DOCX transcripts. |

=======
- 💬 RAG-based Meeting Chatbot

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 Meeting Summary | Generates a concise executive summary. |
| 🗂️ Topic Extraction | Identifies the main discussion topics. |
| ✅ Action Items | Extracts tasks and responsible owners. |
| 🎯 Priority Classification | Classifies tasks into High, Medium, or Low priority. |
| 💬 Meeting Chatbot | Ask questions using Retrieval-Augmented Generation (RAG). |
| 📥 Multi-format Upload | Supports TXT, PDF, and DOCX transcripts. |
| 📄 Download Report | Export structured meeting notes. |
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)

---

## 🧠 Agentic AI Workflow

```text
Meeting Transcript
        │
        ▼
   Input Node
        │
        ▼
 Topic Extraction Agent
        │
        ▼
 Meeting Summary Agent
        │
        ▼
 Action Item Agent
        │
        ▼
 Priority Classification Agent
        │
        ▼
 Embedding Generation
        │
        ▼
<<<<<<< HEAD
 Faiss Vector Store
=======
 ChromaDB Vector Store
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)
        │
        ▼
 RAG Chatbot (Qwen2.5-0.5B)
        │
        ▼
 Structured Meeting Report
```

---

<<<<<<< HEAD
##  Tech Stack
=======
## 🛠️ Tech Stack
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Backend Development |
| LangGraph | Multi-Agent Workflow Orchestration |
| LangChain | Prompt Engineering & RAG Pipeline |
| Qwen2.5-0.5B Instruct | Open-source LLM |
| Sentence Transformers | Embedding Model |
<<<<<<< HEAD
| Faiss | Vector Database |
=======
| ChromaDB | Vector Database |
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)
| Hugging Face Transformers | Model Inference |
| Streamlit | Interactive Web UI |

---

<<<<<<< HEAD
##  Application Preview

## 📸 Application Preview

<p align="center">
  <img src="app-preview.png" alt="AI Meeting Notes Analyzer Streamlit UI" width="100%">
</p>





##  Skills Demonstrated

- Agentic AI using LangGraph
- Retrieval-Augmented Generation (RAG)
- Vector Databases (FAISS)
=======
## 📸 Application Preview

> Save your Streamlit screenshot as **assets/app-preview.png** and it will appear automatically.

```md
![Application Preview](assets/app-preview.png)
```

---

## 📊 Example Output

### Meeting Summary

> The meeting focused on improving website performance, reducing page load time, and assigning optimization tasks before Friday.

### Key Topics

- Website Performance
- Database Optimization
- Homepage Redesign

### Action Items

| Owner | Task | Priority |
|-------|------|----------|
| David | Optimize database queries | High |
| Sarah | Redesign homepage layout | High |

### Ask Questions

```text
Q: Who is responsible for database optimization?

A: David is responsible for optimizing the database queries this week.
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/ARCHITTOMAR15/ai-meeting-notes-analyzer-langgraph.git

cd ai-meeting-notes-analyzer-langgraph

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

## 🎯 Skills Demonstrated

- Agentic AI using LangGraph
- Retrieval-Augmented Generation (RAG)
- Vector Databases (ChromaDB)
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)
- Open-source LLM Deployment
- Prompt Engineering
- Streamlit Application Development

---

<<<<<<< HEAD
##  Future Improvements
=======
## 🔮 Future Improvements
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)

- Speaker-wise meeting insights.
- Multilingual transcript support.
- Sentiment analysis.
- PDF meeting report generation.
- Cloud vector database integration.

---

<<<<<<< HEAD
##  Author

**Archit Tomar**
=======
## 👨‍💻 Author

**Archit Choudhary**
>>>>>>> 621f9c8 (Use Hugging Face Inference API instead of local Qwen model)

AI & Machine Learning Engineer focused on building production-ready Generative AI applications using **LangGraph, LangChain, RAG, LLMs, and Streamlit**.

⭐ If you like this project, consider giving it a **Star** on GitHub.
