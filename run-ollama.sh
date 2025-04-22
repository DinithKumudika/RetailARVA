#!/bin/bash

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Error: Ollama is not installed. Please install it from https://ollama.com" >&2
    exit 1
fi

# Define models to pull
models=("pull llama3.1:latest" "pull nomic-embed-text:latest")

# Pull models if not already present
for model in "${models[@]}"; do
    echo "Checking for model: $model"
    
    # Check if model already exists
    if ollama show "$model" &> /dev/null; then
        echo "Model '$model' is already installed."
    else
        echo "Pulling model: $model..."
        if ollama pull "$model"; then
            echo "Successfully pulled '$model'."
        else
            echo "Error: Failed to pull model '$model'." >&2
            exit 1
        fi
    fi
done

echo "All specified models have been processed successfully."