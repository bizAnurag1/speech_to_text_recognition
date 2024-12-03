import logging
import os
import time
import asyncio
import tempfile
from functions import transcribe_audio as ta
from functions import log_entry as le
from functions import convert_mp3_to_wav as mw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioFileHandler(FileSystemEventHandler):
    def __init__(self, process_function, output_directory):
        """
        Initialize the file handler.
        Args:
            process_function (function): The function to process new files.
            output_directory (str): The directory where processed files will be saved.
        """
        self.process_function = process_function
        self.output_directory = output_directory

    def on_created(self, event):
        """
        Triggered when a new file is created in the monitored folder.
        Args:
            event (FileSystemEvent): Event data containing file details.
        """
        if event.is_directory:
            return  # Ignore directories
        if event.src_path.endswith(".mp3"):  # Only process MP3 files
            logging.info(f"Detected new file: {event.src_path}")
            asyncio.run(self.process_function(event.src_path, self.output_directory))


# async def main(blob: func.InputStream, context: func.Context):
async def main(input_file_path, output_directory):
    """
    Local version of the main function for processing an audio file.
    Args:
        input_file_path (str): Path to the input MP3 file.
        output_directory (str): Directory to save the output transcription JSON files.
    """
    try:
        logging.info(f"Processing local file: {input_file_path}")
        
        filename = os.path.basename(input_file_path)
        temp_dir = tempfile.gettempdir()  # Use a temporary directory for intermediate files
        mp3_file_path = os.path.join(temp_dir, filename)
        wav_file_path = mp3_file_path.replace('.mp3', '.wav')

        # Copy the input MP3 file to the temporary directory
        logging.info("Copying input file to temporary directory.")
        with open(input_file_path, "rb") as input_file, open(mp3_file_path, "wb") as temp_file:
            temp_file.write(input_file.read())

        # Convert MP3 to WAV
        logging.info("Converting MP3 to WAV.")
        duration = mw.convert_mp3_to_wav(mp3_file_path, wav_file_path)

        # Process and transcribe the WAV file
        await ta.transcribe_audio(wav_file_path, filename, duration, output_directory)
    except Exception as e:
        logging.error(f"Error during audio processing: {e}")
        le.insert_log_entry(
            "INFO",
            "Error during audio processing",
            {'error': str(e)},
            source="process_audio_file",
        )
    # finally:
    #     logging.info("Starting cleanup process...")

    #     # Clean up temporary files
    #     if os.path.exists(mp3_file_path):
    #         os.remove(mp3_file_path)
    #     if os.path.exists(wav_file_path):
    #         os.remove(wav_file_path)

    #     logging.info("Cleanup complete.")

def monitor_folder(input_directory, output_directory):
    """
    Monitors a folder for new MP3 files and processes them automatically.
    Args:
        input_directory (str): Folder to monitor for new files.
        output_directory (str): Folder to save processed output.
    """
    logging.info(f"Starting to monitor folder: {input_directory}")
    event_handler = AudioFileHandler(main, output_directory)
    observer = Observer()
    observer.schedule(event_handler, input_directory, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        logging.info("Stopping folder monitoring.")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Define directories
    input_directory = "data/input_audio"
    output_directory = "data/transcriptions"

    # Ensure directories exist
    os.makedirs(input_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)

    # Start monitoring
    monitor_folder(input_directory, output_directory)