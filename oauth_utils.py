import json
import requests
import base64
import time

class OAuthClient:
    def __init__(self, app_key, app_secret, redirect_uri):
        self.app_key = app_key
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri

    def obtain_access_token(self, token_url):
        credentials = f"{self.app_key}:{self.app_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }

        token_params = {
            'grant_type': 'client_credentials',
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(token_url, data=token_params, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to obtain access token. Error:", response.text)
            return None


def save_access_token(access_token_file, access_token_response):
    expiration_time = calculate_expiration_time(access_token_response['expires_in'])
    access_token_response['expiration_time'] = expiration_time
    with open(access_token_file, 'w') as file:
        json.dump(access_token_response, file)



def calculate_expiration_time(expires_in):
    # Calculate expiration time by adding expires_in seconds to the current time
    current_time = int(time.time())
    expiration_time = current_time + int(expires_in)
    return expiration_time

# # Example usage
# if __name__ == "__main__":
#     # Initialize OAuth client
#     oauth_client = OAuthClient(app_key, app_secret, redirect_uri)

#     # Token URL
#     token_url = 'https://api.schwabapi.com/v1/oauth/token'

#     # Obtain access token response
#     access_token_response = oauth_client.obtain_access_token(token_url)

#     if access_token_response:
#         # Calculate expiration time
#         expiration_time = calculate_expiration_time(access_token_response['expires_in'])
#         print("Expiration time:", expiration_time)

#         # Save access token along with expiration time
#         access_token_file = 'access_token.json'
#         save_access_token(access_token_file, access_token_response, expiration_time)
#         print("Access token saved successfully.")
#     else:
#         print("Failed to obtain access token.")
