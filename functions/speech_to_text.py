import os
import tempfile
import asyncio
import logging
import azure.cognitiveservices.speech as speechsdk
from functions.log_entry import insert_log_entry

async def perform_speech_to_text(audio_file, timeout):
    try:
        speech_key = os.environ['AZURE_SPEECH_SUBSCRIPTION_KEY']
        service_region = os.environ['AZURE_SERVICE_REGION']

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_recognition_language = "en-US"

        temp_dir = tempfile.gettempdir()
        logfile = os.path.join(temp_dir, "speechtotextlog.txt")
        speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, logfile)

        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        recognized_text = []
        recognition_done = asyncio.Event()

        def speech_recognized(event_args):
            recognized_text.append(event_args.result.text)
            logging.info(f"Resulted_text :::: {event_args.result.text}")

        def recognizing(event_args):
            if event_args.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                pass
            elif event_args.result.reason == speechsdk.ResultReason.NoMatch:
                pass
            elif event_args.result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = event_args.result.cancellation_details
                logging.info(f"Recognition canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logging.info(f"Error details: {cancellation_details.error_details}")

                speech_recognizer.stop_continuous_recognition()

        def recognition_completed(event_args):
            recognition_done.set()  # Signal completion of recognition
            logging.info("Recognition session completed.")

        speech_recognizer.recognized.connect(speech_recognized)
        speech_recognizer.recognizing.connect(recognizing)
        speech_recognizer.session_stopped.connect(recognition_completed)

        # await asyncio.sleep(5)  # Add a delay to give time for speech recognition to start
        logging.info("Starting continuous recognition...")

        speech_recognizer.start_continuous_recognition()
        await asyncio.wait_for(recognition_done.wait(), timeout=timeout)  # Wait until recognition is complete

        speech_recognizer.stop_continuous_recognition()
        return recognized_text
    except asyncio.TimeoutError:
        message = f"Speech recognition timed out after {timeout} seconds."
        logging.warning(message)
        insert_log_entry("WARNING", message, {'timeout': timeout},filename=audio_file, source="perform_speech_to_text")
    except Exception as e:
        logging.error(f"Speech recognition failed: {e}")
        insert_log_entry("ERROR", "Speech recognition failed", {'audio_file': audio_file, 'error': str(e)}, filename=audio_file,source="perform_speech_to_text")