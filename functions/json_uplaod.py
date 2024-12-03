import os
import json
import logging
from functions.log_entry import insert_log_entry

def upload_json_content_to_local(json_content, original_filename, local_directory):
    try:
        logging.info("Initializing local JSON upload.")
        insert_log_entry("INFO", "Initializing local JSON upload.", source="upload_json_content_to_local")
        
        # Ensure the directory exists
        if not os.path.exists(local_directory):
            os.makedirs(local_directory)
            logging.info(f"Created directory '{local_directory}'.")
            insert_log_entry("INFO", f"Created directory '{local_directory}'.", source="upload_json_content_to_local")
        
        # Generate the new filename by replacing the extension
        json_filename = original_filename.replace('.mp3', '.json')
        json_filepath = os.path.join(local_directory, json_filename)

        logging.info(f"Saving JSON content to local file '{json_filepath}'.")
        insert_log_entry("INFO", f"Saving JSON content to local file '{json_filepath}'.", {'filename': original_filename}, source="upload_json_content_to_local")
        
        # Write JSON content to file
        with open(json_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(json_content, json_file, ensure_ascii=False, indent=4)
        
        logging.info(f"Successfully saved JSON content for '{original_filename}' to local folder.")
        insert_log_entry("INFO", f"Successfully saved JSON content for '{original_filename}' to local folder.", source="upload_json_content_to_local")
    except Exception as e:
        logging.error(f"Failed to save JSON content locally: {e}")
        insert_log_entry("ERROR", "Failed to save JSON content locally", {'error': str(e)}, source="upload_json_content_to_local")
