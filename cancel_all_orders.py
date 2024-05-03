from SchwabAPIClient import SchwabAPIClient


if __name__ == "__main__":
    # Initialize SchwabAPIClient with credentials and base URL
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    base_url = 'https://api.schwabapi.com/trader/v1'

    client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)

    print('\nAccount Information:')
    # Get account information
    account_info = client.get_account_info()
    client.hashValue = account_info[0]['hashValue']

    if account_info:
        print("Account information:", account_info)
    print(f'client hashValue: {client.hashValue}')

    # status = 'PENDING_ACTIVATION'
    status = 'WORKING'

    days = 0
    hours = 1
    minutes = 10

    order_ids = client.cancel_all_orders(days, hours, minutes, status)
    print(f'The following ids were cancelled:{order_ids}')
