import csv
import json
import os

def read_pharmacies(directories):
    """
    Reads pharmacy data from CSV files in the given directories.

    Args:
        directories (list): List of directories containing pharmacy CSV files.

    Returns:
        dict: A dictionary mapping NPI to chain name.
    """
    pharmacies = {}
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as csvfile:
                    # Read CSV file with fieldnames 'chain' and 'npi'
                    reader = csv.DictReader(csvfile, fieldnames=['chain', 'npi'])
                    for row in reader:
                        # Map NPI to chain name
                        pharmacies[row['npi']] = row['chain']
    return pharmacies

def read_json_files(directories):
    """
    Reads JSON data from files in the given directories.

    Args:
        directories (list): List of directories containing JSON files.

    Returns:
        list: A list of data entries from all JSON files.
    """
    data = []
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as jsonfile:
                    try:
                        # Load JSON data and extend the data list
                        json_data = json.load(jsonfile)
                        data.extend(json_data)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file {filepath}")
    return data
