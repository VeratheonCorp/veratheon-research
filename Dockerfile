# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only project metadata first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Sync dependencies using uv (no dev deps). This creates a .venv
RUN uv sync --no-dev

ENV PATH="/app/.venv/bin:${PATH}"

# Now copy the rest of the application code
COPY . .

# Expose API port
EXPOSE 8085

# Default command can be overridden by compose
CMD ["python", "server.py"]
