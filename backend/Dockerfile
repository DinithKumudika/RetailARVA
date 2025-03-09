# Build the Python environment using Poetry
FROM python:3.11.0-slim AS builder

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only the files needed for Poetry to install dependencies
COPY pyproject.toml poetry.lock ./

# Install dependencies into a virtual environment
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev --no-interaction --no-ansi

# Create the final image
FROM python:3.11.0-slim

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy the application code
COPY run.py ./
COPY src ./src

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"]
