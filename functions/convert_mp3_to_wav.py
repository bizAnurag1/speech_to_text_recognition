import logging
from functions.log_entry import insert_log_entry
from functions.file_extension import check_file_and_extension
from moviepy.editor import AudioFileClip

def convert_mp3_to_wav(mp3_path, wav_path):
    try:
        message = f"Converting MP3 file '{mp3_path}' to WAV format."
        logging.info(message)
        insert_log_entry("INFO", message, {'mp3_path': mp3_path}, source="convert_mp3_to_wav")

        audio_clip = AudioFileClip(mp3_path)
        audio_clip.write_audiofile(wav_path, nbytes=2, fps=16000, codec="pcm_s16le", bitrate="5k")
        duration = audio_clip.duration

        message = f"Conversion complete. WAV file saved at '{wav_path}' with duration {duration} seconds."
        logging.info(message)
        insert_log_entry("INFO", message, {'wav_path': wav_path, 'duration': duration}, source="convert_mp3_to_wav")

        check_file_and_extension(wav_path)
        return format(duration / 60, '.2f')
    except Exception as e:
        logging.error(f"Failed to convert MP3 to WAV: {e}")
        insert_log_entry("ERROR", "Failed to convert MP3 to WAV", {'mp3_path': mp3_path, 'error': str(e)}, source="convert_mp3_to_wav")
        raise