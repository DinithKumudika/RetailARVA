#!/bin/bash

# Define the name of the conda environment
ENV_NAME="rag-eval"

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Conda (Miniconda or Anaconda) first."
    exit 1
fi

# Create and activate the conda environment
echo "Creating and activating conda environment: $ENV_NAME"
conda create -n "$ENV_NAME" python=3.10 -y
conda activate "$ENV_NAME"

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "Failed to activate conda environment. Exiting."
    exit 1
fi

# Set OLLAMA environment variables
echo "Setting OLLAMA environment variables..."
mkdir -p "$CONDA_PREFIX/etc/conda/activate.d"
cat <<EOL > "$CONDA_PREFIX/etc/conda/activate.d/env_vars.sh"
export OLLAMA_EMBEDDING_MODEL_ID="nomic-embed-text" 
export OLLAMA_CHAT_MODEL_ID="llama3"                
EOL

# Install jq via conda
echo "Installing jq via conda..."
conda install -c conda-forge jq -y

# Install Python packages via pip
echo "Installing Python packages via pip..."
pip install -U deepeval langchain langchain-community langchain-core "ollama<0.4.0" langchain-ollama

# Verify installation
echo "Verifying installations..."
python -c "import deepeval; import langchain; import langchain_community; import langchain_core; import ollama; print('All packages installed successfully.')"



echo "Setup complete! Activate the environment with 'conda activate $ENV_NAME'."
echo "NOTE: OLLAMA models are set to defaults (nomic-embed-text and llama3). Modify them in:"
echo "$CONDA_PREFIX/etc/conda/activate.d/env_vars.sh"