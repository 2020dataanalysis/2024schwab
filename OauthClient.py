#   OauthClient.py

"""
Explanation:
    1. The authorization server redirects the user to the login page and obtains their consent for accessing the requested resources.
    2. The user logs in and grants access to the OAuth client.
    3. The authorization server generates an authorization code and returns it to the OAuth client.
    4. The OAuth client exchanges the authorization code for access and refresh tokens by making a request to the token endpoint.
    5. Upon receiving the tokens, the OAuth client saves them in .json files (e.g., access_token.json, refresh_token.json) for future use.

This explanation simplifies the OAuth 2.0 authorization flow and focuses on the steps related to token retrieval and saving them in .json files.
"""




import json
import requests
import base64
import time
# import logging
from pathlib import Path
from urllib.parse import unquote
import asyncio
from datetime import datetime


# logging.basicConfig(level=logging.INFO)

class OAuthClient:
    AUTHORIZATION_CODE_KEY = 'AUTHORIZATION_CODE'
    REFRESH_TOKEN_KEY = 'REFRESH_TOKEN'

    def __init__(self, credentials_path, credentials_file, grant_flow_type_filenames_file):
        self.credentials_path = credentials_path
        self.credentials_file = credentials_file
        self.grant_flow_type_filenames_file = grant_flow_type_filenames_file
        self.load_credentials()
        self.load_grant_flow_type_filenames()
        self.AUTHORIZATION_CODE_GRANT_FILENAME = self.grant_flow_type_filenames[self.AUTHORIZATION_CODE_KEY]
        self.REFRESH_TOKEN_GRANT_FILENAME = self.grant_flow_type_filenames[self.REFRESH_TOKEN_KEY]
        # print(self.AUTHORIZATION_CODE_GRANT_FILENAME)
        # print(self.REFRESH_TOKEN_GRANT_FILENAME)
        # self.load_access_token()
        self.manage_tokens()

        # asyncio.run(self.refresh_token_timer())

    def load_credentials(self):
        # path = Path(path) / self.credentials_file
        # self.config = self._load_config(path)

        try:
            with open(Path(self.credentials_path) / self.credentials_file, 'r') as file:
                credentials = json.load(file)
                self.app_key = credentials.get('app_key')
                self.app_secret = credentials.get('app_secret')
                self.redirect_uri = credentials.get('redirect_uri')
                self.authorization_endpoint = credentials.get('authorization_endpoint')
                self.token_url = credentials.get('token_url')
                # logging.info(f'token_url: {self.token_url}')

        except FileNotFoundError:
            # print(f"Credentials file '{self.credentials_file}' not found.")
            self.app_key = None
            self.app_secret = None


    def load_grant_flow_type_filenames(self):
        try:
            file_path = Path('config') / self.grant_flow_type_filenames_file
            with open(file_path, 'r') as file:
                self.grant_flow_type_filenames = json.load(file)
                # print("Grant Flow Types and Filenames:")
                # for flow_type, filename in self.grant_flow_type_filenames.items():
                #     print(f"Grant Flow Type: {flow_type}, Filename: {filename}")

        except FileNotFoundError:
            # print(f"Config file '{self.grant_flow_type_filenames_file}' not found.")
            self.grant_flow_type_filenames = {}


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
        # token_file = self.AUTHORIZATION_CODE_GRANT_FILENAME
        # print(token_file)
        self.save_token(self.AUTHORIZATION_CODE_KEY, token_response)
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


    def refresh_token_grant_flow(self, token_file_key):
        token_file = self.grant_flow_type_filenames[token_file_key]
        token_response = self.get_refresh_access_token()
        if token_response:
            self.save_token(token_file_key, token_response)
            self.access_token = token_response.get('access_token')
            self.refresh_token = token_response.get('refresh_token')
            self.access_token_expiration_time = token_response['access_token_expiration_time']
            # print('Refresh Token Grant Flow --> Complete')
        else:
            # print('Failed to Refresh Token Grant Flow')
            pass
    


    def get_refresh_access_token(self):
        # print('get_refresh_access_token')
        credentials = f"{self.app_key}:{self.app_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }

        payload = {
					'grant_type': 'refresh_token',
					'refresh_token': self.refresh_token
				}
        # print(headers)
        # print(payload)
        # print(self.token_url)

        response = requests.post(self.token_url, headers=headers, data=payload)
        # print(response)

        if response.status_code == 200:
            token_response = response.json()
            return token_response
        else:
            # print("Failed to refresh access token. Error:", response.text)
            return None


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
        # print("Please visit the following URL and authorize the application:")
        # print(authorization_url)

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
            # print("OAuth credentials not found. Please check the credentials file.")
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
            # print("Failed to obtain access token. Error:", response.text)
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
            # print("OAuth credentials not found. Please check the credentials file.")
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
            # print("Failed to obtain access token. Error:", response.text)
            return None

    def save_access_token(self, access_token_response):
        expiration_time = self.calculate_expiration_time(access_token_response['expires_in'])
        access_token_response['expiration_time'] = expiration_time
        with open(Path(self.credentials_path) / self.token_file, 'w') as file:
            json.dump(access_token_response, file)
        # print("New token data saved successfully.")


    def save_token(self, token_file_key, token_response):
        token_file = self.grant_flow_type_filenames[token_file_key]
        token_file_path = Path(self.credentials_path) / token_file
        # If Authorization Code Grant Flow then make copy for Refresh Token Grant Flow
        expiration_time = self.calculate_expiration_time(token_response['expires_in'])
        token_response['access_token_expiration_time'] = expiration_time
        if 'refresh_token' in token_response:
            expiration_time = self.calculate_expiration_time( 60 * 60 * 24 * 7 )
            token_response['refresh_token_expiration_time'] = expiration_time

        if token_file_key == self.AUTHORIZATION_CODE_KEY:
            with open(Path(self.credentials_path) / self.REFRESH_TOKEN_GRANT_FILENAME, 'w') as file:
                json.dump(token_response, file)
            # print(f"New token data saved successful: {self.REFRESH_TOKEN_GRANT_FILENAME}")

        with open(Path(self.credentials_path) / token_file, 'w') as file:
            json.dump(token_response, file)
        # print(f"New token data saved successful: {token_file}")


    def is_token_valid(self, token_file_key, token):
        token_file = self.grant_flow_type_filenames[token_file_key]
        try:
            with open(Path(self.credentials_path) / token_file, 'r') as file:
                token_data = json.load(file)
            key = token +   '_expiration_time'
            # print(key)
            expiration_time = token_data.get(key)
            if expiration_time:
                current_time = int(time.time())
                if current_time < expiration_time:
                    # print(f"{token} is still valid.")
                    return True
                else:
                    # print(f"Token has expired: {token}")
                    return False
            else:
                # print("Expiration time not found in access token data.")
                return False
        except FileNotFoundError:
            # print(f"File '{token_file}' not found.")
            return False


    def load_token_file(self, token_file_key):
        token_file = self.grant_flow_type_filenames[token_file_key]
        token_file_path = Path(self.credentials_path) / token_file
        try:
            # Load the tokens from the file
            with open(token_file_path, 'r') as file:
                token_data = json.load(file)
            self.access_token = token_data['access_token']
            self.access_token_expiration_time = token_data['access_token_expiration_time']
            # logging.info(f'access_token_expiration_time: {self.access_token_expiration_time}')
            self.refresh_token = None
            if 'refresh_token' in token_data:
                self.refresh_token = token_data['refresh_token']
        except FileNotFoundError:
            # print(f'Access token file {token_file} not found.')
            self.access_token = None
            self.refresh_token = None


    def manage_tokens(self):
        # Check if access token is valid with Refresh Flow
        token_file_key = self.REFRESH_TOKEN_KEY
        token_file = self.grant_flow_type_filenames[token_file_key]
        # print(f'token_file: {token_file}')
        import os
        if os.path.exists(Path(self.credentials_path) / token_file):
            # print(f'File Exists: {token_file}')
            if self.is_token_valid(token_file_key, 'access_token'):
                # print('load token file')
                self.load_token_file(token_file_key)
                return
            else:
                # print('Perform Refresh Grant Flow')
                if self.is_token_valid(token_file_key, 'refresh_token'):
                    # print('Refresh Token is valid')
                    # print('Perform Refresh Grant Flow')
                    # print('load token file')  
                    self.load_token_file(token_file_key)
                    self.refresh_token_grant_flow(token_file_key)
                    return
                else:
                    # print('Perform Authorization Code Grant Flow')
                    self.authorization_code_grant_flow()
        else:
            # print(f'File does not Exist: {token_file}')
            # print('Perform Authorization Code Grant Flow')
            self.authorization_code_grant_flow()
            return


    # async def refresh_token_timer(self):
    #     if self.access_token_expiration_time:
    #         if isinstance(self.access_token_expiration_time, int):
    #             expiration_time = datetime.utcfromtimestamp(self.access_token_expiration_time)
    #             remaining_time = (expiration_time - datetime.utcnow()).total_seconds()
    #             # print(f'OauthClient: refresh_token_timer(): 359 remaining_time: {remaining_time}')

    #             #   Use 1 second instead of 0 because it may come back milliseconds before & loop a couple times before less than 0
    #             if remaining_time < 1:
    #                 # print("async refresh_token_timer(): Access token already expired.")
    #                 token_file_key = self.REFRESH_TOKEN_KEY
    #                 # logging.info("Log Perform Refresh Grant Flow")
    #                 # self.manage_tokens()
    #                 # print('Perform Refresh Grant Flow')
    #                 # print('load token file')  
    #                 self.load_token_file(token_file_key)
    #                 self.refresh_token_grant_flow(token_file_key)
    #                 expiration_time = datetime.utcfromtimestamp(self.access_token_expiration_time)
    #                 remaining_time = (expiration_time - datetime.utcnow()).total_seconds()
    #                 # print(f'OauthClient: refresh_token_timer(): 404 remaining_time: {remaining_time}')

    #             await asyncio.sleep(remaining_time)
    #             asyncio.create_task(self.refresh_token_timer())

    #         else:
    #             # print("Access token expiration time is not in the correct format.")
    #             pass
    #     else:
    #         # print("Access token expiration time not set.")
    #         pass


    def refresh_token_timer(self):
        if self.access_token_expiration_time:
            if isinstance(self.access_token_expiration_time, int):
                expiration_time = datetime.utcfromtimestamp(self.access_token_expiration_time)
                remaining_time = (expiration_time - datetime.utcnow()).total_seconds()
                # print(f'OauthClient: refresh_token_timer(): 359 remaining_time: {remaining_time}')

                #   Use 1 second instead of 0 because it may come back milliseconds before & loop a couple times before less than 0
                if remaining_time < 1:
                    # print("async refresh_token_timer(): Access token already expired.")
                    token_file_key = self.REFRESH_TOKEN_KEY
                    # logging.info("Log Perform Refresh Grant Flow")
                    # self.manage_tokens()
                    # print('Perform Refresh Grant Flow')
                    # print('load token file')  
                    self.load_token_file(token_file_key)
                    self.refresh_token_grant_flow(token_file_key)
                    expiration_time = datetime.utcfromtimestamp(self.access_token_expiration_time)
                    remaining_time = (expiration_time - datetime.utcnow()).total_seconds()
                    # print(f'OauthClient: refresh_token_timer(): 404 remaining_time: {remaining_time}')

                # await asyncio.sleep(remaining_time)
                # asyncio.create_task(self.refresh_token_timer())
                return remaining_time

            else:
                # print("Access token expiration time is not in the correct format.")
                pass
        else:
            # print("Access token expiration time not set.")
            pass
        return None