import time
import logging
import asyncio
from SchwabAPIClient import SchwabAPIClient


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
    def __init__(self, credentials_file, grant_flow_type_filenames_file):
        self.client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)
        account_info = self.client.get_account_info()
        self.client.set_account_number_hash_value(account_info[0]['hashValue'])
 
        if account_info:
            logger.info("Account information: %s", account_info)
            logger.info('Client Account Number hash value: %s', self.client.get_account_number_hash_value())


async def token_timer():
    remaining_time = bot.client.oauth_client.refresh_token_timer()
    logger.info(f'remaining_time: {remaining_time}')
    remaining_time = 10
    await asyncio.sleep(remaining_time)
    asyncio.create_task(token_timer())


if __name__ == "__main__":
    logger = configure_logging()
    logger.info('Initial Log')
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    bot = TradingBot(credentials_file, grant_flow_type_filenames_file)
    asyncio.run(token_timer())

    while True:
        pass