import json
import requests
import base64
import time


class OAuthClient:
    def __init__(self, credentials_file, access_token_file, token_url):
        self.credentials_file = credentials_file
        self.access_token_file = access_token_file
        self.token_url = token_url
        # self.redirect_uri = redirect_uri
        self.load_credentials()
        self.load_access_token()

    def load_credentials(self):
        try:
            with open(self.credentials_file, 'r') as file:
                credentials = json.load(file)
                self.app_key = credentials.get('app_key')
                self.app_secret = credentials.get('app_secret')
                self.redirect_uri = credentials.get('redirect_uri')
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




    def get_refresh_token(self, authorization_code):
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
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        # headers = {'Authorization': f'Basic {base64.b64encode(bytes(f"{self.app_key}:{self.app_secret}", "utf-8")).decode("utf-8")}', 'Content-Type': 'application/x-www-form-urlencoded'}
        print(self.token_url)
        print(f'headers: {headers}')
        print(token_params)

        response = requests.post(self.token_url, data=token_params, headers=headers)
        print(response)
        if response.status_code == 200:
            token_response = response.json()
            self.save_access_token(token_response)
            self.access_token = token_response.get('access_token')
            self.refresh_token = token_response.get('refresh_token')
            return token_response       # May need to return True or 200

            # token_data = response.json()
            # access_token = token_data.get('access_token')
            # refresh_token = token_data.get('refresh_token')
            # print(f'access token: {access_token}')
            # print(f'refresh token: {refresh_token}')
            # return access_token, refresh_token
        else:
            print("Failed to obtain access token. Error:", response.text)
            return None





    def get_access_token(self):
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
            access_token_response = response.json()
            return access_token_response
        else:
            print("Failed to obtain access token. Error:", response.text)
            return None

    def save_access_token(self, access_token_response):
        with open(self.access_token_file, 'w') as file:
            json.dump(access_token_response, file)

    def authenticate_and_get_access_token(self):
        print("Access token is not available or has expired.")
        access_token_response = self.get_access_token()
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
