import json
import requests
import time
from oauth_utils import OAuthClient

class QuoteClient:
    def __init__(self, credentials_file, access_token_file, token_url):
        self.oauth_client = OAuthClient(credentials_file, access_token_file, token_url)

    def get_ticker_data(self, symbol_id):
        # Check if access token is valid
        if not self.oauth_client.is_token_valid():
            # Authenticate and obtain a new access token
            self.oauth_client.authenticate_and_get_access_token()

        # Get access token
        access_token = self.oauth_client.access_token

        if access_token:
            base_url = 'https://api.schwabapi.com/marketdata/v1'
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            endpoint = f"{base_url}/{symbol_id}/quotes"
            response = requests.get(endpoint, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to get ticker data. Error:", response.text)
                return None
        else:
            print("Error: Failed to obtain access token.")
            return None

def main(credentials_file, access_token_file, token_url, symbol_id):
    quote_client = QuoteClient(credentials_file, access_token_file, token_url)
    ticker_data = quote_client.get_ticker_data(symbol_id)

    if ticker_data:
        print("Ticker data:", ticker_data)

if __name__ == "__main__":
    credentials_file = 'credentials.json'
    access_token_file = 'access_token.json'
    token_url = 'https://api.schwabapi.com/v1/oauth/token'
    symbol_id = 'AAPL'  # Example symbol ID
    main(credentials_file, access_token_file, token_url, symbol_id)
