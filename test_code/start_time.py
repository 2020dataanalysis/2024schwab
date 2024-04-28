import requests
from datetime import datetime, timedelta

# Calculate the start time (60 days before today)
start_time = datetime.now() - timedelta(days=60)

# Format the start time in ISO-8601 format
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

# Define the URL for your API endpoint
url = "https://your-api-endpoint.com/orders"

# Define the query parameters
params = {
    "fromEnteredTime": start_time_str,
    "toEnteredTime": "2024-04-27T23:59:59.999Z"  # Assuming today's date as end time
}

print(params)

# # Make the HTTP request
# response = requests.get(url, params=params)

# # Process the response
# if response.status_code == 200:
#     orders = response.json()
#     # Do something with the orders
# else:
#     print("Failed to fetch orders. Status code:", response.status_code)
