# 🔍 RAG Agent — Local AI with Real-Time Web Search

> A RAG-based AI agent that uses **Qwen3:8b** (via Ollama) with live web search to answer questions with current, real-world information.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000)
![LangChain](https://img.shields.io/badge/LangChain-1.2-blue)

## The Problem

Local LLMs like Qwen3 are powerful, but their knowledge has a cutoff date. Ask about the latest iPhone launch, today's news, or current pricing — and you get outdated or hallucinated answers.

**RAG (Retrieval-Augmented Generation)** fixes this by searching the web first, retrieving real content, and injecting it as context before the model generates a response.

## How It Works

```
User Prompt
    ↓
┌─────────────────────────────┐
│  🔍 Web Search (DuckDuckGo) │  ← Search for current info
└─────────────┬───────────────┘
              ↓
┌─────────────────────────────┐
│  📄 Fetch Articles          │  ← Read full webpage content
└─────────────┬───────────────┘
              ↓
┌─────────────────────────────┐
│  🧠 Context Injection       │  ← Feed search results + article text to LLM
└─────────────┬───────────────┘
              ↓
┌─────────────────────────────┐
│  🤖 Qwen3:8b via Ollama     │  ← Generate response with real context
└─────────────┬───────────────┘
              ↓
         Response with
        cited sources
```

### Example: Marketing Use Case

**Prompt:** "Create Google Ads for the latest iPhone launch."

**What the agent does:**
1. Searches DuckDuckGo for "latest iPhone launch 2026 specs features"
2. Reads top articles from Apple, The Verge, etc.
3. Extracts key specs (chip, camera, price, etc.)
4. Injects all of that as context
5. Qwen3 generates accurate ad copy based on **real, current data**

No hallucinated specs. No outdated pricing. Real information → real output.

## Tools

The agent has 2 tools it can call autonomously:

| Tool | What it does |
|------|-------------|
| `web_search` | Searches DuckDuckGo for current info (no API key needed) |
| `fetch_webpage` | Fetches and extracts text content from any URL |

The agent decides **when and how** to use tools based on the query. It can chain them — search first, then read specific articles for detail.

## Prerequisites

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager (written in Rust, 10-100x faster than pip)
- **Ollama** installed and running with `qwen3:8b` model

### Install Ollama & Qwen3

```bash
# Install Ollama (if not already)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the Qwen3 8B model
ollama pull qwen3:8b

# Start Ollama server (if not running)
ollama serve
```

### Install uv (if not already)

```bash
# macOS
brew install uv

# Or via the install script
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

```bash
# Clone and navigate
cd agents/rag-agent

# Create virtual environment with uv
uv venv venv --python python3.10 --seed

# Activate
source venv/bin/activate   # macOS / Linux

# Install dependencies (using uv pip — same as pip, but ~10x faster)
uv pip install -r requirements.txt
```

## Usage

### Interactive Mode (Chat)

```bash
python3 agent.py
```
Initializing Qwen3 (qwen3:8b) via Ollama...
Creating RAG agent with tools: web_search, fetch_webpage
RAG Agent ready!

Running demo queries...


────────────────────────────────────────────────────────────
📝 Query: Create Google Ads copy for the latest iPhone launch. Include key specs and features.
────────────────────────────────────────────────────────────


🤖 Response:

Here's a Google Ads copy for the latest iPhone launch (iPhone 17 series), based on current specs and
features:

---

**🚀 Upgrade to the Future with the iPhone 17!**  
Experience next-level performance with the **iPhone 17** and **iPhone 17 Pro**—the most advanced
iPhones ever!

✨ **Key Features:**  
✅ **A18 Bionic Chip**: Smoother multitasking, faster app launches, and superior AI capabilities.  
✅ **Pro-grade Camera System**: 48 MP main lens + 12 MP ultra-wide, capture stunning photos and 4K
videos.
✅ **Dynamic Island 2.0**: Intuitive notifications and controls right on your screen.  
✅ **Action Button**: Customize shortcuts for quick access to apps, music, or more.  
✅ **All-Day Battery Life**: Up to 24 hours of streaming, browsing, and more.  
✅ **Lightning-fast 5G**: Stay connected everywhere, all the time.  

**📱 Choose Your Model:**  
- **iPhone 17e** (Entry-Level): 6 GB RAM, 48 MP camera, starting at ₹43,900.  
- **iPhone 17 Pro** (Pro Version): Advanced telephoto lens, bigger battery, and premium design.  

**📅 Launch Date:** September 19, 2025.  
**🛒 Available Now:** Pre-order today and get exclusive early-bird perks!  

**Don’t Miss Out!**  
👉 [Shop iPhone 17 Now](https://www.apple.com/in/iphone-17)  

---

**Sources:**  
1. [iPhone 17 specs and release date](https://en.wikipedia.org/wiki/List_of_iPhone_models)  
2. [CNET: Best iPhone 2026 guide](https://www.cnet.com/tech/mobile/best-iphone/)  
3. [91Mobiles: iPhone price list](https://www.91mobiles.com/list-of-phones/apple-mobile-price-list-
in-india)

*Note: Specs are based on 2025–2026 releases. Always verify details on Apple’s official site.*

────────────────────────────────────────────────────────────
```

### Single Query Mode

```bash
python3 agent.py "What are the top trending AI tools in March 2026? Give me a brief summary of each."
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `qwen3:8b` | Ollama model to use |

Create a `.env` file to override:

```bash
OLLAMA_MODEL=qwen3:8b
```

## Project Structure

```
rag-agent/
├── agent.py             # Main RAG agent — tools + LLM + interactive mode
├── requirements.txt     # Python dependencies
├── .env                 # (optional) Environment variable overrides
├── .gitignore           # Git ignore rules
├── README.md            # You are here
└── venv/                # Virtual environment (not committed)
```

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        User Layer                            │
│                    (CLI / Interactive)                       │
└──────────────────────┬───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                   LangChain Agent                            │
│               (create_agent + tool routing)                  │
│                                                              │
│       ┌─────────────┐         ┌──────────────┐               │
│       │ web_search  │         │ fetch_webpage│               │
│       │ (DuckDuckGo)│         │ (BS4 + lxml) │               │
│       └──────┬──────┘         └──────┬───────┘               │
│              │                       │                       │
└──────────────┼───────────────────────┼───────────────────────┘
               │                       │
┌──────────────▼───────────────────────▼───────────────────────┐
│                    RAG Context Layer                         │
│           (search results + article text)                    │
└──────────────────────┬───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│                   Ollama (Local)                             │
│                Qwen3:8b Model                                │
│                                                              │
│   Receives: system prompt + user query + tool results        │
│   Returns:  contextual response with cited sources           │
└──────────────────────────────────────────────────────────────┘
```

## Example Queries

```bash
# Marketing
python3 agent.py "Write social media posts about trending AI tools"

# Research
python3 agent.py "Compare the latest MacBook Pro vs Dell XPS specs"

# News
python3 agent.py "What happened in tech news today?"

# Sports
python3 agent.py "Give me the two finalists of T20 Cricket Men's World Cup 2026?"
```

## Limitations

- **Rate limits**: DuckDuckGo may rate-limit after many rapid queries. Space out requests if this happens.
- **Scraping**: Some sites block automated access. The agent handles errors gracefully and moves to the next result.
- **Context window**: Article content is truncated to 3,000 chars per page to fit within the model's context window.
- **Model quality**: Qwen3:8b is capable but smaller models may occasionally misuse tools or produce less coherent output. Upgrade to larger models (e.g., `qwen3:32b`) for better results.

## License

MIT
