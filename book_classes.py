from datetime import datetime, timedelta
from config import load_config
from credentials import load_credentials
import time

config = load_config()
classEventMatcher = config.create_matcher()

credentials = load_credentials()
if credentials is None:
    print("Failed to obtain MyWellness credentials. Terminating")
    quit(1)

session = credentials.login()
now = datetime.now()
today = now.strftime('%Y-%m-%d')
in_a_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
events = [event for event in session.search_events(config.facilityId, today, in_a_week) if event.bookingInfo.bookingAvailable and classEventMatcher.matches(event)]

for event in events:
    print(f"Found event matching interests: {event.to_string_with_status()}")

events = [event for event in events if not event.is_signed_up() and not event.signup_closed() and event.booking_opens_in()]

def pause_until(hour, minute, second):
    next_run = now.replace(hour=hour, minute=minute, second=second)
    sleep_duration = (next_run - now).total_seconds()
    if (sleep_duration > 100):
        print(f"Still {sleep_duration} seconds until the next booking run ({next_run}), exceeding the 100 second limit. Terminating")
        quit()
    if (sleep_duration > 0):
        print(f"Pausing for {sleep_duration} seconds until {next_run}")
        time.sleep(sleep_duration)

pause_until(19, 59, 55)

session.burst_booking(events)
