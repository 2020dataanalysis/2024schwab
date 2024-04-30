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

    #   Working
    # Retrieve all orders for all accounts
    print('\nGet All Orders')
    days = 1
    all_orders = client.get_all_orders(days)
    if all_orders:
        print("All Orders:", all_orders)




    # # Retrieve orders for a specific account
    # account_number = "123456789"
    # account_orders = client.get_account_orders(account_number)
    # if account_orders:
    #     print(f"Orders for Account {account_number}:", account_orders)

    # # Retrieve a specific order for a specific account
    # order_id = "987654321"
    # specific_order = client.get_specific_order(account_number, order_id)
    # if specific_order:
    #     print(f"Specific Order {order_id}:", specific_order)

    # Place an order for a specific account
    account_number = client.hashValue
    # print(f'account_number: {account_number}')
    # order_data = {"orderType": "LIMIT", "session": "NORMAL", "duration": "DAY", "orderStrategyType": "SINGLE", "price": 10.00, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": {"symbol": "INTC", "assetType": "EQUITY"}}]}  # Fill in order data
    # order_data =   {"orderType": "LIMIT",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": 500.00, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    # order_data =   {"orderType": "LIMIT",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": 500.00, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    order_data =   {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": 509.80, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}

    # # Preview an order for a specific account (if available)
    # previewed_order = client.preview_order(account_number, order_data)
    # if previewed_order:
    #     print("Previewed Order:", previewed_order)

    # # Replace an existing order for a specific account
    # updated_order_data = {...}  # Fill in updated order data
    # updated_order = client.replace_order(account_number, order_id, updated_order_data)
    # if updated_order:
    #     print("Updated Order:", updated_order)

    # # Cancel an existing order for a specific account
    # cancellation_result = client.cancel_order(account_number, order_id)
    # if cancellation_result:
    #     print("Order Cancellation Successful")
