#   Initial test code to get access token & market data.


import requests
import base64

# OAuth configuration
token_url = 'https://api.schwabapi.com/v1/oauth/token'
# app_key = 'YOUR_APP_KEY'
# app_secret = 'YOUR_APP_SECRET'

redirect_uri = 'https://127.0.0.1'

# Check if access token is already available
access_token = None  # Set to your existing access token if available

if not access_token:
    # If access token is not available, obtain it
    # Encode client credentials using base64
    credentials = f"{app_key}:{app_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Requesting access token
    token_params = {
        'grant_type': 'client_credentials',
        'redirect_uri': redirect_uri  # Not used in client credentials grant flow
    }

    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.post(token_url, data=token_params, headers=headers)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        print("Access token:", access_token)
    else:
        print("Failed to obtain access token. Error:", response.text)

# API configuration
base_url = 'https://api.schwabapi.com/marketdata/v1'  # Modified base URL
symbol_id = 'AAPL'  # Example symbol

# Construct API endpoint
endpoint = f"{base_url}/{symbol_id}/quotes"

# Include access token in the Authorization header
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Send GET request to retrieve quotes for the specified symbol
response = requests.get(endpoint, headers=headers)

if response.status_code == 200:
    quotes = response.json()
    print("Quotes:", quotes)
else:
    print("Failed to retrieve quotes. Error:", response.text)
