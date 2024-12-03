from functions.log_entry import insert_log_entry
import logging
import os

def check_file_and_extension(path):
    if os.path.isfile(path):
        message = f"{path} is a file."
        logging.info(message)
        insert_log_entry("INFO", message, source="check_file_and_extension")
        
        _, extension = os.path.splitext(path)
        if extension:
            message = f"The file's extension is: {extension}"
            logging.info(message)
            insert_log_entry("INFO", message, source="check_file_and_extension")
        else:
            message = "The file does not have an extension."
            logging.info(message)
            insert_log_entry("INFO", message, source="check_file_and_extension")
    else:
        message = f"{path} is not a file or does not exist."
        logging.warning(message)
        insert_log_entry("WARNING", message, source="check_file_and_extension")