
# 🎙️ AI Meeting Notes Analyzer using LangGraph (Agentic RAG)

<p align="center">
  <img src="assets/banner.png" alt="AI Meeting Notes Analyzer Banner" width="100%"/>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.11-blue?logo=python"/></a>
  <a href="#"><img src="https://img.shields.io/badge/LangGraph-Agentic%20Workflow-purple"/></a>
  <a href="#"><img src="https://img.shields.io/badge/LangChain-RAG-green"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Whisper-Speech--to--Text-black"/></a>
  <a href="#"><img src="https://img.shields.io/badge/ChromaDB-Vector%20Database-orange"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Streamlit-Deployed-red?logo=streamlit"/></a>
  <a href="#"><img src="https://img.shields.io/badge/HuggingFace-LLM-yellow?logo=huggingface"/></a>
</p>

> **An end-to-end Agentic AI application that converts meeting audio into structured meeting notes, action items, executive summaries, and an intelligent chatbot powered by Retrieval-Augmented Generation (RAG).**

---

## 📌 Project Overview

AI Meeting Notes Analyzer is a production-style Generative AI application built with **LangGraph**, **LangChain**, **Whisper**, **ChromaDB**, and **Hugging Face LLMs**.

Instead of simply summarizing a transcript, the application follows an **Agentic RAG workflow** where specialized AI agents collaborate to process meeting recordings.

### ✨ What this application does

- 🎤 Converts meeting audio into text using Whisper.
- 📝 Generates concise executive meeting summaries.
- ✅ Extracts action items automatically.
- 💬 Lets users chat with meeting transcripts using RAG.
- 🧠 Uses LangGraph to orchestrate multiple AI agents.
- 🌐 Interactive Streamlit web application.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🎙️ Speech-to-Text | Converts MP3, WAV and M4A audio into transcripts using Whisper. |
| 📄 Meeting Summary | Generates an executive summary using an LLM. |
| ✅ Action Item Extraction | Identifies tasks, owners and deadlines. |
| 💬 Meeting Chatbot | Ask natural language questions about the meeting transcript. |
| 📚 RAG Pipeline | Retrieves relevant transcript chunks before answering questions. |
| 🧠 LangGraph Workflow | State-based orchestration of multiple AI agents. |
| ⚡ Streamlit UI | Clean interactive frontend for uploading and chatting. |

---

## 🏗️ Architecture

<p align="center">
  <img src="assets/architecture.png" width="90%"/>
</p>

### Agentic Workflow

```text
Upload Audio
      │
      ▼
 Whisper Transcription
      │
      ▼
 Transcript Processing
      │
      ▼
 Text Chunking
      │
      ▼
 Embeddings
      │
      ▼
 ChromaDB Vector Store
      │
 ┌────┴──────────────┐
 │                   │
 ▼                   ▼
Summary Agent   Action Item Agent
 │                   │
 └──────┬────────────┘
        ▼
   Retrieval Agent
        ▼
      Chatbot
```

---

## 🧠 LangGraph Workflow

This project uses **LangGraph** instead of a traditional sequential chain.

### AI Agents

| Agent | Responsibility |
|-------|----------------|
| 🎤 Transcription Agent | Converts speech into text. |
| ✂️ Chunking Agent | Splits transcript into semantic chunks. |
| 📦 Embedding Agent | Creates vector embeddings. |
| 🔍 Retrieval Agent | Retrieves relevant transcript context. |
| 📝 Summary Agent | Generates executive meeting summary. |
| ✅ Action Item Agent | Extracts tasks and ownership. |
| 💬 Chat Agent | Answers user questions grounded in retrieved context. |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Framework | Streamlit |
| Agent Framework | LangGraph |
| LLM Framework | LangChain |
| Speech Recognition | Whisper |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Language Model | Hugging Face Transformers |
| Deployment | Streamlit Community Cloud |

---

## 📂 Project Structure

```text
AI-Meeting-Notes-Analyzer-LangGraph/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── graph/
│   ├── components/
│   ├── utils/
│   └── exception.py
│
├── chroma_db/
├── uploaded_audio/
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/ARCHITTOMAR15/ai-meeting-notes-analyzer-langgraph.git
cd ai-meeting-notes-analyzer-langgraph
```

### Create Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## 🎯 How It Works

### Step 1 — Upload Audio

Upload meeting recordings in **MP3**, **WAV**, or **M4A** format.

### Step 2 — Speech-to-Text

Whisper converts the audio into an accurate transcript.

### Step 3 — Chunk & Embed

Transcript is split into semantic chunks and converted into embeddings.

### Step 4 — Store in ChromaDB

Embeddings are stored inside ChromaDB for semantic retrieval.

### Step 5 — AI Agents Execute

LangGraph coordinates summary generation, action item extraction, and retrieval.

### Step 6 — Chat with Meeting Notes

Users ask natural language questions grounded in the meeting transcript.

---

## 📸 Application Screenshots

> Replace these placeholders after uploading screenshots.

| Upload Audio | Meeting Summary |
|--------------|----------------|
| ![](assets/upload.png) | ![](assets/summary.png) |

| Action Items | Meeting Chatbot |
|--------------|----------------|
| ![](assets/action_items.png) | ![](assets/chatbot.png) |

---

## 💬 Example Output

### Executive Summary

```text
The team discussed the September product launch timeline,
deployment blockers, marketing deliverables, and pending backend tasks.
The deployment is scheduled for Wednesday while marketing assets
will be finalized before Friday.
```

### Action Items

| Owner | Task | Deadline |
|-------|------|----------|
| Ravi | Deploy backend service | Wednesday |
| Priya | Finalize marketing creatives | Friday |
| QA Team | Complete regression testing | Thursday |

### Ask Questions

```text
Q: Who is responsible for deployment?

A: Ravi is responsible for backend deployment before Wednesday.
```

---

## 📚 Retrieval-Augmented Generation (RAG)

The chatbot does **not** rely only on the LLM.

Instead it follows this retrieval pipeline:

1. Convert transcript into embeddings.
2. Store embeddings in ChromaDB.
3. Retrieve top relevant chunks.
4. Send retrieved context to the LLM.
5. Generate grounded responses.

### Why RAG?

- Reduces hallucinations.
- Answers are based on meeting content.
- Supports long meeting transcripts efficiently.

---

## ⚡ Streamlit Cloud Deployment Optimization

The project is optimized for Streamlit Community Cloud.

### Optimizations Included

- Lazy loading of Hugging Face models.
- Cached embeddings.
- Cached Whisper model.
- Reduced startup memory usage.
- Lightweight dependency loading.
- Persistent ChromaDB storage.

---

## 🔮 Future Improvements

- Speaker diarization.
- Multi-speaker meeting identification.
- Sentiment analysis.
- PDF export of meeting minutes.
- Email summary generation.
- Cloud vector database support.
- Multi-meeting knowledge base.

---

## 👨‍💻 About the Developer

**Archit Choudhary**

AI & Machine Learning Engineer focused on building production-ready Generative AI applications using LangGraph, LangChain, RAG, LLMs, Machine Learning, and MLOps.

### Connect With Me

- LinkedIn: *Add your LinkedIn URL*
- GitHub: https://github.com/ARCHITTOMAR15

---

## ⭐ If you found this project useful

Give this repository a ⭐ on GitHub if it helped you learn Agentic AI, LangGraph, or RAG workflows.

---

## 📄 License

This project is released under the **MIT License**.
