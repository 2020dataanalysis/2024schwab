import json
import os
import requests
import json
import time
from oauth_utils import OAuthClient, save_access_token

def is_token_valid(access_token_file):
    # Load access token data from file
    with open(access_token_file, 'r') as file:
        access_token_data = json.load(file)

    # Get the expiration time from the access token data
    expiration_time = access_token_data.get('expiration_time')

    if expiration_time:
        # Get the current time
        current_time = int(time.time())

        # Compare the current time with the expiration time
        if current_time < expiration_time:
            print("Access token is still valid.")
            return True
        else:
            print("Access token has expired.")
            return False
    else:
        print("Expiration time not found in access token data.")
        return False





def get_access_token(access_token_file, app_key, app_secret, redirect_uri, token_url):
    if os.path.exists(access_token_file):
        with open(access_token_file, 'r') as file:
            data = json.load(file)
            return data.get('access_token')
    else:
        oauth_client = OAuthClient(app_key, app_secret, redirect_uri)
        access_token_response = oauth_client.obtain_access_token(token_url)

        if access_token_response:
            save_access_token(access_token_file, access_token_response)
            return access_token_response.get('access_token')
        else:
            print("Error: Failed to obtain access token.")
            return None

def get_ticker_data(base_url, access_token, symbol_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    endpoint = f"{base_url}/{symbol_id}/quotes"
    response = requests.get(endpoint, headers=headers)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get ticker data. Error:", response.text)
        return None

def main(credentials_file, access_token_file, symbol_id):
    with open(credentials_file, 'r') as file:
        credentials = json.load(file)
        app_key = credentials.get('app_key')
        app_secret = credentials.get('app_secret')
        redirect_uri = credentials.get('redirect_uri')

    if app_key and app_secret:
        if not is_token_valid(access_token_file):
            pass

        token_url = 'https://api.schwabapi.com/v1/oauth/token'
        access_token = get_access_token(access_token_file, app_key, app_secret, redirect_uri, token_url)

        if access_token:
            base_url = 'https://api.schwabapi.com/marketdata/v1'
            print('49')
            ticker_data = get_ticker_data(base_url, access_token, symbol_id)

            if ticker_data:
                print("Ticker data:", ticker_data)
        else:
            print("Error: Failed to obtain access token.")
    else:
        print("Error: App key or app secret not found in credentials file.")

if __name__ == "__main__":
    credentials_file = 'credentials.json'
    access_token_file = 'access_token.json'
    symbol_id = 'AAPL'  # Example symbol ID
    main(credentials_file, access_token_file, symbol_id)
