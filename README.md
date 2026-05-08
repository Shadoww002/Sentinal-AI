# 🛡️ Sentinel AI: Real-Time RAG Fact-Checking Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Llama 3](https://img.shields.io/badge/Local_LLM-Llama_3-orange.svg)](https://ollama.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sentinel AI** is a production-grade, 100% locally hosted Retrieval-Augmented Generation (RAG) pipeline designed to combat misinformation. It uses local LLM reasoning and real-time live news retrieval to verify claims, outputting detailed reasoning, live citations, and confidence scores.

By utilizing **Ollama** for local inference, Sentinel AI runs completely privately with **zero API costs** and no risk of data leakage.

---

## 🎥 Demo

> **Note:** *Insert a GIF or link to a YouTube video showcasing your Streamlit dashboard fact-checking a live news event here.*

[![Watch the Demo](https://img.shields.io/badge/Watch-Demo_Video-red?style=for-the-badge&logo=youtube)](YOUR_YOUTUBE_LINK_HERE)

---

## ✨ Core Features

- **Live Web RAG:** Bypasses LLM knowledge cutoffs by actively querying Google News (`gnews`) for breaking journalistic evidence.
- **Local Reasoning Engine:** Powered by Meta's **Llama 3 (8B)** running locally via Ollama. It doesn't just output True/False; it writes coherent, human-like explanations based on strict temporal logic constraints.
- **Semantic Noise Filtering:** Uses `all-mpnet-base-v2` and **FAISS** vector databases to sift through raw web scraping and extract only the most mathematically relevant sentences.
- **Enterprise-Grade UI:** A sleek Streamlit dashboard featuring confidence progress bars, expander widgets, and direct markdown links to cited live sources.

---

## 🧠 System Architecture

Sentinel AI follows a strict, decoupled microservice architecture:

```mermaid
graph TD
    A[User Input] -->|Streamlit UI| B(FastAPI Router)
    B --> C{Decision Engine}
    C -->|1. Raw Text| D[Claim Extractor <br> Llama 3]
    D -->|2. Optimized Query| E[News Fetcher <br> GNews API]
    E -->|3. Live Articles| F[Vector Store <br> MPNet + FAISS]
    F -->|4. Exact Evidence Sentence| G[NLI Verifier <br> Llama 3]
    D -->|Original Claim| G
    G -->|5. Verdict & Reasoning| C
    C -->|JSON Payload| B
    B -->|Render Dashboard| A '''

Here is a complete, highly professional, and production-ready README.md for your GitHub repository.

I have included a Mermaid.js diagram (which GitHub natively renders into a beautiful flowchart), a dedicated section for your demo video, and explicit instructions for setting up the local Llama 3 engine.

Copy everything inside the code block below and paste it into your README.md file.

Markdown
# 🛡️ Sentinel AI: Real-Time RAG Fact-Checking Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Llama 3](https://img.shields.io/badge/Local_LLM-Llama_3-orange.svg)](https://ollama.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sentinel AI** is a production-grade, 100% locally hosted Retrieval-Augmented Generation (RAG) pipeline designed to combat misinformation. It uses local LLM reasoning and real-time live news retrieval to verify claims, outputting detailed reasoning, live citations, and confidence scores.

By utilizing **Ollama** for local inference, Sentinel AI runs completely privately with **zero API costs** and no risk of data leakage.

---

## 🎥 Demo

> **Note to user:** *Replace the placeholder image below with a link to your actual YouTube video or upload a `.gif` showcasing the Streamlit UI in action.*

[![Watch the Demo](https://img.shields.io/badge/Watch-Demo_Video-red?style=for-the-badge&logo=youtube)](YOUR_YOUTUBE_LINK_HERE)

*(Insert a GIF or screenshot of the UI running a successful fact-check here)*

---

## ✨ Core Features

- **Live Web RAG:** Bypasses LLM knowledge cutoffs by actively querying Google News (`gnews`) for breaking journalistic evidence.
- **Local Reasoning Engine:** Powered by Meta's **Llama 3 (8B)** running locally via Ollama. It doesn't just output True/False; it writes coherent, human-like explanations.
- **Semantic Noise Filtering:** Uses `all-mpnet-base-v2` and **FAISS** vector databases to sift through raw web scraping and extract only the most mathematically relevant sentences.
- **Advanced Temporal Logic:** The LLM is explicitly prompted to understand timelines (e.g., distinguishing between a completed event and a pending decision).
- **Enterprise-Grade UI:** A sleek Streamlit dashboard featuring confidence progress bars, expander widgets, and direct markdown links to cited sources.

---

## 🧠 System Architecture

Sentinel AI follows a strict, decoupled microservice architecture:

```mermaid
graph TD
    A[User Input] -->|Streamlit UI| B(FastAPI Router)
    B --> C{Decision Engine}
    C -->|1. Raw Text| D[Claim Extractor <br> Llama 3]
    D -->|2. Optimized Query| E[News Fetcher <br> GNews API]
    E -->|3. Live Articles| F[Vector Store <br> MPNet + FAISS]
    F -->|4. Exact Evidence Sentence| G[NLI Verifier <br> Llama 3]
    D -->|Original Claim| G
    G -->|5. Verdict & Reasoning| C
    C -->|JSON Payload| B
    B -->|Render Dashboard| A '''

# 🛠️ Tech Stack

## 🎨 Frontend
- **Streamlit** — Interactive web-based user interface

## ⚙️ Backend
- **FastAPI** — High-performance backend API framework
- **Uvicorn** — ASGI server for running FastAPI applications

## 🤖 AI / LLMs
- **Ollama** — Local LLM runtime environment
- **Llama 3 8B** — Large Language Model for reasoning and response generation
- **HuggingFace Sentence-Transformers** — Text embedding generation for semantic similarity and retrieval

## 🔍 Retrieval & Vector Search
- **GNews** — Google News wrapper for fetching real-time news articles
- **FAISS (faiss-cpu)** — Efficient vector similarity search and retrieval engine


# 🛣️ Roadmap & Future Enhancements

- [ ] **Caching Layer**  
  Implement Redis or SQLite to cache previously verified claims and bypass the LLM/Search process for identical queries.

- [ ] **Multi-Agent Debate**  
  Implement a secondary "Devil's Advocate" LLM to challenge the Verifier's logic before returning a final verdict.

- [ ] **PDF / Document Ingestion**  
  Allow users to upload PDFs and verify claims against internal documents rather than the live internet.


# 🚀 Future Vision

Sentinel AI aims to evolve into a fully autonomous, explainable, and research-grade misinformation detection system capable of:
- Multi-source verification
- Agentic reasoning
- Long-document analysis
- Real-time streaming verification
- Enterprise-grade deployment

# 🤝 Contributing

Contributions and suggestions are welcome.  
Feel free to fork the repo, open issues, or submit pull requests.

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
