param (
     [string]$StaticDomain = "select-organic-lacewing.ngrok-free.app"
)

# Configuration Variables
$NGROK_AUTH_TOKEN = $env:NGROK_AUTH_TOKEN
$NGROK_STATIC_DOMAIN = $StaticDomain
$OLLAMA_MODEL_DIR = "C:\Users\Dinith\.ollama\models"
$OLLAMA_URL = "http://localhost:11434/"

# Function to check Ollama server status
function Check-ServerStatus {
     try {
          $response = Invoke-WebRequest -Uri $OLLAMA_URL -UseBasicParsing -ErrorAction Stop
          if ($response.StatusCode -eq 200) {
               Write-Host "Ollama server is running on localhost port 11434" -ForegroundColor Green
               return $true
          }
          else {
               Write-Host "Ollama server returned unexpected status: $($response.StatusCode)" -ForegroundColor Red
               return $false
          }
     }
     catch {
          Write-Host "Failed to connect to Ollama server." -ForegroundColor Red
          return $false
     }
}

# Function to run a command and stream output
function Run-Command {
     param (
          [string[]]$Command
     )

     # Start the process with redirected streams
     $process = Start-Process -FilePath $Command[0] -ArgumentList $Command[1..($Command.Length - 1)] `
          -NoNewWindow -PassThru -RedirectStandardOutput "stdout.log" -RedirectStandardError "stderr.log" `

     # Stream output from logs
     Start-Sleep -Seconds 2

     if (Test-Path "stdout.log") {
          Write-Host "Standard Output:" -ForegroundColor Green
          Get-Content -Path "stdout.log"
     }
     if (Test-Path "stderr.log") {
          Write-Host "Standard Error:" -ForegroundColor Yellow
          Get-Content -Path "stderr.log"
     }
}

# Main Script Execution
if (-not (Test-Path $OLLAMA_MODEL_DIR)) {
     Write-Host "Ollama is not installed. Exiting..." -ForegroundColor Red
     exit 1
}

# Set ngrok authentication
if (-not $NGROK_AUTH_TOKEN) {
     Write-Host "Ngrok authentication token is not set. Exiting..." -ForegroundColor Red
     exit 1
}

Run-Command -Command @("ngrok", "config", "add-authtoken", $NGROK_AUTH_TOKEN)

# Start Ollama server in the background
Write-Host "Starting Ollama server..." -ForegroundColor Cyan
$ollamaProcess = Start-Process -FilePath "ollama" -ArgumentList "serve" `
     -NoNewWindow -PassThru

# Wait for server startup
Start-Sleep -Seconds 5

try {
     if (Check-ServerStatus) {
          Write-Host "Starting Ngrok with static domain: $StaticDomain" -ForegroundColor Cyan
          Run-Command -Command @("ngrok", "http", "--log", "stdout", "11434", "--host-header", "localhost:11434", "--domain", $NGROK_STATIC_DOMAIN)
     }

     Write-Host "Ollama mapped to Ngrok static domain $NGROK_STATIC_DOMAIN" -ForegroundColor Green

     Write-Host "Press Ctrl+C to terminate the script and stop the Ollama server." -ForegroundColor Yellow
     
     # Keep the script running to allow the server and Ngrok to continue
     while ($true) {
          Start-Sleep -Seconds 10
     }
}
finally {
     Write-Host "Terminating Ollama server..." -ForegroundColor Yellow
     Stop-Process -Id $ollamaProcess.Id -Force

     if ($ngrokProcess) {
          Write-Host "Terminating Ngrok process..." -ForegroundColor Yellow
          Stop-Process -Id $ngrokProcess.Id -Force
     }
}

# Cleanup log files
Remove-Item -Path "stdout.log", "stderr.log" -ErrorAction SilentlyContinue