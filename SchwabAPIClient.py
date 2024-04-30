import json
import requests
import logging
from pathlib import Path
from oauth_utils import OAuthClient

class SchwabAPIClient:
    """
    A class to interact with the Schwab API to retrieve account information and orders.
    """
    ACCOUNT_ACCESS_URL_KEY = 'ACCOUNT_ACCESS'
    MARKET_DATA_KEY = 'MARKET_DATA_PRODUCTION'

    def __init__(self, credentials_file, grant_flow_type_filenames_file, config_file='config.json'):
        """
        Initializes the SchwabAPIClient with OAuth credentials and base URL.

        :param credentials_file: Path to the OAuth credentials file.
        :param grant_flow_type_filenames_file: Path to the grant flow type filenames file.
        :param base_url: Base URL for the Schwab API.
        """

        self.oauth_client = OAuthClient(credentials_file, grant_flow_type_filenames_file)

        # Load configuration from either custom or default config file
        config_path = Path('config') / config_file
        self.config = self._load_config(config_path)

        # Extract base URLs from configuration
        self.base_urls = self.config.get('BASE_URLS', {})
        print(self.base_urls)
        self.base_url = self.base_urls[self.ACCOUNT_ACCESS_URL_KEY]
        print(f'base_url: {self.base_url}')

    def _load_config(self, config_file):
        try:
            # config_path = os.path.join('config', config_file)
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file '{config_file}' not found. Using default config.")
            # Load default config
            with open('config.json', 'r') as f:
                return json.load(f)

    def set_base_url(self, base_url):
        self.base_url = base_url

    def load_config_file(self):
        try:
            with open(self.grant_flow_type_filenames_file, 'r') as file:
                self.grant_flow_type_filenames = json.load(file)
                # print("Grant Flow Types and Filenames:")
                # for flow_type, filename in self.grant_flow_type_filenames.items():
                #     print(f"Grant Flow Type: {flow_type}, Filename: {filename}")

        except FileNotFoundError:
            print(f"Config file '{self.grant_flow_type_filenames_file}' not found.")
            self.grant_flow_type_filenames = {}


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












    def get_all_orders(self, days, hours, minutes):
        """
        Retrieves all orders for all accounts.

        :return: Orders JSON if successful, None otherwise.
        """
        endpoint = '/orders'

        from datetime import datetime, timedelta, timezone

        # Get current UTC time
        now_utc = datetime.now(timezone.utc)

        # Calculate the start time (30 minutes before current UTC time)
        # start_time = now_utc - timedelta(minutes=10)
        start_time = now_utc - timedelta(days=days, hours=hours, minutes=minutes)
        end_time = now_utc


        # Format the start time and current time as strings in ISO-8601 format with milliseconds and 'Z' for UTC timezone
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        to_time_str = now_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        # Define the parameters for the request
        params = {
            "fromEnteredTime": start_time_str,
            "toEnteredTime": to_time_str
        }

        # Retrieve orders from the endpoint
        response = self.get_request(endpoint, params)

        if response is not None:
            # Filter out orders based on time range
            filtered_orders = self.filter_times(response, start_time_str, to_time_str)
            
            if filtered_orders:
                # Save filtered orders to a file
                self.save_to_file(endpoint, filtered_orders)

            return filtered_orders
        else:
            # Handle error message
            error_message = "{} is not a valid value for fromEnteredTime".format(start_time_str)
            print("Failed to get data from {}. Error: {}".format(endpoint, error_message))
            print("No orders found within the specified time range.")
            return None


    def filter_times(self, trades, start_time_str, end_time_str):
        from datetime import datetime

        print(f'start_time_str: {start_time_str}')
        # Define the format of the input string
        date_format_str = "%Y-%m-%dT%H:%M:%S.%fZ"
        date_format = '%Y-%m-%dT%H:%M:%S'

        # # Parse start time and end time strings
        start_time = datetime.strptime(start_time_str, date_format_str)
        end_time = datetime.strptime(end_time_str, date_format_str)
        # print(f'start_time: {start_time}')
        # print(f'end_time: {end_time}')

        filtered_trades = []
        for trade in trades:
            # Remove the timezone offset from the enteredTime string
            entered_time_str = trade["enteredTime"][:-5]  # Remove the timezone offset
            print(f'entered: {entered_time_str}')
            # Parse enteredTime string into datetime object
            entered_time = datetime.strptime(entered_time_str, date_format)

            # Filter trades based on time range
            if start_time <= entered_time <= end_time:
                filtered_trades.append(trade)

        return filtered_trades









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
        print(response)
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




    def read_orders_from_file(self, file_path):
        """
        Reads orders from a JSON file.

        :param file_path: Path to the JSON file containing orders.
        :return: List of orders if successful, None otherwise.
        """
        try:
            with open(file_path, 'r') as file:
                orders = json.load(file)
            return orders
        except FileNotFoundError:
            print("File not found:", file_path)
            return None
        except Exception as e:
            print("Error reading orders from file:", e)
            return None

    # def process_orders_from_file(self, file_path):
    #     """
    #     Process orders read from a JSON file and return a list of orderId's.

    #     :param file_path: Path to the JSON file containing orders.
    #     :return: List of orderId's if successful, None otherwise.
    #     """
    #     # Read orders from file
    #     orders = self.read_orders_from_file(file_path)

    #     # Check if orders were successfully read
    #     if orders is not None:
    #         # Extract orderId's from orders
    #         order_ids = [order.get("orderId") for order in orders]
    #         return order_ids
    #     else:
    #         # Handle case where reading orders failed
    #         print("Failed to read orders from file. Check the logs for details.")
    #         return None



    def process_orders_from_file(self, file_path):
        """
        Process orders read from a JSON file and return a list of orderId's with status 'PENDING_ACTIVATION'.

        :param file_path: Path to the JSON file containing orders.
        :return: List of orderId's with status 'PENDING_ACTIVATION' if successful, None otherwise.
        """
        # Read orders from file
        orders = self.read_orders_from_file(file_path)

        # Check if orders were successfully read
        if orders is not None:
            # Extract orderId's with status 'PENDING_ACTIVATION' from orders
            pending_activation_order_ids = [order["orderId"] for order in orders if order.get("status") == "PENDING_ACTIVATION"]
            return pending_activation_order_ids
        else:
            # Handle case where reading orders failed
            print("Failed to read orders from file. Check the logs for details.")
            return None