import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

async def refresh_token_timer():
    while True:
        logging.info("Refreshing access token...")
        # Your code to refresh the access token here
        await asyncio.sleep(60)  # Refresh token every 60 seconds

async def print_periodically():
    while True:
        logging.info("Printing periodically...")
        await asyncio.sleep(10)  # Print every 10 seconds
        print('Can you see me ?')

async def main():
    # Start tasks
    tasks = [refresh_token_timer(), print_periodically()]
    await asyncio.gather(*tasks)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
