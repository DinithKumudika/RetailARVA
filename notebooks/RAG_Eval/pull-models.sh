#!/bin/bash

# Start Ollama server in the background
ollama serve &

# Wait for Ollama server to start
sleep 5

# Pull llama 3 and nomic-embed
ollama pull bge-large
ollama pull nomic-embed-text:latest

# Wait for the Ollama server to finish 
wait $!