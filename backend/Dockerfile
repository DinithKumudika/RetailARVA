# Build the Python environment using Poetry
FROM python:3.11.0-slim AS builder

# Set working directory
WORKDIR /app

# Install Poetry using the official installation script
#RUN curl -sSL https://install.python-poetry.org | python3 -

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel && \
    pip --version

# Install Poetry
RUN pip install --no-cache-dir poetry && \
    poetry --version

# Add Poetry to PATH
#ENV PATH="/root/.local/bin:${PATH}"

# Copy only the files needed for Poetry to install dependencies
COPY pyproject.toml poetry.lock ./

# Install dependencies into the system Python environment
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main --no-interaction --no-ansi

# Create the final image
FROM python:3.11.0-slim

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the application code
COPY run.py ./
COPY src ./src

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "run.py"]