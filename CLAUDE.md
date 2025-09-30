# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Package Manager**: This repository uses `uv` (Astral's package manager). Do NOT use `pip` or `pipenv`.

**Run the main application**:
```bash
uv run python run.py
```

**Run the FastAPI server**:
```bash
uv run python server.py
```

**Run with Docker Compose** (includes API, UI, and Redis):
```bash
docker-compose up
```

**Run tests**:
```bash
uv run pytest
```

**Run specific test file**:
```bash
uv run pytest tests/unit/historical_earnings/test_historical_earnings_util.py -v
```

**Run tests with coverage**:
```bash
uv run pytest --cov=src
```

**Install dependencies**:
```bash
uv sync
```

**UI Development** (SvelteKit frontend in `agent-ui/`):
```bash
cd agent-ui
npm install        # Install dependencies
npm run dev        # Development server (runs on http://localhost:5173)
npm run build      # Production build  
npm run preview    # Preview production build
npm run test       # Run Vitest tests
npm run test:unit  # Run unit tests
npm run lint       # ESLint + Prettier linting
npm run format     # Format code with Prettier
npm run check      # Svelte type checking
```

**UI Tech Stack**:
- **Svelte 5.x + SvelteKit 2.x**: Full-stack framework with TypeScript support
- **Tailwind CSS 4.x**: Utility-first CSS framework with Vite plugin
- **DaisyUI 5.x**: Tailwind CSS component library for UI components
- **Vitest**: Testing framework with browser testing via Playwright
- **ESLint + Prettier**: Code linting and formatting with Svelte support
- **Marked**: Markdown parsing for analysis content rendering
- **Redis**: Client library for state management integration

**UI Structure**:
- `src/routes/+page.svelte`: Main research interface
- `src/routes/+layout.svelte`: App layout and navigation
- `src/routes/api/research/+server.ts`: SvelteKit API endpoint for research requests
- `src/routes/api/status-updates/+server.ts`: Real-time status updates endpoint

## Architecture

This is a **market research agent** for stock analysis using async flows with OpenAI Agents SDK, featuring a FastAPI backend and SvelteKit UI frontend.

### Key Architectural Principles

1. **Strict Separation of Concerns**:
   - **Flows** (`src/flows/`): Thin wrappers for async orchestration, contain NO business logic
   - **Tasks** (`src/tasks/`): Data orchestration only, contain NO business logic  
   - **Business Logic** (`src/research/`): All core research logic lives here

2. **Data Flow Architecture**:
   - Main flow: `src/flows/research_flow.py:main_research_flow()`
   - Core subflows: Historical earnings, financial statements, earnings projections, management guidance, forward PE analysis, news sentiment, trade ideas
   - **EPS Validation subflows**: Peer-relative EPS validation, market sentiment EPS check, technical EPS validation, EPS validation synthesis
   - Uses Alpha Vantage API for financial data (`src/lib/`)

3. **Model Management**:
   - Uses `litellm` for model abstraction (`src/lib/llm_model.py`)
   - Supports multiple Ollama models (Gemma 27B/12B/4B, GPT-OSS) and OpenAI models
   - Model selection via `MODEL_SELECTED` environment variable

4. **Full-Stack Application**:
   - **Backend**: FastAPI server (`server.py`) with `/health` and `/research` endpoints
   - **Frontend**: SvelteKit UI (`agent-ui/`) with Tailwind CSS and DaisyUI
   - **Infrastructure**: Docker Compose with Redis for caching/state management

### Research Pipeline

The agent performs comprehensive stock research through these sequential steps:
1. **Historical Earnings Analysis**: Establishes foundational baseline patterns
2. **Financial Statements Analysis**: Analyzes recent changes for projection accuracy
3. **Independent Earnings Projections**: Creates baseline projections for consensus validation
4. **Management Guidance Analysis**: Cross-checks against management guidance from earnings calls
5. **Peer Group Analysis**: Identifies comparable companies (enhanced with financial context)
6. **Forward PE Sanity Check**: Validates earnings data quality
7. **Forward PE Analysis**: Calculates valuation metrics (enhanced with projections and guidance)
8. **News Sentiment Analysis**: Analyzes recent news sentiment (enhanced with earnings context)
9. **EPS Validation Analysis**: Multi-method consensus validation using 6 independent approaches
10. **Cross-Reference Analysis**: Cross-validates insights across all previous analyses
11. **Trade Ideas Generation**: Synthesizes all analyses into actionable insights

### Enhanced EPS Validation System

The system employs a **comprehensive 6-method EPS validation approach** to provide robust consensus validation:

#### EPS Validation Methods

1. **Historical Earnings Analysis** (`src/research/historical_earnings/`):
   - Baseline patterns and predictability assessment
   - Beat/miss patterns and earnings quality trends
   - Provides foundational context for consensus reliability

2. **Independent Earnings Projections** (`src/research/earnings_projections/`):
   - Forward-looking fundamental analysis
   - Independent EPS reconstruction from financial drivers
   - Validation against Wall Street consensus

3. **Management Guidance Analysis** (`src/research/management_guidance/`):
   - Company-provided expectations and commentary
   - Management track record and guidance reliability
   - Insider perspective on earnings potential

4. **Peer-Relative EPS Validation** (`src/research/eps_validation/peer_relative_eps_validation_agent.py`):
   - Industry comparison using peer group forward P/E ratios
   - Implied EPS calculation from current stock price and peer valuations
   - Contextual validation considering company's relative positioning

5. **Market Sentiment EPS Check** (`src/research/eps_validation/market_sentiment_eps_check_agent.py`):
   - Revision momentum trends and analyst sentiment analysis
   - Whisper numbers vs. consensus expectations
   - Market expectation alignment with published estimates

6. **Technical EPS Validation** (`src/research/eps_validation/technical_eps_validation_agent.py`):
   - Price momentum and volume pattern analysis
   - Technical indicator-based EPS estimation
   - Chart pattern validation of consensus expectations

#### EPS Validation Verdicts

Each validation method provides one of four possible verdicts:

- **CONSENSUS_VALIDATED**: Method confirms consensus estimate accuracy (within ±3-5%)
- **CONSENSUS_TOO_HIGH**: Method suggests consensus is overly optimistic (>10% variance)
- **CONSENSUS_TOO_LOW**: Method suggests consensus is overly conservative (>10% variance)
- **INSUFFICIENT_DATA**: Method cannot provide reliable validation due to data limitations

#### EPS Validation Synthesis

The **EPS Validation Synthesis Agent** (`src/research/eps_validation/eps_validation_synthesis_agent.py`) combines all validation results:

- **Method Agreement Analysis**: Identifies consensus vs. disagreement across validation approaches
- **Confidence Scoring**: 0-1 scale based on method agreement and data quality
- **Overall Verdict**: Weighted synthesis considering method reliability and current context
- **Investment Implications**: Clear guidance on consensus reliability for investment decisions

#### Example EPS Validation Scenarios

**High Confidence Validation** (Score: 0.85-1.0):
```
Peer-Relative: CONSENSUS_VALIDATED (+1.7%)
Market Sentiment: CONSENSUS_VALIDATED (stable momentum)
Technical: CONSENSUS_VALIDATED (bullish momentum)
Overall Verdict: CONSENSUS_VALIDATED
Investment Implication: Strong confidence in consensus reliability
```

**Consensus Overoptimism** (Score: 0.70-0.85):
```
Peer-Relative: CONSENSUS_TOO_HIGH (-12.3%)
Market Sentiment: CONSENSUS_VALIDATED (mixed signals)
Technical: CONSENSUS_TOO_HIGH (bearish divergence)
Overall Verdict: CONSENSUS_TOO_HIGH
Investment Implication: Consider 15-20% haircut to consensus estimates
```

**Mixed Signals** (Score: 0.40-0.60):
```
Peer-Relative: CONSENSUS_TOO_HIGH (-8.7%)
Market Sentiment: CONSENSUS_VALIDATED (neutral)
Technical: CONSENSUS_TOO_LOW (strong momentum)
Overall Verdict: CONSENSUS_VALIDATED (low confidence)
Investment Implication: Monitor for additional data points before adjusting models
```

#### EPS Validation Components

**Models** (`src/research/eps_validation/eps_validation_models.py`):
- `PeerRelativeEpsValidation`: Peer comparison analysis results
- `MarketSentimentEpsCheck`: Sentiment and revision momentum analysis
- `TechnicalEpsValidation`: Technical analysis validation results
- `EpsValidationSynthesis`: Multi-method synthesis with overall verdict

**Agents** (`src/research/eps_validation/`):
- `peer_relative_eps_validation_agent.py`: Industry comparison specialist
- `market_sentiment_eps_check_agent.py`: Sentiment and momentum specialist
- `technical_eps_validation_agent.py`: Technical analysis specialist
- `eps_validation_synthesis_agent.py`: Multi-method synthesis specialist

**Tasks** (`src/tasks/eps_validation/`):
- `peer_relative_eps_validation_task.py`: Orchestrates peer comparison
- `market_sentiment_eps_check_task.py`: Orchestrates sentiment analysis
- `technical_eps_validation_task.py`: Orchestrates technical analysis
- `eps_validation_synthesis_task.py`: Orchestrates synthesis across methods

**Flows** (`src/flows/subflows/`):
- `peer_relative_eps_validation_flow.py`: Async flow with caching and status tracking
- `market_sentiment_eps_check_flow.py`: Async flow with caching and status tracking
- `technical_eps_validation_flow.py`: Async flow with caching and status tracking
- `eps_validation_synthesis_flow.py`: Async flow with caching and status tracking

**Cache Integration** (`src/tasks/cache_retrieval/`):
- Independent caching for each EPS validation method
- TTL-based invalidation aligned with earnings data freshness
- Cache utilities in `src/lib/eps_validation_cache_utils.py`

**Job Status Tracking** (`src/lib/job_tracker.py`):
- Real-time status updates for each validation method
- UI integration for progress monitoring during analysis

### Environment Variables

Required in `.env` file:
- `ALPHA_VANTAGE_API_KEY`: For financial data
- `OPENAI_API_KEY`: For AI model access (if using OpenAI)
- `MODEL_SELECTED`: Model choice (local_gemma27b, nord_gemma27b, local_gemma12b, nord_gemma12b, local_gemma4b, nord_gemma4b, local_gptoss, nord_gptoss, o4_mini)
- `LOCAL_OLLAMA_URL`/`NORD_OLLAMA_URL`: Ollama server URLs (when using Ollama models)

Optional in `.env` file:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8085)  
- `REDIS_URL`: Redis connection URL (default: redis://redis:6379/0)

### Testing Strategy

- Uses `pytest` with path configuration in `pyproject.toml`
- Test files in `tests/` directory with unit tests in `tests/unit/`
- Mocks external API calls to avoid hitting real APIs during tests
- **EPS Validation Testing** (`tests/unit/eps_validation/`):
  - Comprehensive test fixtures for all validation scenarios
  - Unit tests for models, agents, tasks, and flows
  - Integration tests for end-to-end EPS validation workflows
  - Mock validation results for testing synthesis logic

**Run EPS validation tests**:
```bash
uv run pytest tests/unit/eps_validation/ -v
```

## Development Guidelines

- When adding new research capabilities, put business logic in `src/research/`
- When adding new data sources, put integration code in `src/lib/`
- Keep flows and tasks as thin orchestration layers
- All new features must maintain the separation between orchestration and business logic
- Use `uv run` prefix for all Python commands
- Frontend development uses SvelteKit with TypeScript, Tailwind CSS, and DaisyUI components
- API endpoints follow REST conventions and return structured JSON responses
- All external API calls should be mocked in tests to avoid hitting real services

### EPS Validation Development Guidelines

- **Adding new validation methods**: Create agent in `src/research/eps_validation/`, task in `src/tasks/eps_validation/`, and flow in `src/flows/subflows/`
- **Validation verdicts**: Always use the `EpsValidationVerdict` enum for consistency
- **Confidence scoring**: Use 0-1 scale with clear methodology documented in agent instructions
- **Investment implications**: Include actionable guidance in all validation results
- **Cache integration**: Follow existing patterns in `src/tasks/cache_retrieval/` for new validation methods
- **Status tracking**: Add new job statuses to `src/lib/job_tracker.py` for UI integration
- **Testing**: Create comprehensive test coverage including fixtures, unit tests, and integration tests

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.