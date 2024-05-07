#   Can only have 1 stop above or below.

import time
from SchwabAPIClient import SchwabAPIClient

class TradingBot:
    def __init__(self, credentials_file, grant_flow_type_filenames_file):
        self.client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)
        account_info = self.client.get_account_info()
        self.client.set_account_number_hash_value(account_info[0]['hashValue'])

        if account_info:
            print("Account information:", account_info)
            print(f'client Account Number hash value: {self.client.get_account_number_hash_value()}')

        self.order_ids_filled = []

    def cancel_previous_orders(self, days=0, hours=0, minutes=0):
        status = 'WORKING'
        # status = 'PENDING_ACTIVATION'
        order_ids = self.client.cancel_all_orders(days, hours, minutes, status)
        print(f'The following ids were cancelled:{order_ids}')

    def place_order(self, order):
        self.client.place_order(order)
        time.sleep(1)

        #   Assert that there is only 1 working order
        orders = self.client.get_all_orders(0, 0, 1, 'WORKING')
        order_ids = self.client.get_IDs(orders)
        # if order_ids:
        #     print(f'order_ids: {order_ids}')
        # else:
        #     print('order_id1: Order not placed')
        return order_ids

    def place_bollinger_orders(self, symbol, price):
        gap = .01
        # price = round(price, 2)
        upper_price = round(price + gap, 2)
        lower_price = round(price - gap, 2)
        print("Upper order:", upper_price)
        print("Lower order:", lower_price)
        if SESSION == 'NORMAL':
            #   Normal Hours
            order1 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": upper_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}
            order2 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": lower_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}
        else:
            # After Hours
            order1 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": lower_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}
            order2 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": upper_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}

        id1_list = self.place_order(order1)
        # assert(len(id1_list) == 1)        # Error when gets filled immediately
        #               need to also check if filled.
        id1 = id1_list[0]
        id2 = None      # Do not need
        if (SESSION == 'EXTO' and not self.order_ids_filled):
            return id1, None

        time.sleep(1)
        id2_list = self.place_order(order2)
        if (len(id2_list) == 2):
            index = id2_list.index(id1)
            print("Index of", id1, "is:", index)
            id2_list_popped = id2_list.pop(index)
            assert(len(id2_list) == 1)
            id2 = id2_list[0]
        elif (len(id2_list) == 1):
            # assert(len(id2_list) == 1)        Error
            id2 = id2_list[0]
            assert(id1 != id2)
        else:
            return None, None
        return id1, id2


    def process_order(self, id):
        order = self.client.get_specific_order(id)
        if not order:
            print(f'order is None: {order}')
        else:
            if 'status' in order:
                if order['status'] == 'FILLED':
                    self.order_ids_filled.append(id)
                else:
                    self.client.cancel_order(id)
                    print(f'cancelled order: {id}')


if __name__ == "__main__":
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    bot = TradingBot(credentials_file, grant_flow_type_filenames_file)
    symbol = 'SPY'
    bot.cancel_previous_orders(0, 1, 0)
    # SESSION = 'NORMAL'
    SESSION = 'EXTO'

    while True:
        ticker_data = bot.client.get_ticker_data(symbol)
        price = 0
        if symbol in ticker_data and ticker_data[symbol] is not None and 'quote' in ticker_data[symbol] and 'lastPrice' in ticker_data[symbol]['quote']:
            price = ticker_data[symbol]['quote']['lastPrice']
            print(price)

        id1, id2 = bot.place_bollinger_orders(symbol, price)
        time.sleep(60)

        if id1:
            bot.process_order(id1)
        if id2:
            bot.process_order(id2)

        print(f'Filled Orders: {bot.order_ids_filled}')
