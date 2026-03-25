# GitHub AI Agent

Ever tried asking an AI about a framework that just came out, or about your private codebase? It doesn't go well. The AI doesn't know what it doesn't know, and you end up copy-pasting docs into chat windows like it's 2019.

This project fixes that. It's an AI agent that actually reads your GitHub repo — the docs, the code, all of it — and then answers your questions about it intelligently. Not from memory. From the source.

I'm building this over 7 days as part of an AI Engineering cohort. Everything here is a work in progress, and I'm learning as I go.

## How it works

The idea is pretty straightforward:

1. Point it at a GitHub repo
2. It pulls down the docs and code
3. It chunks everything into searchable pieces
4. When you ask a question, it searches for the relevant chunks and hands them to Claude (Anthropic's LLM), which reasons over them and gives you an actual answer

Under the hood, search uses a mix of keyword matching (BM25) and semantic embeddings — so it catches both exact terms and conceptual similarity. The agent layer uses Pydantic AI for structured tool calling.

## What I'm using

- **Python 3.11+** for everything
- **Anthropic Claude** as the brain
- **Pydantic AI** for the agent and tool-calling layer
- **BM25 + embeddings** for hybrid search
- **Streamlit** for the web interface

## Project layout

```
src/
  ingestion/      # Fetching and extracting repo content
  processing/     # Chunking documents intelligently
  search/         # Lexical, semantic, and hybrid search
  agent/          # Claude-powered agent with tools
  evaluation/     # Testing and measuring how well it works

app/
  streamlit_app.py  # The web UI

data/             # Downloaded repo content (not committed)
tests/            # Tests
docs/             # Extra documentation and demo assets
```

## Getting started

You'll need Python 3.11+, an [Anthropic API key](https://console.anthropic.com/), and optionally a [GitHub token](https://github.com/settings/tokens) for better rate limits.

```bash
git clone https://github.com/YOUR_USERNAME/github-ai-agent.git
cd github-ai-agent

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Add your API keys to .env
```

Then run it:

```bash
streamlit run app/streamlit_app.py
```

## Progress

Tracking where I am in the 7-day build:

- [ ] Day 1 — Pull data from a GitHub repo
- [ ] Day 2 — Chunk and process documents for search
- [ ] Day 3 — Build lexical, semantic, and hybrid search
- [ ] Day 4 — Wire up a Claude agent with tool calling
- [ ] Day 5 — Evaluate and test everything
- [ ] Day 6 — Deploy with Streamlit
- [ ] Day 7 — Polish, document, and share

## Results

I'll add evaluation metrics and a demo here once I get to Days 5 and 6.

## License

MIT
