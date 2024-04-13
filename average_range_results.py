import json

def calculate_average_range(file_path):
    # Initialize a dictionary to store the average range for each time period
    average_ranges = {}

    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        minute_data = json.load(file)

    # Iterate over each time period
    for time_period, time_data in minute_data.items():
        # Initialize variables to calculate sum and count of ranges for the current time period
        sum_range = 0
        count = 0

        # Iterate over the data for each day within the time period
        for day_data in time_data.values():
            # Add the range for the current day to the sum for the time period
            sum_range += day_data['range']
            count += 1

        # Calculate the average range for the current time period
        if count > 0:
            average_range = sum_range / count
        else:
            average_range = 0

        # Store the average range for the current time period
        average_ranges[time_period] = average_range

    return average_ranges

# Example usage
file_path = 'minute_data.json'  # Specify the file path here
average_ranges = calculate_average_range(file_path)
print("Average range for each time period:")
print(json.dumps(average_ranges, indent=4))
