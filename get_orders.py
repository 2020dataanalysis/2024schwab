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


    # Retrieve all orders for all accounts
    print('\nGet All Orders')
    status = None
    # status = 'FILLED'
    # status = 'PENDING_ACTIVATION'
    status = 'WORKING'
    if status:
        print(f'where status = {status}')
    else:
        print('where status:')
        print(client.config['ORDER_STATUS_VALUES'])

    days = 0
    hours = 1
    minutes = 20
    all_orders = client.get_all_orders(days, hours, minutes, status)
    print("All Orders:", all_orders)