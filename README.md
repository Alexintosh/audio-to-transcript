# Audio Transcription Tool

## Overview
This tool automates the transcription of audio files. It takes an MP3 file, splits it into 10-minute segments, transcribes each segment using OpenAI's Whisper API, and compiles the transcriptions into a single text file.

## Features
- Splits audio files into 10-minute segments.
- Transcribes audio segments using OpenAI's Whisper API.
- Compiles transcriptions into a single text file.
- Avoids data overwrite without user confirmation.

## Getting Started

### Prerequisites
- Python 3.6 or higher.
- pip for installing dependencies.
- Virtualenv for creating an isolated Python environment (optional, but recommended).
- An OpenAI API key with access to the Whisper API.

### Installation
1. Clone the repository to your local machine.
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. (Optional) Create a virtual environment to isolate the project dependencies. Replace `env_name` with your desired environment name.
    ```sh
    python3 -m venv env_name
    ```

3. Activate the virtual environment.
   - On macOS and Linux:
    ```sh
    source env_name/bin/activate
    ```
   - On Windows:
    ```cmd
    .\env_name\Scripts\activate
    ```

4. Install the required Python packages within the activated virtual environment.
    ```sh
    pip install -r requirements.txt
    ```

5. Set up your OpenAI API key by creating a `.env` file in the root directory and adding your key to it.
    ```sh
    echo OPENAI_API_KEY='your-api-key' > .env
    ```

### Usage
Activate your virtual environment if it is not already activated and run the script with the path to your audio file.
    ```sh
    source env_name/bin/activate  # On macOS and Linux
    .\env_name\Scripts\activate   # On Windows
    python main.py path_to_your_audio_file.mp3
    ```

The script will process the audio file, transcribe it, and save the transcription in a dedicated directory named after the audio file.

## Configuration
- To adjust the length of audio segments, modify the `ten_minutes` variable in the `AudioProcessor` class.

## Contributing
We welcome contributions! Please fork the repository and submit a pull request with your suggested changes.

## License
This project is released under the [MIT License](LICENSE).
