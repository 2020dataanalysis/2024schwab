import time
from SchwabAPIClient import SchwabAPIClient



def cancel_previous_orders(client):
    status = 'WORKING'

    days = 0
    hours = 0
    minutes = 2

    order_ids = client.cancel_all_orders(days, hours, minutes, status)
    print(f'The following ids were cancelled:{order_ids}')


# def create_order(client, price, gap):
#     # Calculate stop prices
#     gap = .3
#     round(price, 2)
#     upper_price = round(price + gap, 2)
#     lower_price = round(price - gap, 2)
    
#     # Print stop prices
#     print("Upper order:", upper_price)
#     print("Lower order:", lower_price)
#     #   STOP ORDER
#     # order_data_buy = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": upper_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
#     # order_data_sell = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": lower_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}

#     # After Hours
#     order1 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": upper_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 100, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
#     order2 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": lower_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 100, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}


#     # placed_order = client.place_order(client.hashValue, order1)
#     placed_order = client.place_order(client.hashValue, order2)


def place_order(client, order):
    client.place_order(order)
    orders = client.get_all_orders(0, 0, 1, 'WORKING')
    order_ids = client.get_IDs(orders)      # Of orders just made
    if order_ids:
        print(f'order_ids: {order_ids}')
    else:
        print('order_id1: Order not placed')

    return order_ids



def place_bollinger_orders(price):
    gap = .3
    price = round(price, 2)
    upper_price = round(price + gap, 2)
    lower_price = round(price - gap, 2)
    print("Upper order:", upper_price)
    print("Lower order:", lower_price)
    #   STOP ORDER
    order1 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": upper_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    order2 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": lower_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}

    # After Hours
    # order1 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": upper_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 100, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
    # order2 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": lower_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 100, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}

    id1 = place_order(client, order1)
    time.sleep(5)
    id2 = place_order(client, order2)
    if len(id1) == 1:
        if len(id2) == 1:
            if (id1 != id2):
                print('id1 != id2')
                return id1[0], id2[0]

    return None


def get_orders(client, days, hours, minutes, status):
    orders = client.get_all_orders(days, hours, minutes, status)
    return orders


def get_working_order_ids(client, orders):
    client.get_IDs(orders)


def process_order(client, id):
    order = client.get_specific_order(id)
    if order['status'] == 'FILLED':
        order_ids_filled.append(id)
    else:
        client.cancel_order(id)



if __name__ == "__main__":
    # Initialize SchwabAPIClient with credentials and base URL
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    base_url = 'https://api.schwabapi.com/trader/v1'

    client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)

    # Get account information
    account_info = client.get_account_info()
    client.set_account_number_hash_value(account_info[0]['hashValue'])

    if account_info:
        print("Account information:", account_info)
        print(f'client Account Number hash value: {client.get_account_number_hash_value}')

    symbol = 'SPY'
    cancel_previous_orders(client)
    order_ids_filled = []


    while True:
        ticker_data = client.get_ticker_data(symbol)
        # print(ticker_data)
    
        # current_price = ticker_data[symbol]['quote']['lastPrice']
        current_price = 0
        # Assuming ticker_data is a dictionary containing symbol as keys and quote data as values
        # symbol is the symbol for which you want to get the current price
        if symbol in ticker_data and ticker_data[symbol] is not None and 'quote' in ticker_data[symbol] and 'lastPrice' in ticker_data[symbol]['quote']:
            price = ticker_data[symbol]['quote']['lastPrice']
        print(price)

        id1, id2 = place_bollinger_orders(price)
        time.sleep(60)

        process_order(client, id1)
        process_order(client, id2)
