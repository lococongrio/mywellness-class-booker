from datetime import datetime, timedelta
from config import load_config
import time
import sys
import pytz

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
filtered_events = [event for event in interesting_events
                   if not event.is_signed_up()
                   and not event.signup_closed()]

# Get just the closest bookable one
if filtered_events:
    bookable_events = [min(filtered_events, key=lambda event: event.startDate)]
else:
    bookable_events = []
    print("No bookable events found.")
print()
for event in bookable_events:
    print(f"Found bookable event: {event.to_string_with_status()}")
    print()

# Suspends the current thread until the supplied time,
def pause_until(pause_time):
    tz = pytz.timezone('Europe/Berlin')  # Replace with your timezone
    while datetime.now(tz) < pause_time:
        time.sleep(1)

# Suspend to book events if there are any to sign up for
if bookable_events:
    booking_time = bookable_events[0].bookingInfo.bookingOpensOn
    print(f"Booking time: {booking_time}")
    pause_time = booking_time - timedelta(seconds=5)
    print(f"Pausing until: {pause_time}")
    pause_until(pause_time)
    print(f"Current time: {datetime.now(tz)}")
    # Attempt to book the class
    print(f"Attempting to book {bookable_events[0].name}")
    # Trigger a short burst of bookings for eligible classes
    session.burst_booking(bookable_events)
else:
    print("No events to book")    
