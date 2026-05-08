fake_news_system/
├── backend/                  # The Python engine
│   ├── api/                  
│   │   ├── main.py           # FastAPI entry point. Defines endpoints and rate limiting.
│   │   └── schemas.py        # Pydantic models. Enforces strict I/O validation.
│   ├── services/             # Business logic orchestration
│   │   ├── claim_extractor.py# Isolates testable facts from raw text.
│   │   ├── decision_engine.py# The "brain" that combines NLI scores and source reputation.
│   │   └── explainer.py      # Generates the human-readable justification.
│   ├── models/               
│   │   └── baseline.py       # A naive TF-IDF classifier to benchmark our RAG against.
│   ├── retrieval/            # The "R" in RAG
│   │   ├── news_fetcher.py   # Handles external API calls (Serper/NewsAPI) to get live context.
│   │   └── vector_store.py   # FAISS semantic search to find the exact supporting/refuting sentences.
│   ├── verification/         
│   │   └── nli_verifier.py   # PyTorch-based Natural Language Inference (DeBERTa).
│   ├── scoring/              
│   │   └── credibility.py    # Source reliability heuristics.
│   ├── utils/                
│   │   └── preprocessing.py  # DOM parsing and text normalization.
│   └── config/               
│       └── settings.py       # Pydantic BaseSettings for secure env var management.
├── frontend/                 # User Interface
│   └── app.py                # Streamlit app for rapid prototyping and interaction.
├── deployment/               # Infrastructure
│   ├── Dockerfile            # Containerizes the backend for cloud deployment.
│   └── .github/workflows/    # CI/CD pipelines (main.yml).
├── tests/                    # Pytest suite
│   └── test_pipeline.py      # End-to-end integration tests.
└── requirements.txt          # Pinned dependencies.