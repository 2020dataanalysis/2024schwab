# from datetime import datetime

# # Parse the string into a datetime object
# dt = datetime.fromisoformat("2024-04-28T23:19:08+0000")

# # Print the datetime object
# print(dt)



from datetime import datetime

# Define the format of the input string
date_format = "%Y-%m-%dT%H:%M:%S%z"

# Parse the string into a datetime object
dt = datetime.strptime("2024-04-28T23:19:08+0000", date_format)

# Print the datetime object
print(dt)
