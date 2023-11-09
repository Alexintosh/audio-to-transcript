import os
import sys
import logging
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio = None
        self.segments = []
        self.transcripts = []
        self.ten_minutes = 10 * 60 * 1000  # 10 minutes in milliseconds
        self.output_directory = self.create_output_directory()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  # Load API key from environment
        
    def load_audio(self):
        try:
            self.audio = AudioSegment.from_file(self.file_path)
            logging.info("Audio file loaded")
        except Exception as e:
            logging.error(f"Failed to load audio file: {e}")
            sys.exit(1)
    
    def create_output_directory(self):
        original_file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        output_directory = os.path.join(os.getcwd(), original_file_name)
        os.makedirs(output_directory, exist_ok=True)
        logging.info(f"Output directory created: {output_directory}")
        return output_directory

    def split_audio(self):
        for i in range(0, len(self.audio), self.ten_minutes):
            segment_index = i // self.ten_minutes
            logging.info(f"Processing segment: {segment_index}")
            segment = self.audio[i:i + self.ten_minutes]
            self.segments.append((segment_index, segment))

    def save_segments(self):
        for index, segment in self.segments:
            segment_file_name = f"{os.path.splitext(os.path.basename(self.file_path))[0]}_segment_{index}.mp3"
            segment_file_path = os.path.join(self.output_directory, segment_file_name)
            segment.export(segment_file_path, format="mp3")
            logging.info(f"Segment saved: {segment_file_path}")

    def transcribe_segments(self):
        for index, _ in self.segments:
            segment_file_name = f"{os.path.splitext(os.path.basename(self.file_path))[0]}_segment_{index}.mp3"
            segment_file_path = os.path.join(self.output_directory, segment_file_name)
            try:
                with open(segment_file_path, "rb") as audio_segment:
                    response = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_segment
                    )
                    # Assuming the response contains a 'text' attribute with the transcription
                    transcript = response['text'] if 'text' in response else ""
                    logging.info(f"Transcription completed for segment: {index}")
                    self.transcripts.append(transcript)
            except Exception as e:
                logging.error(f"Transcription failed for segment {index}: {e}")
                self.transcripts.append("")  # Append an empty string if transcription fails

    def save_transcripts(self):
        full_transcript = "\n".join(self.transcripts)
        transcript_file_path = os.path.join(self.output_directory, f"{os.path.splitext(os.path.basename(self.file_path))[0]}_transcript.txt")
        with open(transcript_file_path, 'w') as transcript_file:
            transcript_file.write(full_transcript)
        logging.info(f"Full transcript saved: {transcript_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("You must provide the path to the audio file as an argument")
        sys.exit(1)
    
    audio_file_path = sys.argv[1]
    processor = AudioProcessor(audio_file_path)
    processor.load_audio()
    processor.split_audio()
    processor.save_segments()
    processor.transcribe_segments()
    processor.save_transcripts()
