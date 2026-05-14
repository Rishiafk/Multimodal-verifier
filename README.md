# 🧠 NexusAI — Multimodal Claim-Evidence Verifier

A modern Retrieval-Augmented Generation (RAG) powered AI verification platform that analyzes claims against supporting evidence using semantic retrieval, embeddings, and grounded AI reasoning.

Built with Flask, Cohere AI, Sentence Transformers, and a modular scalable backend architecture.

---

# ✨ Features

## 🔍 AI-Powered Claim Verification
- Verifies claims against supporting evidence using Cohere LLMs
- Produces structured verdicts:
  - ✅ Supported
  - ⚠️ Partially Supported
  - ❌ Refuted

---

## 🧠 Retrieval-Augmented Generation (RAG)
- Semantic chunking pipeline
- Embedding-based evidence retrieval
- Cosine similarity ranking
- Top-K relevant evidence chunk selection
- Grounded reasoning generation

---

## 📚 Embedding Pipeline
- Uses `sentence-transformers/all-MiniLM-L6-v2`
- Sentence-aware chunking
- Metadata-enriched vector generation
- Retrieval trace support
- Similarity threshold filtering

---

## ⚡ Modern Modular Architecture

Refactored from a monolithic Flask app into a scalable modular monolith.

### Includes:
- `services/`
- `config/`
- `vector_store/`
- `uploads/`
- reusable AI service layers
- parser services
- verification orchestration

---

## 🛡️ Production-Oriented Safeguards
- Structured JSON response parsing
- Token-aware prompt budgeting
- Exception sanitization
- Graceful frontend degradation
- Backend logging + observability
- Safe fallback handling

---

## 🎨 Modern AI Dashboard UI
- Dark futuristic interface
- Responsive design
- Animated AI confidence indicators
- Clean verification panels
- Real-time verification results

---

# 🏗️ Updated Architecture

```text
User Input
   ↓
Verification Service
   ↓
Embedding Service
   ↓
Semantic Chunk Retrieval
   ↓
Relevant Evidence Chunks
   ↓
Cohere AI Generation
   ↓
Structured JSON Parsing
   ↓
Frontend Result Rendering
```

---

# 📂 Project Structure

```text
multimodal-verifier/
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── embedding_service.py
│   ├── parser_service.py
│   └── verification_service.py
│
├── vector_store/
│
├── uploads/
│
├── static/
│   └── styles.css
│
├── templates/
│   └── index.html
│
├── run.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🚀 Quick Start

## 1. Clone Repository

```bash
git clone https://github.com/Rishiafk/Multimodal-verifier.git
cd Multimodal-verifier
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create `.env`

```env
COHERE_API_KEY=your_api_key_here
```

---

## 5. Run Application

```bash
python run.py
```

---

## 6. Open Browser

```text
http://127.0.0.1:5000
```

---

# 🧪 Example Usage

## Claim

```text
The Eiffel Tower is located in Paris.
```

## Evidence

```text
The Eiffel Tower is one of the most famous landmarks in Paris, France.
```

## Expected Result

```text
SUPPORTED
```

with grounded reasoning generated from retrieved semantic evidence chunks.

---

# 🔍 How the RAG Pipeline Works

## Step 1 — Evidence Chunking
Large evidence text is split into semantically coherent chunks.

---

## Step 2 — Embedding Generation
Each chunk is converted into vector embeddings using Sentence Transformers.

---

## Step 3 — Semantic Retrieval
The claim embedding is compared against evidence embeddings using cosine similarity.

---

## Step 4 — Top-K Chunk Selection
Most relevant chunks are selected based on similarity thresholds.

---

## Step 5 — Grounded AI Verification
Only the retrieved evidence chunks are passed into the LLM.

---

## Step 6 — Structured Parsing
The model returns structured JSON:
- verdict
- explanation
- confidence

---

# ⚙️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Flask |
| LLM | Cohere |
| Embeddings | Sentence Transformers |
| Vector Logic | Cosine Similarity |
| Frontend | HTML, CSS |
| Environment | Python |
| Architecture | Modular Monolith |

---

# 🛠️ Current Capabilities

- ✅ Claim verification
- ✅ Semantic retrieval
- ✅ Grounded reasoning
- ✅ Embedding pipeline
- ✅ RAG workflow
- ✅ Confidence scoring
- ✅ Error handling
- ✅ Modular architecture

---

# 🔮 Planned Enhancements

## Multimodal Expansion
- [ ] Image verification
- [ ] OCR pipeline
- [ ] PDF ingestion
- [ ] Audio evidence support

---

## Advanced Retrieval
- [ ] FAISS vector database
- [ ] Hybrid retrieval
- [ ] Reranking pipeline
- [ ] Cross-encoder retrieval

---

## AI Enhancements
- [ ] Hallucination detection
- [ ] Source citation system
- [ ] Multi-agent verification
- [ ] Self-consistency reasoning

---

## Platform Features
- [ ] Authentication
- [ ] Verification history
- [ ] Export reports
- [ ] Public API
- [ ] Batch verification

---

# 🧪 Error Handling

The system gracefully handles:
- invalid API responses
- token overflow
- retrieval failures
- malformed JSON
- unsupported model responses
- frontend-safe degradation

---

# 📈 Engineering Improvements Made

## Backend
- Refactored monolithic architecture
- Introduced service orchestration
- Added reusable verification pipeline

---

## AI Pipeline
- Implemented semantic retrieval
- Added token budgeting
- Added structured parsing

---

## Stability
- Added logging
- Added fallback mechanisms
- Added exception sanitization

---

# 🤝 Contributing

## Steps

```bash
git checkout -b feature-name
git commit -m "Added feature"
git push origin feature-name
```

Then open a Pull Request.

---

# 📝 License

This project is licensed under the MIT License.

---

# 🙏 Acknowledgments

- Cohere
- Hugging Face
- Sentence Transformers
- Flask
- Open-source AI ecosystem

---

# 👨‍💻 Developer

Built and engineered by **Rishi Kumar**

Focused on:
- AI Systems
- Retrieval-Augmented Generation
- Full Stack Development
- Intelligent Verification Systems

---

# ⭐ Project Status

## Current Status:
✅ Functional RAG Verification Platform

## Architecture Status:
✅ Modularized and scalable

## Next Major Phase:
🚀 Multimodal AI expansion
