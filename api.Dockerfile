FROM python:3.11.0-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src .
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

ENV USE_GROQ=False
ENV USE_OLLAMA=True
ENV USE_GEMINI=False
ENV USE_HUGGINGFACE_EMBEDDING=False
ENV USE_GOOGLE_EMBEDDING=False
ENV USE_OLLAMA_EMBEDDING=True

ENV OLLAMA_URL="http://localhost:11434"
ENV OLLAMA_MODEL_ID="llama3.1:latest"
ENV OLLAMA_EMBEDDING_MODEL_ID="nomic-embed-text:latest"

ENV GEMINI_MODEL_ID="gemini-1.5-flash"
ENV GEMINI_EMBEDDING_MODEL_ID="llama3.1:latest"
ENV GOOGLE_GENERATIVE_LANGUAGE_API_KEY="AIzaSyDpcYeeReEC_IdaiNRtMJLfqTJpX74ZtLI"

ENV GROQ_API_KEY="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"
ENV GROQ_MODEL_ID="llama-3.1-8b-instant"
ENV HUGGINGFACE_EMBEDDING_MODEL_ID="BAAI/bge-large-en-v1.5"

ENV QDRANT_API_KEY="drmITqgpRoFSiZqHR7GHrTc5fLWELgYCENyqhKS2GgiXcGroEsQhqQ"
ENV QDRANT_CLUSTER_URL="https://58c8568b-8331-409a-bb60-9d8f04bd4ddd.us-east4-0.gcp.cloud.qdrant.io"

ENV DATABASE_URL="sqlite:///./database/db.db"

ENV GRADIO_URL="http://127.0.0.1:7860"
ENV GRADIO_PORT=7860

ENV LANGCHAIN_TRACING_V2=true
ENV LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
ENV LANGCHAIN_API_KEY="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"
ENV LANGCHAIN_PROJECT="retailarva-chatbot"

CMD ["python", "app.py"]