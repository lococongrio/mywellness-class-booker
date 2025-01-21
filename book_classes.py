from datetime import datetime, timedelta
from config import load_config
import time

config = load_config()

# Establish a session
credentials = config.load_credentials()
if credentials is None:
    print("Failed to obtain MyWellness credentials. Terminating")
    quit(1)
session = credentials.login()
print(f"Established a session with user id: {session.user_id}")


# Look at the whole next week for classes of interest
now = datetime.now(tz=config.load_timezone())
today = now.strftime('%Y-%m-%d')
in_a_week = (now + timedelta(days=7)).strftime('%Y-%m-%d')


# Setup the matcher to establish whether a class is of interest
classEventMatcher = config.create_matcher()


# Query for the interesting events the upcoming week
interesting_events = [event for event in session.search_events(config.facilityId, today, in_a_week) if event.bookingInfo.bookingAvailable and classEventMatcher.matches(event)]
for event in interesting_events:
    print(f"Found event matching interests: {event.to_string_with_status()}")


# Filter down to those that we can book
bookeable_events = [event for event in interesting_events if not event.is_signed_up() and not event.signup_closed() and event.booking_opens_in()]


def pause_until(hour, minute, second):
    print(f"Current time: {now}")
    next_run = now.replace(hour=hour, minute=minute, second=second)
    sleep_duration = (next_run - now).total_seconds()
    if (sleep_duration > config.maxSuspendSeconds):
        print(f"Still {sleep_duration} seconds until the next booking run ({next_run}), exceeding the maxSuspendSeconds ({config.maxSuspendSeconds}) limit. Terminating")
        quit()
    if (sleep_duration > 0):
        print(f"Pausing for {sleep_duration} seconds until {next_run}")
        time.sleep(sleep_duration)

# Pause until 5 seconds before opening time
pause_until(19, 59, 55)


# Trigger a short burst of bookings for eligible classes
session.burst_booking(bookeable_events)
