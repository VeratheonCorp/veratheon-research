# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Package Manager**: This repository uses `uv` (Astral's package manager). Do NOT use `pip` or `pipenv`.

**Run the main application**:
```bash
uv run python run.py
```

**Run tests**:
```bash
uv run pytest
```

**Run tests with coverage**:
```bash
uv run pytest --cov=src
```

**Install dependencies**:
```bash
uv sync
```

## Architecture

This is a **market research agent** for stock analysis using Prefect orchestration and OpenAI Agents SDK.

### Key Architectural Principles

1. **Strict Separation of Concerns**:
   - **Flows** (`src/prefect/flows/`): Thin wrappers for Prefect orchestration, contain NO business logic
   - **Tasks** (`src/prefect/tasks/`): Data orchestration only, contain NO business logic  
   - **Business Logic** (`src/research/`): All core research logic lives here

2. **Data Flow Architecture**:
   - Main flow: `src/prefect/flows/research_flow.py:main_research_flow()`
   - Subflows: Forward PE analysis, news sentiment, trade ideas
   - Uses Alpha Vantage API for financial data (`src/lib/`)

3. **Model Management**:
   - Uses `litellm` for model abstraction (`src/lib/llm_model.py`)
   - Supports multiple Ollama models (Gemma, GPT-OSS) and OpenAI models
   - Model selection via `MODEL_SELECTED` environment variable

### Research Pipeline

The agent performs stock research through these steps:
1. **Peer Group Analysis**: Identifies comparable companies
2. **Forward PE Sanity Check**: Validates earnings data quality  
3. **Forward PE Analysis**: Calculates valuation metrics
4. **News Sentiment Analysis**: Analyzes recent news sentiment
5. **Trade Ideas Generation**: Synthesizes research into actionable insights

### Environment Variables

Required in `.env` file:
- `ALPHA_VANTAGE_API_KEY`: For financial data
- `OPENAI_API_KEY`: For AI model access (if using OpenAI)
- `MODEL_SELECTED`: Model choice (local_gemma27b, nord_gemma27b, local_gptoss, nord_gptoss, o4_mini)
- `LOCAL_OLLAMA_URL`/`NORD_OLLAMA_URL`: Ollama server URLs

Optional in `.env` file:
- `USE_EARNINGS_ESTIMATES_API`: Set to "false" to use the legacy Earnings Calendar API instead of the new Earnings Estimates API for consensus EPS data (default: true)

### Testing Strategy

- Uses `pytest` with path configuration in `pyproject.toml`
- Test files in `tests/` directory with unit tests in `tests/unit/`
- Mocks external API calls to avoid hitting real APIs during tests

## Development Guidelines

- When adding new research capabilities, put business logic in `src/research/`
- When adding new data sources, put integration code in `src/lib/`
- Keep Prefect flows and tasks as thin orchestration layers
- All new features must maintain the separation between orchestration and business logic
- Use `uv run` prefix for all Python commands