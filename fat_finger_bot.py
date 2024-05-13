import time
import logging
import asyncio
from SchwabAPIClient import SchwabAPIClient

# # Set up logging configuration
# logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Define a stream handler to print logs to the console
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# logging.getLogger('').addHandler(console)


times_up = False

def configure_logging():
    # Set up logging configuration
    logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Define a stream handler to print logs to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console)

    return logging.getLogger(__name__)





class TradingBot:
    # def __init__(self, credentials_file, grant_flow_type_filenames_file):
        # pass

    def __init__(self, credentials_file, grant_flow_type_filenames_file):
        # self.logger = logger
        # logger.info('***************************************** - ')
        # Initialize Schwab API client
        


        self.client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)
        account_info = self.client.get_account_info()
        self.client.set_account_number_hash_value(account_info[0]['hashValue'])
        # self.logger.info('***************************************** - ')

        if account_info:
            # logger.info("Account information: %s", account_info)
            # logger.info('Client Account Number hash value: %s', self.client.get_account_number_hash_value())
            pass

        self.order_ids_working = []
        self.order_ids_filled = []

    def cancel_previous_orders(self, days=0, hours=0, minutes=0, seconds=0):
        status = 'WORKING'
        order_ids = self.client.cancel_all_orders(days, hours, minutes, seconds, status)
        # logger.info('The following ids were cancelled: %s', order_ids)

    def place_order(self, order):
        self.client.place_order(order)
        time.sleep(2)

        # Assert that there is only 1 working order
        orders_working = self.client.get_all_orders(0, 0, 0, 10, 'WORKING')
        order_ids = self.client.get_IDs(orders_working)

        if order_ids:
            # logging.info('%s - Working', order_ids)
            self.order_ids_working.append(order_ids[0])
            assert len(order_ids) == 1
        else:
            # logging.info('Order not placed')
            orders_cancelled = self.client.get_all_orders(0, 0, 0, 10, 'CANCELLED')
            if orders_cancelled:
                order_ids_cancelled = self.client.get_IDs(orders_cancelled)
                # logging.info('Orders cancelled: %s', order_ids_cancelled)
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
            status = order['status']
            if status == 'WORKING':
                self.client.cancel_order(id)
                self.order_ids_working
                # logging.info('%s - cancelled order', id)
                index = self.order_ids_working.index(id)
                id2_list_popped = self.order_ids_working.pop(index)

            if status == 'FILLED':
                self.order_ids_filled.append(id)
            elif status == 'CANCELLED':
                index = self.order_ids_working.index(id)
                id2_list_popped = self.order_ids_working.pop(index)


async def token_timer():
    global times_up
    # logger.info("token_timer: ")
    remaining_time = bot.client.oauth_client.refresh_token_timer()
    # logger.info(f'remaining_time: {remaining_time}')
    times_up = True
    await asyncio.sleep(10)
    asyncio.create_task(token_timer())





if __name__ == "__main__":
    # global times_up
    # Configure logging
    logger = configure_logging()
    logger.info('Initial Log')
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    bot = TradingBot(credentials_file, grant_flow_type_filenames_file)
    symbol = 'SPY'
    bot.cancel_previous_orders(0, 2, 0, 0)
    SESSION = 'NORMAL'
    logger.info('while True')
    asyncio.run(token_timer())

    while True:
        ticker_data = bot.client.get_ticker_data(symbol)
        price = 0
        try:
            if symbol in ticker_data and ticker_data[symbol] is not None and 'quote' in ticker_data[symbol] and 'lastPrice' in ticker_data[symbol]['quote']:
                price = ticker_data[symbol]['quote']['lastPrice']
                print(price)
        except Exception as e:
            # print()
            print(e)

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

        remaining_time = bot.client.oauth_client.refresh_token_timer()
        # print(f'loop: remaining_time: {remaining_time}')
        # logger.info("loop")
        
        if times_up:
            times_up = False
            print('times_up')
            remaining_time = bot.client.oauth_client.refresh_token_timer()
            logging.info(f'loop: remaining_time: {remaining_time}')


        time.sleep(1)
