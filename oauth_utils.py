import json
import requests
import base64
import time
from urllib.parse import unquote

class OAuthClient:
    def __init__(self, credentials_file, access_token_file):
        self.credentials_file = credentials_file
        self.access_token_file = access_token_file
        self.load_credentials()
        self.load_access_token()

    def load_credentials(self):
        try:
            with open(self.credentials_file, 'r') as file:
                credentials = json.load(file)
                self.app_key = credentials.get('app_key')
                self.app_secret = credentials.get('app_secret')
                self.redirect_uri = credentials.get('redirect_uri')
                self.authorization_endpoint = credentials.get('authorization_endpoint')
                self.token_url = credentials.get('token_url')
        except FileNotFoundError:
            print(f"Credentials file '{self.credentials_file}' not found.")
            self.app_key = None
            self.app_secret = None

    def load_access_token(self):
        try:
            # Load the access token from the file
            with open(self.access_token_file, 'r') as file:
                access_token_data = json.load(file)
            self.access_token = access_token_data['access_token']  # Assuming the access token key is 'access_token'
        except FileNotFoundError:
            print(f'Access token file {self.access_token_file} not found.')
            self.access_token = None
            self.refresh_token = None


    def calculate_expiration_time(self, expires_in):
        # Calculate expiration time by adding expires_in seconds to the current time
        current_time = int(time.time())
        expiration_time = current_time + int(expires_in)
        return expiration_time


    def authorization_code_grant_flow(self):
        # returns:
        # {
        #     "expires_in": 1800,
        #     "token_type": "Bearer",
        #     "scope": "api",
        #     "refresh_token": "",
        #     "access_token": "",
        #     "id_token": "",
        #     "expiration_time": 1713904409
        # }

        self.get_authorization_code()
        token_response = self.exchange_authorization_code_for_tokens()
        self.save_access_token(token_response)
        self.access_token = token_response.get('access_token')
        self.refresh_token = token_response.get('refresh_token')


    def client_credentials_grant_flow(self):
        #         {
        #     "expires_in": "3600",
        #     "token_type": "Bearer",
        #     "scope": "api",
        #     "access_token": "",
        #     "expiration_time": 1713929225
        # }
        token_response = self.client_credentials_grant_flow_request()
        self.save_access_token(token_response)
        self.access_token = token_response.get('access_token')


    def get_authorization_code(self):
        """
        Redirects the user to the authorization endpoint and prompts the user to input the authorization code.

        Args:
            authorization_endpoint (str): The OAuth authorization endpoint URL.
            client_id (str): The client ID of the OAuth application.
            redirect_uri (str): The redirect URI where the authorization server will redirect the user after authorization.

        Returns:
            str: The authorization code obtained from the user.
                    # returns:
        # {
        #     "expires_in": 1800,
        #     "token_type": "Bearer",
        #     "scope": "api",
        #     "refresh_token": "",
        #     "access_token": "",
        #     "id_token": "",
        #     "expiration_time": 1713904409
        # }

        """
        # Redirect the user to the authorization endpoint
        authorization_url = (
            f"{self.authorization_endpoint}?client_id={self.app_key}"
            f"&redirect_uri={self.redirect_uri}&response_type=code"
        )
        print("Please visit the following URL and authorize the application:")
        print(authorization_url)

        # After user authorization, the authorization code will be obtained via the redirect URI
        authorization_code_url = input(
            "Enter the authorization code from the callback URL: "
        )

        # Find the index of 'code=' and '&session=' in the URL
        code_index = authorization_code_url.find('code=')
        session_index = authorization_code_url.find('&session=')

        # Extract the authorization code using the indices
        if code_index != -1 and session_index != -1:
            authorization_code_extracted = (
                authorization_code_url[code_index + len('code='):session_index]
            )
        else:
            # Handle case where either 'code=' or '&session=' is not found
            authorization_code_extracted = None

        # print("Extracted Authorization Code:", authorization_code_extracted)
        authorization_code = unquote(authorization_code_extracted)
        # print("Extracted Authorization Code URL decoded:", authorization_code)
        self.authorization_code = authorization_code
        return authorization_code


    def exchange_authorization_code_for_tokens(self):
        if not self.app_key or not self.app_secret:
            print("OAuth credentials not found. Please check the credentials file.")
            return None

        credentials = f"{self.app_key}:{self.app_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        token_params = {
            'grant_type': 'authorization_code',
            'code': self.authorization_code,
            'redirect_uri': self.redirect_uri
        }
        # headers = {'Authorization': f'Basic {base64.b64encode(bytes(f"{self.app_key}:{self.app_secret}", "utf-8")).decode("utf-8")}', 'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.token_url, data=token_params, headers=headers)

        if response.status_code == 200:
            token_response = response.json()
            return token_response       # May need to return True or 200
        else:
            print("Failed to obtain access token. Error:", response.text)
            return None


    def client_credentials_grant_flow_request(self):
        # returns:
        # {
        #     "expires_in": 3600,
        #     "token_type": "Bearer",
        #     "scope": "api",
        #     "access_token": "I0.b2F1dGgyLmNkYy5zY2h3YWIuY29t.u8N8IhFHFzBtImflrht1CylwwRVuctgfzDBhvYMVhTg@",
        #     "expiration_time": 1713904409
        # }

        if not self.app_key or not self.app_secret:
            print("OAuth credentials not found. Please check the credentials file.")
            return None

        credentials = f"{self.app_key}:{self.app_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }

        token_params = {
            'grant_type': 'client_credentials',
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(self.token_url, data=token_params, headers=headers)

        if response.status_code == 200:
            token_response = response.json()
            return token_response
        else:
            print("Failed to obtain access token. Error:", response.text)
            return None

    def save_access_token(self, access_token_response):
        expiration_time = self.calculate_expiration_time(access_token_response['expires_in'])
        access_token_response['expiration_time'] = expiration_time
        with open(self.access_token_file, 'w') as file:
            json.dump(access_token_response, file)

    def authenticate_and_get_access_token(self):
        print("Access token is not available or has expired.")
        access_token_response = self.client_credentials_grant_flow()
        if access_token_response:
            # Save the new access token to file
            self.save_access_token(access_token_response)
            self.access_token = access_token_response['access_token']
            print("New access token saved successfully.")
        else:
            print("Failed to obtain a new access token.")

    def is_token_valid(self):
        try:
            with open(self.access_token_file, 'r') as file:
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
            print(f"File '{self.access_token_file}' not found.")
            return False
