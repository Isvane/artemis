# --- Stage 1: Build Stage ---
# Using the pre-baked python3.12 bookworm-slim variant of uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
# Disable automatic downloads; we rely strictly on the system's Python 3.12
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /workspace

# Install dependencies only (cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

# Copy the actual app folder and source code
COPY ./app /workspace/app
COPY ./pyproject.toml ./uv.lock /workspace/

# Final sync to install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable


# --- Stage 2: Final Runtime ---
# Mirroring the exact base Python/OS version to keep paths perfectly aligned
FROM python:3.12-slim-bookworm

# Setup non-root user for security
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy ONLY the workspace. It contains the self-contained .venv
# linked cleanly to the identical system Python interpreter.
COPY --from=builder --chown=nonroot:nonroot /workspace /workspace

# Set environment variables
ENV PATH="/workspace/.venv/bin:$PATH"
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace
USER nonroot

# Run the uvicorn server pointing to your app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--reload"]
