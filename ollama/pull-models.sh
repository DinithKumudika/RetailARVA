#!/bin/bash

# Start Ollama server in the background
ollama serve &

# Wait for Ollama server to start
sleep 5

# Pull llama 3 and nomic-embed
ollama pull llama3.1:latest
ollama pull gemma3:4b-it-qat
ollama pull nomic-embed-text:latest

# Wait for the Ollama server to finish 
wait $!