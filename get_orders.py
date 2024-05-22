import logging
from SchwabAPIClient import SchwabAPIClient


class Schwab:
    # def __init__(self, credentials_file, grant_flow_type_filenames_file):
        # pass

    def __init__(self, credentials_file, grant_flow_type_filenames_file):
        # Initialize Schwab API client
        self.client = SchwabAPIClient(credentials_file, grant_flow_type_filenames_file)
        account_info = self.client.get_account_info()
        self.client.set_account_number_hash_value(account_info[0]['hashValue'])

        if account_info:
            # logger.info("Account information: %s", account_info)
            # logger.info('Client Account Number hash value: %s', self.client.get_account_number_hash_value())
            pass


def configure_logging():
    # Set up logging configuration
    logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Define a stream handler to print logs to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console)
    return logging.getLogger(__name__)



if __name__ == "__main__":
    # Configure logging
    logger = configure_logging()
    logger.info('Initial Log')
    credentials_file = 'credentials.json'
    grant_flow_type_filenames_file = 'grant_flow_type_filenames.json'
    schwab = Schwab(credentials_file, grant_flow_type_filenames_file)



    # base_url = 'https://api.schwabapi.com/trader/v1'
    # # status = 'PENDING_ACTIVATION'
    status = 'FILLED'


    days = 1
    hours = 0
    minutes = 0
    seconds = 0
    all_orders = schwab.client.get_all_orders(days, hours, minutes, seconds, status)
    print("All Orders:", all_orders)
