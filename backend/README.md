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