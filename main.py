# main.py

import os
import configparser
import logging

from app_window.creator import open_main_window

def load_default_settings():
    config_path = os.path.join(os.getcwd(), 'config.ini')

    try:
        config = configparser.ConfigParser()
        config.read(config_path)

    except FileNotFoundError:
        raise FileNotFoundError("Cannot find config.ini file.")

    return config


if __name__ == "__main__":

    logging.basicConfig(filename=f"sales_data_importer.log", filemode='a', level=logging.DEBUG,
                        format='%(name)s - %(levelname)s - %(message)s')

    config = load_default_settings()

    if config.getboolean('DEBUG', 'mode'):
        open_main_window(config)
    else:
        try:
            open_main_window(config)
        except Exception as e:
            logging.error(e)
