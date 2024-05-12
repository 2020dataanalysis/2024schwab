#   Can only have 1 stop above or below.

import time
import logging
import asyncio
from SchwabAPIClient import SchwabAPIClient

class TradingBot:
    def __init__(self, credentials_file, grant_flow_type_filenames_file):
        self.client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)
        account_info = self.client.get_account_info()
        self.client.set_account_number_hash_value(account_info[0]['hashValue'])

        if account_info:
            print("Account information:", account_info)
            print(f'client Account Number hash value: {self.client.get_account_number_hash_value()}')

        self.order_ids_working = []
        self.order_ids_filled = []

    def cancel_previous_orders(self, days=0, hours=0, minutes=0, seconds=0):
        status = 'WORKING'
        # status = 'PENDING_ACTIVATION'
        order_ids = self.client.cancel_all_orders(days, hours, minutes, seconds, status)
        print(f'The following ids were cancelled:{order_ids}')

    def place_order(self, order):
        self.client.place_order(order)
        time.sleep(2)

        #   Assert that there is only 1 working order
        orders_working = self.client.get_all_orders(0, 0, 0, 10, 'WORKING')
        orders_filled = self.client.get_all_orders(0, 0, 0, 5, 'FILLED')
        order_ids = self.client.get_IDs(orders_working)

        order_ids_filled = self.client.get_IDs(orders_filled)   #  May assume only if no cancel & no working
        #   For now assuming not filled, may need to work on this later.

        if order_ids:
            print(f'{order_ids} - Working ---> ', end='', flush=True)
            self.order_ids_working.append(order_ids[0])
            assert( len(order_ids) == 1)    # If not 1 then need to use list comprehension

        else:
            print('order_id1: Order not placed')
            orders_cancelled = self.client.get_all_orders(0, 0, 0, 10, 'CANCELLED')
            if orders_cancelled:
                order_ids_cancelled = self.client.get_IDs(orders_cancelled)
                print(f'orders_cancelled: {order_ids_cancelled}')
        return order_ids

    def place_bollinger_orders(self, symbol, price):
        gap = .1
        upper_price = round(price + gap, 2)
        lower_price = round(price - gap, 2)
        quantity = 1
        if SESSION == 'NORMAL':
            #   Normal Hours
            order1 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": upper_price, "orderLegCollection": [{"instruction": "BUY", "quantity": quantity, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}
            order2 = {"orderType": "STOP",  "session": "NORMAL",  "duration": "DAY",  "orderStrategyType": "SINGLE", "stopPrice": lower_price, "orderLegCollection": [{"instruction": "SELL_SHORT", "quantity": quantity, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}
        else:
            # After Hours
            order1 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": lower_price, "orderLegCollection": [{"instruction": "BUY", "quantity": quantity, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}
            order2 = {"orderType": "LIMIT",  "session": "EXTO",  "duration": "DAY",  "orderStrategyType": "SINGLE", "price": upper_price, "orderLegCollection": [{"instruction": "SELL", "quantity": quantity, "instrument": { "symbol": symbol, "assetType": "EQUITY"}}]}

        id1_list = self.place_order(order1)
        id1 = id2 = None
        if len(id1_list):
            id1 = id1_list[0]



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
            # if 'status' in order:
            status = order['status']
            if status == 'WORKING':
                self.client.cancel_order(id)
                self.order_ids_working
                
                print(f'{id} - cancelled order')
                index = self.order_ids_working.index(id)
                id2_list_popped = self.order_ids_working.pop(index)

            if status == 'FILLED':
                self.order_ids_filled.append(id)
            elif status == 'CANCELLED':
                index = self.order_ids_working.index(id)
                id2_list_popped = self.order_ids_working.pop(index)





# async def refresh_token_timer(bot):
#     logging.info('async def refresh_token_timer')
#     expiration_time = bot.client.access_token_expiration_time
#     logging.info(f'expiration_time: {expiration_time}')
#     while True:
#         logging.info("Refreshing access token...")
#         # Your code to refresh the access token here
#         await asyncio.sleep(expiration_time - time.time() - 10)  # Refresh token 10 seconds before expiration






if __name__ == "__main__":
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    bot = TradingBot(credentials_file, grant_flow_type_filenames_file)
    symbol = 'SPY'
    # bot.cancel_previous_orders(0, 2, 0, 0)
    SESSION = 'NORMAL'
    # SESSION = 'EXTO'
    # Configure logging
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
    
    # asyncio.run(refresh_token_timer(bot))


    # while True:
    #     ticker_data = bot.client.get_ticker_data(symbol)
    #     price = 0
    #     try:
    #         if symbol in ticker_data and ticker_data[symbol] is not None and 'quote' in ticker_data[symbol] and 'lastPrice' in ticker_data[symbol]['quote']:
    #             price = ticker_data[symbol]['quote']['lastPrice']
    #             print(price)
    #     except Exception as e:
    #         # print()
    #         print(e)

        # if price:
        #     id1, id2 = bot.place_bollinger_orders(symbol, price)
        #     time.sleep(20)

        #     if id1:
        #         bot.process_order(id1)
        #     if id2:
        #         bot.process_order(id2)

        #     print(f'{bot.order_ids_filled}, {bot.order_ids_working} - Filled, Working')
        # print('.', end='')


        # print(bot.client.access_token_expiration_time)
        # logging.info("Refreshing access token...")
