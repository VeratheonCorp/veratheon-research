# Market Research Agent

## Overview

This repository contains an AI Agent designed to research a given stock symbol's consensus EPS (Earnings Per Share) via forward PE and price target, specifically targeting the next quarterly earnings cycle.

## Architecture

- **Prefect-based Orchestration**  
  - **Flows**: Thin wrappers used primarily as handles for Prefect to control retries and scheduling. Flows do not contain business logic; they simply call Tasks. All flows are in `src/prefect/flows/`.
  - **Tasks**: Responsible for orchestrating all data handling and research steps. Tasks themselves do not contain business logic. All tasks are in `src/prefect/tasks/`.
  - **Business Logic**: All core business logic resides in `src/research/`.

- **Agents and Data Fetching**
  - Utilizes the OpenAI Agents SDK (not the Assistants API).
  - Main data fetching is performed using Alpha Vantage, with relevant code in `src/lib/`.

## Usage

- **Package Manager**:  
  This repo uses [`uv`](https://github.com/astral-sh/uv) from Astral for dependency management and process launching.  
  **Do not use** `pip` or `pipenv`.

- **Run the Project**:  
  ```bash
  uv run python run.py
  ```

## Directory Structure

```
.
├── run.py                  # Entry point for launching the agent
├── src/
│   ├── research/           # All business logic for research
│   └── lib/                # Alpha Vantage and other data fetching utilities
├── flows/                  # Prefect Flows (entry points for orchestration)
├── tasks/                  # Prefect Tasks (data orchestration, no business logic)
└── README.md               # This file
```

## Key Dependencies

- Prefect (workflow orchestration)
- OpenAI Agents SDK
- Alpha Vantage API
- uv (package manager)

## Environment Variables & dotenv

This repository uses the `python-dotenv` package to manage environment variables. Place a `.env` file in the root directory (alongside `run.py` and `README.md`). This file should contain your API keys and any other sensitive configuration, for example:

```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
OPENAI_API_KEY=your_openai_key
```

The `.env` file will be loaded automatically when running the project.

## Testing

This project uses **pytest** as the testing framework. All tests are located in the `tests/` directory, following standard Python testing conventions.

- To run all tests:
  ```bash
  uv run pytest
  ```
- Test files are organized by unit or integration level within the `tests/` directory (e.g., `tests/unit/`).
- Use mocks and fixtures as needed to isolate components and avoid hitting real APIs during test runs.

If you ask for tests to be written, they will be added to the appropriate location in `tests/` and use `pytest` style.

## Development Notes

- All orchestration should be handled via Prefect Flows and Tasks.
- All business logic must remain in `src/research/` for clarity and maintainability.
- Data fetching tools (like Alpha Vantage) are in `src/lib/`.
- If adding new features, maintain the separation between orchestration (Flows/Tasks) and business logic (src/research/).

## Future Work & Considerations

- If new data sources are added, place their integration logic in `src/lib/` and keep research logic in `src/research/`.
- If updating orchestration or retry logic, do so in the Flows/Tasks, not in business logic modules.
- Always use `uv` for dependency management and script execution.
