from SchwabAPIClient import SchwabAPIClient


if __name__ == "__main__":
    # Initialize SchwabAPIClient with credentials and base URL
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)

    print('\nAccount Information:')
    # Get account information
    account_info = client.get_account_info()
    client.hashValue = account_info[0]['hashValue']
    print(f'client hashValue: {client.hashValue}')
    if account_info:
        print("Account information:", account_info)

    # Place an order for a specific account
    account_number = client.hashValue
    # print(f'account_number: {account_number}')

    session_time = {
        "NORMAL": "NORMAL",
        "EXTO": "EXTO"
    }


    #   MARKET ORDER
    # order_data =   {"orderType": "MARKET",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "orderLegCollection": [{"instruction": "BUY", "quantity": 100, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}

    #   LIMIT ORDER
    session = session_time['NORMAL']
    # order_data = {"orderType": "LIMIT", "session": "NORMAL", "duration": "DAY", "orderStrategyType": "SINGLE", "price": 10.00, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": {"symbol": "INTC", "assetType": "EQUITY"}}]}  # Fill in order data
    # order_data = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": 503.80, "orderLegCollection": [{"instruction": "BUY", "quantity": 100, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    order_data = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": 503.50, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}

    #   STOP ORDER
    # order_data = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": 509.50, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    
    placed_order = client.place_order(account_number, order_data)
    if placed_order:
        print("Placed Order:", placed_order.text)
