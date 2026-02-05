# ============================================================================
# Project Chimera: Dockerfile
# ============================================================================
# Multi-stage build for optimized production container
# 
# Usage:
#   docker build -t project-chimera:latest .
#   docker run -it project-chimera:latest
#
# Tech Stack:
#   - Python 3.11+ (required for modern type hints)
#   - uv package manager (fast dependency resolution)
#   - pydantic-ai, MCP SDK, Redis, Weaviate, PostgreSQL clients
# ============================================================================

# ============================================================================
# STAGE 1: Base Image with System Dependencies
# ============================================================================
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
# - curl: for health checks and downloading
# - git: for version control (optional, useful for CI/CD)
# - build-essential: for compiling Python packages with C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash chimera && \
    mkdir -p /app && \
    chown -R chimera:chimera /app

# Set working directory
WORKDIR /app

# ============================================================================
# STAGE 2: Python Dependencies Installation
# ============================================================================
FROM base AS dependencies

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy dependency files
COPY --chown=chimera:chimera pyproject.toml ./

# Install Python dependencies using uv
# uv is much faster than pip for dependency resolution
RUN uv pip install --system --no-cache -r pyproject.toml

# Install development dependencies (for testing in container)
RUN uv pip install --system --no-cache \
    pytest>=8.1.0 \
    pytest-asyncio>=0.23.0 \
    pytest-cov>=5.0.0 \
    pytest-mock>=3.14.0 \
    black>=24.3.0 \
    ruff>=0.4.0 \
    mypy>=1.10.0 \
    structlog>=24.1.0

# ============================================================================
# STAGE 3: Application Code
# ============================================================================
FROM dependencies AS application

# Switch to non-root user
USER chimera

# Copy application code
COPY --chown=chimera:chimera . /app/

# Create necessary directories if they don't exist
RUN mkdir -p /app/logs /app/data /app/.cache

# Validate project structure
RUN test -d /app/specs && \
    test -d /app/skills && \
    test -d /app/tests && \
    echo "✅ Project structure validated"

# ============================================================================
# STAGE 4: Production Runtime
# ============================================================================
FROM application AS production

# Set production environment variables
ENV ENVIRONMENT=production \
    LOG_LEVEL=INFO

# Expose ports (if needed for API/Dashboard)
# 8000: FastAPI application (optional dashboard)
# 8080: Weaviate (if running in same container - not recommended)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command: Run tests
# Override this in docker-compose or when running container
CMD ["pytest", "tests/", "-v"]

# ============================================================================
# STAGE 5: Development Runtime
# ============================================================================
FROM application AS development

# Set development environment variables
ENV ENVIRONMENT=development \
    LOG_LEVEL=DEBUG

# Install development tools
USER root
RUN uv pip install --system --no-cache \
    ipython>=8.12.0 \
    jupyter>=1.0.0

USER chimera

# Expose additional ports for development
EXPOSE 8000 8888

# Default command: Interactive shell
CMD ["/bin/bash"]

# ============================================================================
# Build Instructions
# ============================================================================
# 
# Build production image:
#   docker build --target production -t project-chimera:latest .
#
# Build development image:
#   docker build --target development -t project-chimera:dev .
#
# Run tests:
#   docker run --rm project-chimera:latest
#
# Run interactive development:
#   docker run -it --rm -v $(pwd):/app project-chimera:dev
#
# Run with environment file:
#   docker run --rm --env-file .env project-chimera:latest
#
# ============================================================================
# In dependencies stage - fix uv usage:
RUN uv pip install --system --no-cache "$(cat pyproject.toml | grep -A 100 '^\[project\]')"

# Or use requirements.txt instead:
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt