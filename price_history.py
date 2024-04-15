# price_history.py
import time
import datetime
import requests
import json
from oauth_utils import OAuthClient


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


def retrieve_price_history(oauth_client, base_url, symbol_id, start_date, end_date, output_file):
    # Load the access token from the file
    with open(access_token_file, 'r') as file:
        access_token_data = json.load(file)
    access_token = access_token_data['access_token']  # Assuming the access token key is 'access_token'

    # Placeholder function for retrieving price history data
    # You should implement the actual logic here to retrieve price history data from the Schwab API
    print("Retrieving price history data for symbol:", symbol_id)
    print("Start Date:", start_date)
    print("End Date:", end_date)

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

            period = 1
            if access_token:
                # Retrieve price history for the current day
                price_history = get_price_history(base_url, access_token, symbol_id, start_timestamp, end_timestamp, period)
                print(price_history)
                
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


def iterate_over_dates(oauth_client, base_url, symbol_id, output_file):
    # Initialize OAuthClient with credentials file

    # # Token URL
    # token_url = 'https://api.schwabapi.com/v1/oauth/token'

    # Check if access token is valid
    if not oauth_client.is_token_valid():
        # Authenticate and obtain a new access token
        oauth_client.authenticate_and_get_access_token()

    # Define start and end dates
    start_date = datetime.datetime(2024, 4, 1)
    end_date = datetime.datetime(2024, 4, 5)


    # Retrieve price history data for the specified date range
    retrieve_price_history(oauth_client, base_url, symbol_id, start_date, end_date, output_file)


# Entry point of the script
if __name__ == "__main__":
    credentials_file = "credentials.json"
    access_token_file = "access_token.json"
    token_url = 'https://api.schwabapi.com/v1/oauth/token'
    base_url = 'https://api.schwabapi.com/marketdata/v1'
    symbol_id = "SPY"
    output_file = "price_history.json"  # Output file name

    # Your existing OAuth credentials
    oauth_client = OAuthClient(credentials_file, access_token_file, token_url)

    # Call the main function to iterate over the date range and retrieve price history
    iterate_over_dates(oauth_client, base_url, symbol_id, output_file)
