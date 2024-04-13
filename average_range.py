#   Version - List

import json
from collections import defaultdict

def save_minute_data_to_file(minute_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(minute_data, file, indent=4)

def get_average_range_for_minutes(file_path, num_days, output_file, target_times):
    # Initialize variables to store data
    minute_data = defaultdict(dict)
    day_counts = defaultdict(int)
    
    # Read JSON data from file
    with open(file_path, 'r') as file:
        for line in file:
            # Parse JSON from each line
            try:
                json_data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue
            
            # Check if JSON data contains "candles" key
            if "candles" not in json_data:
                print("JSON data does not contain 'candles' key.")
                continue
            
            # Iterate over the candles array
            for candle in json_data["candles"]:
                # Calculate the range for the candle
                range_value = candle["high"] - candle["low"]
                # Check if the time is in the target times
                if candle["human_readable_time"] in target_times:
                    # print(candle)
                    # Ensure we collect data for the specified number of days
                    if day_counts[candle["human_readable_time"]] < num_days:
                        # Only select one data point for each day
                        if candle["human_readable_date"] not in minute_data[candle["human_readable_time"]]:
                            # Add the range value and candle data to the corresponding minute
                            minute_time = candle["human_readable_time"]
                            minute_data[minute_time][candle["human_readable_date"]] = {"range": range_value, "candle_data": candle}
                            # Increment day count for the minute
                            day_counts[minute_time] += 1
                        else:
                            # Update the range value if the data point already exists for the day
                            minute_data[minute_time][candle["human_readable_date"]]["range"] += range_value
    
    # Save the minute data to a file
    save_minute_data_to_file(minute_data, output_file)
    print(f"Minute data saved to {output_file}")

# Example usage
file_path = 'price_history.json'  # Specify your file path here
output_file = 'minute_data.json'   # Specify the output file path here
num_days = 10
# target_times = ["06:30:00", "06:31:00", "06:32:00"]  # Specify the target times here
# # Set the number of target times
# num_target_times = 60

# # Initialize an empty list to store the target times
# target_times = []

# # Iterate over the range to generate the target times
# for i in range(num_target_times):
#     # Construct the time string based on the index
#     time = f"06:3{i}:00" if i < 2 else f"06:3{i}:00" # Ensure leading zeros for minutes
#     # Append the time to the target_times list
#     target_times.append(time)

# # Print the generated target_times list
# print(target_times)






# # Initialize an empty list to store the target times
# target_times = []

# # Set the initial time
# time = "06:30:00"

# # Append the initial time to the target_times list
# target_times.append(time)

# # Loop to generate the target times
# for _ in range(60):
#     # Extract hours, minutes, and seconds
#     hours, minutes, seconds = map(int, time.split(':'))
    
#     # Increment the minute
#     minutes += 1
    
#     # Check if minutes exceed 59
#     if minutes > 59:
#         break
    
#     # Convert back to string format
#     time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
#     # Append the time to the target_times list
#     target_times.append(time)

# # Print the target_times list
# print(target_times)












# Initialize an empty list to store the target times
target_times = []

# Set the initial time (e.g., "06:30:00")
initial_time = "06:30:00"

# Append the initial time to the target_times list
target_times.append(initial_time)

# Extract hours and minutes from the initial time
hours, minutes, _ = map(int, initial_time.split(':'))

# Calculate the end time (one hour later)
end_hour = hours + 1
end_time = f"{end_hour:02d}:{minutes:02d}:00"

# Loop to generate the target times
current_time = initial_time
while current_time != end_time:
    # Extract hours, minutes, and seconds
    hours, minutes, seconds = map(int, current_time.split(':'))
    
    # Increment the minute
    minutes += 1
    
    # Check if minutes exceed 59
    if minutes > 59:
        # Reset minutes and increment hours
        minutes = 0
        hours += 1
    
    # Check if hours exceed 23
    if hours > 23:
        break
    
    # Convert back to string format
    current_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Append the current time to the target_times list
    target_times.append(current_time)

# Print the target_times list
print(target_times)





get_average_range_for_minutes(file_path, num_days, output_file, target_times)
