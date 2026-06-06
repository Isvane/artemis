# --- Stage 1: Build Stage ---
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python 3.14 (Standalone build)
RUN uv python install 3.14

WORKDIR /workspace

# Install dependencies only (cached until pyproject.toml or uv.lock changes)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the actual app folder and source code
COPY ./app /workspace/app
COPY ./pyproject.toml ./uv.lock /workspace/

# Final sync to install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# --- Stage 2: Final Runtime ---
FROM debian:bookworm-slim

# Setup non-root user for security
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy standalone Python and the app workspace environment
COPY --from=builder /python /python
COPY --from=builder --chown=nonroot:nonroot /workspace /workspace

# Set environment variables
ENV PATH="/workspace/.venv/bin:$PATH"
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace
USER nonroot

# Run the uvicorn server pointing to app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--reload"]
