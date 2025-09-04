# ---- Builder Stage ----
# Using Alpine for a smaller footprint and better security
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build-time system dependencies using Alpine's package manager
RUN apk add --no-cache \
    build-base \
    curl

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies into the venv
COPY requirements.txt .

# Upgrade build tools first, then install requirements
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip check


# ---- Final Stage ----
# Starting from a fresh Alpine image for the final product
FROM python:3.12-alpine

WORKDIR /app

# Create a non-root user (using Alpine's 'adduser')
RUN addgroup -S appuser && adduser -S -G appuser appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code with correct permissions
COPY --chown=appuser:appuser . .

# Create necessary directories and set permissions
RUN mkdir -p uploads /app/celery_beat_data \
    && chown -R appuser:appuser /app/uploads /app/celery_beat_data

# Switch to the non-root user
USER appuser

# Set environment variables for runtime
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Health check using Alpine's 'wget' (pre-installed in this base image)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:8000/health || exit 1

# Default command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]