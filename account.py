# account.py

import json
from oauth_utils import OAuthClient
import requests


class AccountClient:
    """
    A class to interact with the Schwab API to retrieve account information.
    """

    def __init__(self, credentials_file, access_token_file, token_url):
        """
        Initializes the AccountClient with OAuth credentials.

        :param credentials_file: Path to the OAuth credentials file.
        :param access_token_file: Path to the access token file.
        :param token_url: URL for obtaining access token.
        """
        self.oauth_client = OAuthClient(credentials_file, access_token_file, token_url)
        # self.base_url = base_url

    def get_account_info(self, base_url):
        """
        Retrieves account information for the specified account number.

        :param account_number: The account number for which to retrieve information.
        :return: Account information JSON if successful, None otherwise.
        """
        self.base_url = base_url
        # Check if access token is valid
        if not self.oauth_client.is_token_valid():
            # Authenticate and obtain a new access token
            self.oauth_client.authenticate_and_get_access_token()

        # Get access token
        access_token = self.oauth_client.access_token

        if access_token:
            # headers = {
            #     'Authorization': f'Bearer {access_token}'
            # }


            headers = {
                        'Authorization': f'Bearer {self.oauth_client.access_token}',
                        'Accept': 'application/json'
                    }

            endpoint = f"{self.base_url}/accounts/accountNumbers"
            print(f'headers: {headers}')
            print(f'endpoint: {endpoint}')
            response = requests.get(endpoint, headers=headers)

            if response.status_code == 200:
                print(response)
                return response.json()
            else:
                print("Failed to get account information. Error:", response.text)
                return None
        else:
            print("Error: Failed to obtain access token.")
            return None


def main(credentials_file, access_token_file, token_url, base_url):
    """
    The main function to fetch account information using AccountClient.

    :param credentials_file: Path to the OAuth credentials file.
    :param access_token_file: Path to the access token file.
    :param token_url: URL for obtaining access token.
    :param account_number: The account number for which to retrieve information.
    """
    # Create AccountClient instance
    account_client = AccountClient(credentials_file, access_token_file, token_url)

    # Get account information
    account_info = account_client.get_account_info(base_url)

    if account_info:
        print("Account information:", account_info)


if __name__ == "__main__":
    # Define file paths and URLs
    credentials_file = 'credentials.json'
    access_token_file = 'access_token.json'
    token_url = 'https://api.schwabapi.com/v1/oauth/token'
    base_url = 'https://api.schwabapi.com/trader/v1'
    # account_number = '123456789'  # Example account number

    # Call main function to fetch account information
    main(credentials_file, access_token_file, token_url, base_url)
