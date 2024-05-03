import time

def get_current_price():
    # Simulated function to get the current price
    # Replace this with your actual function to get the current price from a data source
    return 50.00  # Simulated current price

def create_stop_orders(current_price):
    # Calculate stop prices
    above_stop_price = current_price + 0.20
    below_stop_price = current_price - 0.20
    
    # Print stop prices
    print("Stop order above:", above_stop_price)
    print("Stop order below:", below_stop_price)

# Continuous loop to get current price and create stop orders
while True:
    current_price = get_current_price()
    create_stop_orders(current_price)
    time.sleep(5)  # Adjust the sleep time as needed
