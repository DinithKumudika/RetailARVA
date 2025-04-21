#!/bin/bash

# Start Ollama server in the background
ollama serve &

# Wait for Ollama server to start
sleep 5

ollama llama3.3:70b-instruct-q4_K_M

# Wait for the Ollama server to finish 
wait $!