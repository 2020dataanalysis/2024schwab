import json
from datetime import datetime

# Define the JSON data
json_data = '''
{
    "session": "SEAMLESS",
    "duration": "DAY",
    "orderType": "LIMIT",
    "complexOrderStrategyType": "NONE",
    "quantity": 20.0,
    "filledQuantity": 0.0,
    "remainingQuantity": 20.0,
    "requestedDestination": "AUTO",
    "destinationLinkName": "AutoRoute",
    "price": 501.0,
    "orderLegCollection": [
        {
            "orderLegType": "EQUITY",
            "legId": 1,
            "instrument": {
                "assetType": "COLLECTIVE_INVESTMENT",
                "cusip": "78462F103",
                "symbol": "SPY",
                "description": "SPDR S&P 500 ETF",
                "instrumentId": 1772540,
                "type": "EXCHANGE_TRADED_FUND"
            },
            "instruction": "BUY",
            "positionEffect": "OPENING",
            "quantity": 20.0
        }
    ],
    "orderStrategyType": "SINGLE",
    "orderId": 1000436258264,
    "cancelable": true,
    "editable": true,
    "status": "PENDING_ACTIVATION",
    "enteredTime": "2024-04-29T02:30:21+0000",
    "tag": "API_TOS:TRADE_ALL",
    "accountNumber": 82167359
}
'''

# Parse the JSON data
order = json.loads(json_data)

# Define the time range for filtering
start_time = datetime.strptime("2024-04-29T00:00:00+0000", "%Y-%m-%dT%H:%M:%S%z")
end_time = datetime.strptime("2024-04-29T23:59:59+0000", "%Y-%m-%dT%H:%M:%S%z")

# Convert enteredTime to datetime object
entered_time = datetime.strptime(order["enteredTime"], "%Y-%m-%dT%H:%M:%S%z")

# Filter orders based on time range
if start_time <= entered_time <= end_time:
    print("Order ID:", order["orderId"])
    print("Entered Time:", order["enteredTime"])
    # Add additional fields as needed

# Add more filtering conditions or processing logic as required
