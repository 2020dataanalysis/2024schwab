from datetime import datetime, timedelta, timezone

# Define the Pacific Time Zone (PT) offset from UTC (California is typically 7 hours behind UTC)
pt_offset = -7  # Pacific Daylight Time (PDT) offset from UTC

# Get current UTC time
current_utc_time = datetime.utcnow()

# Calculate the offset for Pacific Time Zone (PT)
pt_time = current_utc_time + timedelta(hours=pt_offset)

# Format the current time as a string in the required format
to_time_str = pt_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


days = 1
# Calculate the start time (60 days before today)
start_time = datetime.now() - timedelta(days=days)

# Format the start time in ISO-8601 format
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')








# Update the params dictionary
params = {
    "fromEnteredTime": start_time_str,
    "toEnteredTime": to_time_str
}

print(params)