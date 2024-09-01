import os
import asyncio
import subprocess
import requests
import time

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
NGROK_STATIC_DOMAIN = 'select-organic-lacewing.ngrok-free.app'
OLLAMA_MODEL_DIR = r'C:\Users\Dinith\.ollama\models'
OLLAMA_URL = 'http://localhost:11434/'

def check_server_status():
     try:
          response = requests.get(OLLAMA_URL)
          if response.status_code == 200:
               print("Ollama server is running.")
               return True
          else:
               print(f"Ollama server returned unexpected status: {response.status_code}")
               return False
     except requests.ConnectionError:
          print("Failed to connect to Ollama server.")
          return False

# Define run - a helper function to run subcommands asynchronously.
# The function takes in 2 arguments:
#  1. command
#  2. environment variable for Ollama
async def run(cmd, env=None):
     print(">>> starting", *cmd)
     p = await asyncio.subprocess.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
     )

     # This function is designed to handle large amounts of text data efficiently.
     # It asynchronously iterate over lines and print them, stripping and decoding as needed.
     async def pipe(lines):
          async for line in lines:
               print(line.strip().decode("utf-8"))

     # Gather the standard output (stdout) and standard error output (stderr) streams of a subprocess and pipe them through
     # the `pipe()` function to print each line after stripping whitespace and decoding UTF-8.
     # This allows us to capture and process both the standard output and error messages from the subprocess concurrently.
     await asyncio.gather(
          pipe(p.stdout),
          pipe(p.stderr),
     )

async def main():
     # Set the environment variables for ollama serve
     # Variable OLLAMA_MODELS redefines the path for model storage (from Colab to Google Drive)
     ollama_env = os.environ.copy()

     if not os.path.exists(OLLAMA_MODEL_DIR):
          print("Ollama is not installed...")
          exit()

     ollama_env["OLLAMA_MODELS"] = OLLAMA_MODEL_DIR
     print(ollama_env["OLLAMA_MODELS"])

     # Authenticate with Ngrok
     await run(["ngrok", "config", "add-authtoken", NGROK_AUTH_TOKEN])


     # Start Ollama server in the background
     ollama_process = subprocess.Popen(['ollama', 'serve'], env=ollama_env)

     # Give the server a few seconds to start
     time.sleep(5)
     
     try:

          if check_server_status():
               print("Starting Ngrok...")


          await run(['ngrok', 'http', '--log', 'stderr', '11434', '--host-header', 'localhost:11434', '--domain', NGROK_STATIC_DOMAIN]),
     finally:
          ollama_process.terminate()

if __name__ == "__main__":
     asyncio.run(main())


