import logging
import os
from functions.speech_to_text import perform_speech_to_text
from functions.json_uplaod import upload_json_content_to_local

async def transcribe_audio(file_path, filename, duration, local_directory):
    audio_duration_seconds = float(duration) * 60  # Convert minutes to seconds
    timeout = audio_duration_seconds + 5
    logging.info(f"Using a dynamic timeout of {timeout} seconds for transcription.")
   
    # Perform the transcription (assuming st.perform_speech_to_text is a valid function for this)
    transcription = await perform_speech_to_text(audio_file=file_path, timeout=timeout)
    if transcription:
        logging.info(f"Transcription success for {file_path}: {''.join(transcription)}")
    else:
        logging.warning(f"No transcription result for {file_path}")
    
    logging.info(f"Transcription_Status : {transcription}")
    
    # Save transcription result to a local JSON file
    transcription_data = {
        'filename': os.path.basename(filename),
        'call_duration': float(duration)*60,
        'response_text': ''.join(transcription)
    }
    
    upload_json_content_to_local(transcription_data, filename, local_directory)
    logging.info(f"{filename} has been saved to the local directory: {local_directory}")