# file_handler.py

import os
import pandas as pd

from app_window.utils import debug_print

def read_file(filepath):
    """Reads the data from a file."""
    if filepath.endswith('.csv'):
        data = read_csv_file(filepath)
    elif filepath.endswith('.xlsx'):
        data = read_excel_file(filepath)
    else:
        raise Exception(f"Unsupported file format: {filepath}")

    return data

def read_csv_file(filepath):
    """Reads a CSV file and returns the data."""
    data = pd.read_csv(filepath)  # Modify this line based on the specific CSV file format and reading options
    return data

def read_excel_file(filepath):
    """Reads an Excel file and returns the data."""
    data = pd.read_excel(filepath, header=0)
    return data

def extract_channel(filename):
    # This function extracts channel information from a filename.
    # You may need to modify this function depending on your filename format.
    if 'orderlistingstyles' in filename:
        return 'LASHOWROOM'
    elif 'faire-orders' in filename:
        return 'FAIRY'
    else:
        return 'FASHIONGO'

def is_file_accessible(filepath):
    """Check if a file is not being used by another process."""
    try:
        with open(filepath, 'r+') as f:
            return True
    except IOError:
        return False

def detect_new_file(filepath):
    # Get list of all csv and xlsx files in the given directory
    file_list = []
    for entry in os.scandir(filepath):
        if entry.is_file() and entry.name.endswith(('.csv', '.xlsx')):
            file_list.append(entry.path)

    debug_print(f"Target files {len(file_list)}")

    # Filter out files that are not accessible
    accessible_files = [f for f in file_list if is_file_accessible(f)]

    debug_print(f"Accessible files {len(accessible_files)}")

    return accessible_files
