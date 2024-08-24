### Installation

#### Google Cloud Setup
1. follow the instructions on https://cloud.google.com/sdk/docs/install-sdk to install Google Cloud CLI for your OS
2. run `gcloud init` to initialize glcloud CLI and authenticate with your google account
3. select the cloud project associated with the google APIs you are using
4. run `gcloud auth application-default login` to create local authentication credentials for your Google Account

#### Unable to install playsound using pip
subprocess-exited-with-error occurs when run `pip install playsound`
1. first update the wheel package using `pip install --upgrade wheel`
2. then run `pip install playsound` again

#### Llama3.1 Setup
1. Install Ollama this [link](https://ollama.com/download).
2. Install the [Llama3.1](https://ollama.com/library/llama3.1) 8b model using the following command: `ollama pull llama3.1`
3. Use `ollama serve` command to run the model as an API in the localhost (16 GB ram is required to run the model).