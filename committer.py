# committer.py

import time
import logging
import shutil
import os

from data_process.file_handler import detect_new_file, extract_channel, read_file
from erp_interaction.erp_client import process_row_data
from app_window.utils import debug_print

def start_processing(config, on_message):
    import_path = config['DIRECTORY']['importing']  # 'importing' 값을 읽어옴
    debug_mode = config['DEBUG']['mode']

    automatic_processing = config.getboolean('PROCESS', 'automatic')  # 'automatic' 값 읽어오기

    while True:
        # Detect files
        new_files = detect_new_file(import_path)  # 수정된 filepath 사용

        if not new_files:
            logging.info("No files to process.")
            on_message("There are no files to process.\n")
        else:
            for new_file in new_files:
                channel = extract_channel(new_file)
                logging.info(f"New file found: {new_file}, channel: {channel}")
                on_message(f"New file found: {new_file}, 채널: {channel}\n")

                # Read file
                sales_data = read_file(new_file)
                logging.info(f"File read complete: {new_file}")
                on_message(f"File read complete: {new_file}\n")

                for _, row in sales_data.iterrows():
                    debug_print(f"sales_data {type(sales_data)}, row {type(row)}")
                    process_row_data(config, channel, row)

                # Move processed file to 'processed' directory
                shutil.move(new_file, f"{config['DIRECTORY']['processed']}/{os.path.basename(new_file)}")
                logging.info(f"File moved to processed directory: {new_file}")
                on_message(f"File moved to processed directory: {new_file}\n")

        if debug_mode or not automatic_processing:  # debug 모드이거나 automatic_processing이 False인 경우 반복문 종료
            break

        # Wait for the specified interval before checking for new files again
        interval = config.getint('PROCESS', 'interval')
        time.sleep(interval)
