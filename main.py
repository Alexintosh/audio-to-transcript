from openai import OpenAI
from pydub import AudioSegment
import os
import sys
import logging

client = OpenAI()


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if len(sys.argv) < 2:
    logging.error("You must provide the path to the audio file as an argument")
    sys.exit(1)

# The first command line arg is the path to the audio file
path_to_audio_file = sys.argv[1]
logging.info(f"Processing file: {path_to_audio_file}")

# Load the audio file
try:
    audio = AudioSegment.from_file(path_to_audio_file)
    logging.info("Audio file loaded")
except Exception as e:
    logging.error(f"Failed to load audio file: {e}")
    sys.exit(1)


# Define the length of each split in milliseconds
ten_minutes = 10 * 60 * 1000

# Extract the original file name without the extension
original_file_name = os.path.splitext(os.path.basename(path_to_audio_file))[0]

# Create a directory for the original file name if it doesn't exist
output_directory = os.path.join(os.getcwd(), original_file_name)
os.makedirs(output_directory, exist_ok=True)
logging.info(f"Output directory created: {output_directory}")

# Initialize an empty list to hold all transcripts
transcripts = []

# Loop over the audio in 10-minute increments
for i in range(0, len(audio), ten_minutes):
    segment_index = i // ten_minutes
    logging.info(f"Processing segment: {segment_index}")
    
    # Extract the 10-minute segment
    segment = audio[i:i+ten_minutes]
    
    # Construct the new file name
    segment_file_name = f"{original_file_name}_segment_{segment_index}.mp3"
    
    # Path for the new file
    segment_file_path = os.path.join(output_directory, segment_file_name)
    
    # Save the segment in the new directory
    segment.export(segment_file_path, format="mp3")
    logging.info(f"Segment saved: {segment_file_path}")
    
    # Call the Whisper API for transcription (pseudo-code, replace with actual code)
    # Make sure to include error handling here
    try:
        # This is a placeholder for the transcription code.
        # You would have to replace this with the actual call to the Whisper API.
        logging.info(f"Starting Transcription for segment: {segment_index}")
        audio_segment = open(segment_file_path, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_segment
        )
        logging.info(f"Transcription completed for segment: {segment_index}")
    except Exception as e:
        logging.error(f"Transcription failed for segment {segment_index}: {e}")
        transcript = ""

    # Append the transcript to the transcripts list
    transcripts.append(transcript.text)

# Join all transcripts into a single text
full_transcript = "\n".join(transcripts)

# Save the full transcript into a single text file
transcript_file_path = os.path.join(output_directory, f"{original_file_name}_transcript.txt")
with open(transcript_file_path, 'w') as transcript_file:
    transcript_file.write(full_transcript)
logging.info(f"Full transcript saved: {transcript_file_path}")



# print(transcript)