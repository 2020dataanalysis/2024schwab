import json
from oauth_utils import OAuthClient
import requests


class AccountClient:
    """
    A class to interact with the Schwab API to retrieve account information.
    """

    def __init__(self, credentials_file, grant_flow_type_filenames_file):
        """
        Initializes the AccountClient with OAuth credentials.

        :param credentials_file: Path to the OAuth credentials file.
        :param access_token_file: Path to the access token file.
        :param token_url: URL for obtaining access token.
        :param redirect_uri: Redirect URI for OAuth authorization.
        """
        self.oauth_client = OAuthClient(credentials_file, grant_flow_type_filenames_file)

        # Manage tokens to ensure continuous access
        # manage_tokens(oauth_client)
        # self.oauth_client.manage_tokens()


    def get_account_info(self, base_url):
        """
        Retrieves account information for the specified account number.

        :param account_number: The account number for which to retrieve information.
        :return: Account information JSON if successful, None otherwise.
        """

        if self.oauth_client.access_token:
            headers = {
                'Authorization': f'Bearer {self.oauth_client.access_token}',
                'Accept': 'application/json'
            }

            endpoint = f"{base_url}/accounts/accountNumbers"
            response = requests.get(endpoint, headers=headers)
            print(endpoint)
            print(response)
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to get account information. Error:", response.text)
                return None
        else:
            print("Error: Failed to obtain access token.")
            return None


def main(credentials_file, grant_flow_type_filenames_file, base_url):
    """
    The main function to fetch account information using AccountClient.

    :param credentials_file: Path to the OAuth credentials file.
    :param access_token_file: Path to the access token file.
    :param token_url: URL for obtaining access token.
    :param base_url: Base URL for the Schwab API.
    :param redirect_uri: Redirect URI for OAuth authorization.
    """
    # Create AccountClient instance
    account_client = AccountClient(credentials_file, grant_flow_type_filenames_file)

    # Get account information
    account_info = account_client.get_account_info(base_url)

    if account_info:
        print("Account information:", account_info)



import datetime
import time
import json
from oauth_utils import OAuthClient

if __name__ == "__main__":
    # Initialize OAuthClient with credentials and token files
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'

    base_url = 'https://api.schwabapi.com/trader/v1'
    main(credentials_file, grant_flow_type_filenames_file, base_url)
