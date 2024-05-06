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
        order_ids = self.client.cancel_all_orders(days, hours, minutes, status)
        print(f'The following ids were cancelled:{order_ids}')

    def place_order(self, order):
        self.client.place_order(order)
        orders = self.client.get_all_orders(0, 0, 1, 'WORKING')
        order_ids = self.client.get_IDs(orders)      
        if order_ids:
            print(f'order_ids: {order_ids}')
        else:
            print('order_id1: Order not placed')

        return order_ids

    def place_bollinger_orders(self, price):
        gap = .3
        price = round(price, 2)
        upper_price = round(price + gap, 2)
        lower_price = round(price - gap, 2)
        print("Upper order:", upper_price)
        print("Lower order:", lower_price)
        order1 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": upper_price, "orderLegCollection": [{"instruction": "BUY", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
        order2 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": lower_price, "orderLegCollection": [{"instruction": "SELL", "quantity": 1, "instrument": { "symbol": "SPY", "assetType": "EQUITY"}}]}
        id1 = self.place_order(order1)
        time.sleep(5)
        id2 = self.place_order(order2)
        if len(id1) == 1 and len(id2) == 1 and id1 != id2:
            print('id1 != id2')
            return id1[0], id2[0]
        return None

    def process_order(self, id):
        order = self.client.get_specific_order(id)
        if order['status'] == 'FILLED':
            self.order_ids_filled.append(id)
        else:
            self.client.cancel_order(id)


if __name__ == "__main__":
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'

    bot = TradingBot(credentials_file, grant_flow_type_filenames_file)

    symbol = 'SPY'
    bot.cancel_previous_orders(0, 1, 0)

    while True:
        ticker_data = bot.client.get_ticker_data(symbol)
        price = 0
        if symbol in ticker_data and ticker_data[symbol] is not None and 'quote' in ticker_data[symbol] and 'lastPrice' in ticker_data[symbol]['quote']:
            price = ticker_data[symbol]['quote']['lastPrice']
            print(price)

        id1, id2 = bot.place_bollinger_orders(price)
        time.sleep(60)

        bot.process_order(id1)
        bot.process_order(id2)

        print(f'Filled Orders: {bot.order_ids_filled}')
