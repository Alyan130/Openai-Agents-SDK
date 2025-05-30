FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv (faster Python package installer)
RUN pip install uv

# Copy project files
COPY . .

# Install Python dependencies using uv
# If you have a pyproject.toml file:
RUN if [ -f pyproject.toml ]; then \
        uv pip compile pyproject.toml --output-file=requirements.txt --system; \
    fi

# Install dependencies
RUN if [ -f requirements.txt ]; then \
        uv pip install --system -r requirements.txt; \
    else \
        uv pip install --system chainlit; \
    fi

# Create a non-root user for security
RUN useradd -m -u 1000 chainlituser && \
    chown -R chainlituser:chainlituser /app

# Switch to non-root user
USER chainlituser

# Expose port (Hugging Face Spaces uses 7860 by default)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Set environment variables for the container
ENV PYTHONUNBUFFERED=1
ENV CHAINLIT_HOST=0.0.0.0
ENV CHAINLIT_PORT=7860

# Create a startup script that sources environment variables
RUN echo '#!/bin/bash\nset -e\necho "Starting Chainlit app..."\necho "Environment variables set:"\nenv | grep -E "(API|KEY)" || echo "No API/KEY variables found"\nexec "$@"' > /app/start.sh && \
    chmod +x /app/start.sh

# Run Chainlit application with startup script
CMD ["/app/start.sh", "chainlit", "run", "agent.py", "--host", "0.0.0.0", "--port", "7860", "--headless"]