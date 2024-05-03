import time
from SchwabAPIClient import SchwabAPIClient



def cancel_previous_orders(client):
    status = 'WORKING'

    days = 0
    hours = 0
    minutes = 10

    order_ids = client.cancel_all_orders(days, hours, minutes, status)
    print(f'The following ids were cancelled:{order_ids}')


def create_stop_orders(client, price):
    # Calculate stop prices
    gap = .25
    round(price, 2)
    upper_price = round(price + gap, 2)
    lower_price = round(price - gap, 2)
    
    # Print stop prices
    print("Upper order:", upper_price)
    print("Lower order:", lower_price)
    #   STOP ORDER
    # order_data_buy = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": upper_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    # order_data_sell = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": lower_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}

    # After Hours
    # order1 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": upper_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    order2 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": lower_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 100, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}


    # placed_order = client.place_order(client.hashValue, order1)
    placed_order = client.place_order(client.hashValue, order2)



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

    symbol = 'SPY'
    # Continuous loop to get current price and create stop orders
    while True:
        ticker_data = client.get_ticker_data(symbol)
        # print(ticker_data)
        current_price = ticker_data[symbol]['quote']['lastPrice']
        print(current_price)

        cancel_previous_orders(client)
        time.sleep(1)
        create_stop_orders(client, current_price)
        time.sleep(60)  # Adjust the sleep time as needed
