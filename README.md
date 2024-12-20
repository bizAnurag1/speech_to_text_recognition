# speech_to_text_recognition
## Audio File Processing with Folder Monitoring
This Python script is designed to monitor a folder for new MP3 files, automatically convert them to WAV format, and transcribe the audio into JSON files using asynchronous processing. Below is a detailed description of the script's functionality and usage.

## Features
Folder Monitoring: Watches a specified directory for new MP3 files using the watchdog library.
Audio Conversion: Converts MP3 files to WAV format for better compatibility with transcription systems.
Asynchronous Transcription: Transcribes audio files asynchronously for efficient processing.
Error Handling: Logs detailed information and errors during processing for debugging and monitoring.
Temporary File Handling: Uses a temporary directory to store intermediate files, ensuring the input folder remains clean.
Cleanup: Ensures temporary files are deleted after processing.

## Folder Structure
Input Directory: The folder where new MP3 files are added for processing.
Output Directory: The folder where transcribed JSON files are saved.
Default directories:

Input: data/input_audio
Output: data/transcriptions

## Code Overview
1. AudioFileHandler Class
Handles events triggered by the watchdog library. When a new MP3 file is detected:
It logs the detection.
It calls the asynchronous processing function to handle the file.

2. main Function
Processes a single audio file:
Copies the MP3 file to a temporary directory.
Converts the MP3 file to WAV format using the convert_mp3_to_wav function.
Transcribes the WAV file using the transcribe_audio function.

3. monitor_folder Function
Initializes the watchdog observer to monitor the input directory for new files.
Uses the AudioFileHandler class to process new files.

4. Logging and Error Handling
All operations are logged using the logging module for real-time monitoring.
Errors are recorded using a logging mechanism and an external log_entry function.

## How to Use
### Set Up the Environment:
Install the required Python packages:
pip install watchdog pydub pytz

Ensure your transcription function (transcribe_audio) and MP3-to-WAV conversion function (convert_mp3_to_wav) are implemented in the functions module.

### Run the Script:
Start the script to monitor the input folder:
python script_name.py

### Add Files:
Place MP3 files in the data/input_audio directory.
Transcriptions will be saved as JSON files in the data/transcriptions directory.

## Dependencies
watchdog: For folder monitoring.
pydub: For audio format conversion (requires ffmpeg or libav installed).
pytz: For timezone handling during logging.
Customization
Update the input and output directory paths in the if __name__ == "__main__" section.
Modify the transcription function (transcribe_audio) or conversion logic as needed.

## Error Handling
If errors occur during processing:
Check the logs for detailed error messages.
Ensure dependencies like ffmpeg are correctly installed.

## Future Improvements
Add support for monitoring subdirectories.
Implement multi-threading or queuing for processing large volumes of files.
Extend to handle other audio formats.