import json
from oauth_utils import OAuthClient
import requests


class AccountClient:
    """
    A class to interact with the Schwab API to retrieve account information.
    """

    def __init__(self, credentials_file, token_file):
        """
        Initializes the AccountClient with OAuth credentials.

        :param credentials_file: Path to the OAuth credentials file.
        :param access_token_file: Path to the access token file.
        :param token_url: URL for obtaining access token.
        :param redirect_uri: Redirect URI for OAuth authorization.
        """
        self.oauth_client = OAuthClient(credentials_file, token_file)

    def get_account_info(self, base_url):
        """
        Retrieves account information for the specified account number.

        :param account_number: The account number for which to retrieve information.
        :return: Account information JSON if successful, None otherwise.
        """
        # Check if access token is valid
        # if not self.oauth_client.is_token_valid():
        #     # Authenticate and obtain a new access token
        #     self.oauth_client.authenticate_and_get_access_token()


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


def main(credentials_file, token_file, base_url):
    """
    The main function to fetch account information using AccountClient.

    :param credentials_file: Path to the OAuth credentials file.
    :param access_token_file: Path to the access token file.
    :param token_url: URL for obtaining access token.
    :param base_url: Base URL for the Schwab API.
    :param redirect_uri: Redirect URI for OAuth authorization.
    """
    # Create AccountClient instance
    account_client = AccountClient(credentials_file, token_file)

    # Get account information
    account_info = account_client.get_account_info(base_url)

    if account_info:
        print("Account information:", account_info)








if __name__ == "__main__":
    credentials_file = 'credentials.json'
    token_file = 'authorization_code_token_data.json'

    # Create OAuthClient instance
    # oauth_client = OAuthClient(
    #     credentials_file, token_file
    # )

    # oauth_client.authorization_code_grant_flow()
    # print("Access token:", oauth_client.access_token)
    # print("Refresh token:", oauth_client.refresh_token)


    base_url = 'https://api.schwabapi.com/trader/v1'
    main(credentials_file, token_file, base_url)
