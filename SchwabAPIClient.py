import json
import requests
from oauth_utils import OAuthClient

class SchwabAPIClient:
    """
    A class to interact with the Schwab API to retrieve account information and orders.
    """

    def __init__(self, credentials_file, grant_flow_type_filenames_file, base_url):
        """
        Initializes the SchwabAPIClient with OAuth credentials and base URL.

        :param credentials_file: Path to the OAuth credentials file.
        :param grant_flow_type_filenames_file: Path to the grant flow type filenames file.
        :param base_url: Base URL for the Schwab API.
        """
        self.base_url = base_url
        self.oauth_client = OAuthClient(credentials_file, grant_flow_type_filenames_file)

    def save_to_file(self, endpoint, response):
        """
        Saves API response to a JSON file.

        :param endpoint: API endpoint.
        :param response: API response data.
        """
        file_name = f'{endpoint.replace("/", "_")}.json'
        with open(file_name, 'w') as file:
            json.dump(response, file)
        print(f"Data saved successfully: {file_name}")

    def get_request(self, endpoint, params=None):
        """
        Makes a GET request to the API.

        :param endpoint: API endpoint.
        :param params: Query parameters (optional).
        :return: JSON response if successful, None otherwise.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.oauth_client.access_token}',
            'Accept': 'application/json'
        }
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get data from {endpoint}. Error: {response.text}")
            return None

    def post_request(self, endpoint, data=None):
        """
        Makes a POST request to the API.

        :param endpoint: API endpoint.
        :param data: Request payload data (optional).
        :return: JSON response if successful, None otherwise.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.oauth_client.access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to post data to {endpoint}. Error: {response.text}")
            return None

    def put_request(self, endpoint, data=None):
        """
        Makes a PUT request to the API.

        :param endpoint: API endpoint.
        :param data: Request payload data (optional).
        :return: JSON response if successful, None otherwise.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.oauth_client.access_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.put(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to put data to {endpoint}. Error: {response.text}")
            return None

    def delete_request(self, endpoint):
        """
        Makes a DELETE request to the API.

        :param endpoint: API endpoint.
        :return: True if successful, False otherwise.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.oauth_client.access_token}'
        }
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            print(f"Successfully deleted data from {endpoint}")
            return True
        else:
            print(f"Failed to delete data from {endpoint}. Error: {response.text}")
            return False

    def get_all_orders(self):
        """
        Retrieves all orders for all accounts.

        :return: Orders JSON if successful, None otherwise.
        """
        endpoint = '/orders'
        response = self.get_request(endpoint)
        if response:
            self.save_to_file(endpoint, response)
        return response

    def get_account_orders(self, account_number):
        """
        Retrieves all orders for a specific account.

        :param account_number: Account number for which to retrieve orders.
        :return: Orders JSON if successful, None otherwise.
        """
        endpoint = f'/accounts/{account_number}/orders'
        response = self.get_request(endpoint)
        if response:
            self.save_to_file(endpoint, response)
        return response

    def get_specific_order(self, account_number, order_id):
        """
        Retrieves a specific order by its ID for a specific account.

        :param account_number: Account number for which to retrieve the order.
        :param order_id: ID of the order to retrieve.
        :return: Order JSON if successful, None otherwise.
        """
        endpoint = f'/accounts/{account_number}/orders/{order_id}'
        response = self.get_request(endpoint)
        if response:
            self.save_to_file(endpoint, response)
        return response

    def place_order(self, account_number, order_data):
        """
        Places an order for a specific account.

        :param account_number: Account number for which to place the order.
        :param order_data: Data representing the order to be placed.
        :return: Order JSON if successful, None otherwise.
        """
        endpoint = f'/accounts/{account_number}/orders'
        response = self.post_request(endpoint, data=order_data)
        if response:
            self.save_to_file(endpoint, response)
        return response

    def preview_order(self, account_number, order_data):
        """
        Previews an order for a specific account.

        :param account_number: Account number for which to preview the order.
        :param order_data: Data representing the order to be previewed.
        :return: Order preview JSON if successful, None otherwise.
        """
        endpoint = f'/accounts/{account_number}/previewOrder'
        response = self.post_request(endpoint, data=order_data)
        if response:
            self.save_to_file(endpoint, response)
        return response

    def replace_order(self, account_number, order_id, updated_data):
        """
        Replaces an existing order for a specific account.

        :param account_number: Account number for which to replace the order.
        :param order_id: ID of the order to be replaced.
        :param updated_data: Updated data representing the order.
        :return: Updated order JSON if successful, None otherwise.
        """
        endpoint = f'/accounts/{account_number}/orders/{order_id}'
        response = self.put_request(endpoint, data=updated_data)
        if response:
            self.save_to_file(endpoint, response)
        return response

    def cancel_order(self, account_number, order_id):
        """
        Cancels an existing order for a specific account.

        :param account_number: Account number for which to cancel the order.
        :param order_id: ID of the order to be cancelled.
        :return: True if successful, False otherwise.
        """
        endpoint = f'/accounts/{account_number}/orders/{order_id}'
        return self.delete_request(endpoint)
