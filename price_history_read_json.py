"""
Candle Analysis Tool

This script provides functionality to analyze JSON data containing candle information.
It reads data from a file, extracts candle details, and performs analysis on the dataset,
including counting the number of candles for each day and providing summary statistics.

Author: Sam Portillo

Usage:
    - Ensure the JSON file containing candle data is available.
    - Set the file path in the 'file_path' variable.
    - Run the script.
    - This script does not work on (visually beautified) formatted data.
"""

import json
import datetime
import os
from collections import defaultdict

# Function definitions...

import json
import datetime
import os
from collections import defaultdict

def get_candles_info_from_file(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return None
    
    # Initialize variables to store data
    total_elements = 0
    day_counts = defaultdict(int)
    unique_dates = set()
    
    # Read JSON data from file
    with open(file_path, 'r') as file:
        for line in file:
            # Parse JSON from each line
            try:
                json_data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue
            
            # Check if JSON data contains "candles" key
            if "candles" not in json_data:
                print("JSON data does not contain 'candles' key.")
                continue
            
            # Iterate over the candles array
            for candle in json_data["candles"]:
                # Extract the date from the "datetime" field
                timestamp = candle.get("datetime")
                if timestamp is None:
                    print("Missing 'datetime' field in candle:", candle)
                    continue
                # Convert the timestamp to a human-readable date (assuming milliseconds)
                date = datetime.datetime.fromtimestamp(timestamp / 1000).date()
                # Add the date to the set of unique dates
                unique_dates.add(date)
                # Increment the count for the corresponding day
                day_counts[date] += 1
                # Increment total elements count
                total_elements += 1
    
    # Print out the total number of days
    print(f"Total number of days: {len(unique_dates)}")
    
    # Print out the total number of elements for all days
    print(f"Total number of elements for all days: {total_elements}")
    
    # Print out the number of elements for each day
    for day, count in day_counts.items():
        print(f"{day}: {count} elements")

# Example usage
file_path = 'price_history.json'  # Specify your file path here
get_candles_info_from_file(file_path)
