from datetime import datetime, timedelta, timezone

minutes = 30
# start_time = datetime.now() - timedelta(minutes=minutes)


pt_offset = -7  # Pacific Daylight Time (PDT) offset from UTC

# Get current UTC time
# current_utc_time = datetime.utcnow()
now = datetime.now()
now_utc = datetime.now(timezone.utc)

# start_time = datetime.now()
# print(start_time)
print(now)
# print(now_utc)
