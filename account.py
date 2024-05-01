import json
from OauthClient import OAuthClient
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

    def set_base_url(self, base_url):
        self.base_url = base_url


    def save_to_file(self, endpoint, response):
        # file = endpoint
        name = endpoint.replace('/', '_')
        file_name = f'{name}.json'
        with open(file_name, 'w') as file:
            json.dump(response, file)
        print(f"Data saved successful: {file_name}")


    def get_account_info(self):
        """
        Retrieves account information for the specified account number.

        :param account_number: The account number for which to retrieve information.
        :return: Account information JSON if successful, None otherwise.
        """

        endpoint = '/accounts/accountNumbers'
        response = self.get_request(endpoint)
        self.save_to_file(endpoint, response)
        return response



    def get_account(self):
        endpoint = "/accounts"
        response = self.get_request(endpoint)
        self.save_to_file(endpoint, response)
        return response


    def get_account2(self):
        endpoint = f'/accounts/{self.hashValue}'
        response = self.get_request(endpoint)
        self.save_to_file(endpoint, response)
        return response



    def get_orders(self):
        url_endpoint = f'/accounts/{self.hashValue}/orders'
        endpoint = f'/accounts/orders'
        response = self.get_request(url_endpoint)
        self.save_to_file(endpoint, response)
        return response


    def get_request(self, endpoint):
        """
        Retrieves account information for the specified account number.

        :param account_number: The account number for which to retrieve information.
        :return: Account information JSON if successful, None otherwise.
        """

        headers = {
            'Authorization': f'Bearer {self.oauth_client.access_token}',
            'Accept': 'application/json'
            }
        url_endpoint = f"{self.base_url}{endpoint}"
        response = requests.get(url_endpoint, headers=headers)

        print(response)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to get account information. Error:", response.text)
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
    account_client.set_base_url(base_url)

    # Get account information
    account_info = account_client.get_account_info()
    account_client.hashValue = account_info[0]['hashValue']

    if account_info:
        print("Account information:", account_info)

    # account = account_client.get_account()
    # if account:
    #     print("Account:", account)



    # acc = account_client.get_account2()
    # print(acc)






    # ORDERS
    # /accounts/{accountNumber}/orders
    orders = account_client.get_orders()





import datetime
import time
import json
from OauthClient import OAuthClient

if __name__ == "__main__":
    # Initialize OAuthClient with credentials and token files
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'

    base_url = 'https://api.schwabapi.com/trader/v1'
    main(credentials_file, grant_flow_type_filenames_file, base_url)
