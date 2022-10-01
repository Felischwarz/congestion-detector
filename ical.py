import requests
from icalendar import Calendar
import recurring_ical_events

import dateutil.rrule
from datetime import datetime, timedelta, timezone
import pytz

ical_url = "https://calendar.google.com/calendar/ical/cfbfbddb%40gmail.com/private-5695e575d0fb4d180171719c0dfb7174/basic.ics"

#Event name in google calendar has to match exactly to this string
kita_opening_hours_appointement_name = "Kita Öffnungszeiten"

def load_ical(ical_url):
	data = requests.get(ical_url, allow_redirects=True)
	open('cal.ics', 'wb').write(data.content)

	ics = open('cal.ics','rb')

	calendar = Calendar.from_ical(ics.read())
	return calendar

def is_kita_open(calendar):
	events = recurring_ical_events.of(calendar).between(datetime.today().date(), datetime.today().date() + timedelta(days=1))
	print("Listing events for today...")
	for event in events:
		if event["SUMMARY"].strip() == kita_opening_hours_appointement_name:
			start_time = event["DTSTART"].dt
			duration = event["DTEND"].dt - event["DTSTART"].dt
			print(f"Found event for today: {kita_opening_hours_appointement_name} start {start_time} duration {duration}")

			current_time = datetime.now(tz=pytz.timezone('CET'))
			return current_time > start_time and current_time < start_time + duration

	return False


#returns None is Kita is closed
def get_time_left_until_kita_closes(calendar):
	if not is_kita_open(cal):
		return None

	events = recurring_ical_events.of(calendar).between(datetime.today().date(), datetime.today().date() + timedelta(days=1))
	print("Listing events for today...")
	for event in events:
		if event["SUMMARY"].strip() == kita_opening_hours_appointement_name:
			start_time = event["DTSTART"].dt
			duration = event["DTEND"].dt - event["DTSTART"].dt
			print(f"Found event for today: {kita_opening_hours_appointement_name} start {start_time} duration {duration}")

			current_time = datetime.now(tz=pytz.timezone('CET'))
			time_left = event["DTEND"].dt - current_time
			print(f"Kita still open for: {time_left}")
			return time_left

	return None
