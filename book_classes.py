from datetime import datetime, timedelta
from config import load_config
from credentials import load_credentials

config = load_config()
classEventMatcher = config.create_matcher()

credentials = load_credentials()
if credentials is None:
    print("Failed to obtain MyWellness credentials. Terminating")
    quit(1)

session = credentials.login()
today = datetime.now().strftime('%Y-%m-%d')
in_a_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
events = [event for event in session.search_events(config.facilityId, today, in_a_week) if event.bookingInfo.bookingAvailable and classEventMatcher.matches(event)]

for event in events:
    print(f"Found event matching interests: {event.to_string_with_status()}")

events = [event for event in events if not event.is_signed_up() and not event.signup_closed() and event.booking_opens_in()]
session.burst_booking(events)
