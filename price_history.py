import time
import datetime
import requests
import json
from oauth_utils import OAuthClient


def datetime_to_epoch(dt):
    """Convert datetime to epoch format (milliseconds)."""
    return int(dt.timestamp()) * 1000


def get_price_history(base_url, access_token, symbol, start_timestamp, end_timestamp, period):
    """Retrieve price history for a given symbol and date range."""
    headers = {'Authorization': f'Bearer {access_token}'}
    endpoint = f"{base_url}/pricehistory"
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

    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get price history. Error:", response.text)
        return None


def retrieve_price_history(oauth_client, base_url, symbol_id, start_date, end_date, output_file):
    """Retrieve price history data for the specified date range."""
    with open(oauth_client.access_token_file, 'r') as file:
        access_token_data = json.load(file)
    access_token = access_token_data['access_token']

    all_candles = []
    with open(output_file, 'a') as f:
        current_date = start_date
        while current_date <= end_date:
            start_timestamp = datetime_to_epoch(current_date)
            end_timestamp = datetime_to_epoch(current_date)
            period = 1

            if access_token:
                price_history = get_price_history(base_url, access_token, symbol_id, start_timestamp, end_timestamp, period)

                if price_history and "candles" in price_history:
                    for candle in price_history["candles"]:
                        candle_datetime = datetime.datetime.fromtimestamp(candle["datetime"] / 1000)
                        candle["human_readable_date"] = candle_datetime.strftime("%Y-%m-%d")
                        candle["human_readable_time"] = candle_datetime.strftime("%H:%M:%S")
                    all_candles.extend(price_history["candles"])
                    print("Retrieved price history for:", current_date.date())
                    print("Number of candles:", len(price_history["candles"]))
                else:
                    print("Failed to retrieve price history for:", current_date.date())
            else:
                print("Failed to obtain access token.")

            current_date += datetime.timedelta(days=period)

        output_data = {"candles": all_candles}
        json.dump(output_data, f)


def iterate_over_dates(oauth_client, base_url, symbol_id, output_file):
    """Iterate over the date range and retrieve price history."""
    if not oauth_client.is_token_valid():
        oauth_client.authenticate_and_get_access_token()

    start_date = datetime.datetime(2024, 4, 1)
    end_date = datetime.datetime(2024, 4, 5)

    retrieve_price_history(oauth_client, base_url, symbol_id, start_date, end_date, output_file)


if __name__ == "__main__":
    # Define file paths and URLs
    credentials_file = "credentials.json"
    access_token_file = "access_token.json"
    token_url = 'https://api.schwabapi.com/v1/oauth/token'
    base_url = 'https://api.schwabapi.com/marketdata/v1'
    symbol_id = "SPY"
    output_file = "price_history.json"  # Output file name

    # Initialize OAuthClient with credentials and access token file paths, and token URL
    oauth_client = OAuthClient(credentials_file, access_token_file, token_url)

    # Call the main function to iterate over the date range and retrieve price history
    iterate_over_dates(oauth_client, base_url, symbol_id, output_file)
