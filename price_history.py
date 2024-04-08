# This script retrieves price history data for a specified stock symbol from a financial API (SchwabAPI) 
# over a given date range and saves the data to a JSON file.

import json  # Library for working with JSON data
import os  # Library for interacting with the operating system
import requests  # Library for making HTTP requests
import time  # Library for working with time-related functions
import datetime  # Library for working with date and time data
from oauth_utils import OAuthClient, save_access_token  # Custom module for OAuth authentication

# Function to convert datetime to epoch format (milliseconds)
def datetime_to_epoch(dt):
    return int(dt.timestamp()) * 1000

# Function to retrieve price history for a given symbol and date range
def get_price_history(base_url, access_token, symbol, start_timestamp, end_timestamp, period):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    endpoint = f"{base_url}/pricehistory"

    # Define parameters for the API request
    params = {
        'symbol': symbol,
        'periodType': 'day',
        'period': period,
        'frequencyType': 'minute',
        'frequency': 1,
        'endDate': end_timestamp,
        'needExtendedHoursData': False,
        'needPreviousClose': False
    }

    # Send a GET request to the API
    response = requests.get(endpoint, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        print("Failed to get price history. Error:", response.text)
        return None

# Function to retrieve access token
def get_access_token(access_token_file, app_key, app_secret, redirect_uri, token_url):
    # Check if the access token file exists
    if os.path.exists(access_token_file):
        with open(access_token_file, 'r') as file:
            access_token_data = json.load(file)
            token = access_token_data.get('access_token')
            expiration_time = access_token_data.get('expiration_time')

            # Check if the access token is valid and not expired
            if token and expiration_time:
                current_time = int(time.time())
                if current_time < expiration_time:
                    print("Using existing access token.")
                    return token

    # Access token is expired or not available, request a new one
    oauth_client = OAuthClient(app_key, app_secret, redirect_uri)
    access_token_response = oauth_client.obtain_access_token(token_url)

    if access_token_response:
        # Save the new access token to file
        save_access_token(access_token_file, access_token_response)
        return access_token_response.get('access_token')
    else:
        print("Error: Failed to obtain access token.")
        return None

# Function to check if access token is valid
def is_token_valid(access_token_file):
    try:
        with open(access_token_file, 'r') as file:
            access_token_data = json.load(file)

        expiration_time = access_token_data.get('expiration_time')

        if expiration_time:
            current_time = int(time.time())
            if current_time < expiration_time:
                print("Access token is still valid.")
                return True
            else:
                print("Access token has expired.")
                return False
        else:
            print("Expiration time not found in access token data.")
            return False
    except FileNotFoundError:
        print(f"File '{access_token_file}' not found.")
        return False

# Main function to iterate over a date range and retrieve price history
def iterate_over_dates(base_url, credentials_file, access_token_file, symbol_id, output_file):
    with open(credentials_file, 'r') as file:
        credentials = json.load(file)
        app_key = credentials.get('app_key')
        app_secret = credentials.get('app_secret')
        redirect_uri = credentials.get('redirect_uri')

    if app_key and app_secret:
        if not is_token_valid(access_token_file):
            print('not valid token')

        token_url = 'https://api.schwabapi.com/v1/oauth/token'

        # Define start and end dates
        start_date = datetime.datetime(2024, 4, 1)
        end_date = datetime.datetime(2024, 4, 8)

        # Initialize an empty list to store candles data
        all_candles = []

        # Open output file in append mode
        with open(output_file, 'a') as f:
            # Iterate over the date range
            current_date = start_date
            while current_date <= end_date:
                # Convert dates to epoch format (milliseconds)
                start_timestamp = datetime_to_epoch(current_date)
                end_timestamp = datetime_to_epoch(current_date)

                # Retrieve access token
                access_token = get_access_token(access_token_file, app_key, app_secret, redirect_uri, token_url)
                period = 1
                if access_token:
                    # Retrieve price history for the current day
                    price_history = get_price_history(base_url, access_token, symbol_id, start_timestamp, end_timestamp, period)
                    
                    # Check if price history data is available and contains candles
                    if price_history and "candles" in price_history:
                        # Add human-readable date and time keys to each candle
                        for candle in price_history["candles"]:
                            candle_datetime = datetime.datetime.fromtimestamp(candle["datetime"] / 1000)
                            candle["human_readable_date"] = candle_datetime.strftime("%Y-%m-%d")
                            candle["human_readable_time"] = candle_datetime.strftime("%H:%M:%S")

                        # Append candles data to the list
                        all_candles.extend(price_history["candles"])
                        
                        # Print message indicating successful retrieval
                        print("Retrieved price history for:", current_date.date())
                        print("Number of candles:", len(price_history["candles"]))  # Print number of candles
                    else:
                        print("Failed to retrieve price history for:", current_date.date())
                else:
                    print("Failed to obtain access token.")

                # Move to the next day
                current_date += datetime.timedelta(days=period)

            # Create a dictionary with "candles" key containing all the candles data
            output_data = {"candles": all_candles}
            
            # Write the output data to the file
            json.dump(output_data, f)

if __name__ == "__main__":
    base_url = 'https://api.schwabapi.com/marketdata/v1'
    credentials_file = "credentials.json"
    access_token_file = "access_token.json"
    symbol_id = "SPY"
    output_file = "price_history.json"  # Output file name

    # Call the main function to iterate over the date range and retrieve price history
    iterate_over_dates(base_url, credentials_file, access_token_file, symbol_id, output_file)
