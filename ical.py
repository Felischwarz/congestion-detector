import requests
from icalendar import Calendar
import recurring_ical_events

import dateutil.rrule
from datetime import datetime, timedelta, timezone
import pytz

import os

from config import KITA_OPENING_HOURS_APPOINTEMENT_NAME


def load_ical(ical_url, profile):
	data = requests.get(ical_url, allow_redirects=True)

	if not os.path.exists("ical_data"):
		os.makedirs("ical_data")

	open(f'ical_data/{profile}.ics', 'wb').write(data.content)
	ics = open(f'ical_data/{profile}.ics','rb')

	calendar = Calendar.from_ical(ics.read())
	return calendar

def is_kita_open(calendar):
	events = recurring_ical_events.of(calendar).between(datetime.today().date(), datetime.today().date() + timedelta(days=1))
	for event in events:
		if event["SUMMARY"].strip() == KITA_OPENING_HOURS_APPOINTEMENT_NAME:
			start_time = event["DTSTART"].dt
			duration = event["DTEND"].dt - event["DTSTART"].dt
			#print(f"Found event for today: {KITA_OPENING_HOURS_APPOINTEMENT_NAME} start {start_time} duration {duration}")

			current_time = datetime.now(tz=pytz.timezone('CET'))
			return current_time > start_time and current_time < start_time + duration

	return False


#returns None if Kita is closed
def get_time_left_until_kita_closes(calendar):
	if not is_kita_open(calendar):
		return None

	events = recurring_ical_events.of(calendar).between(datetime.today().date(), datetime.today().date() + timedelta(days=1))
	for event in events:
		if event["SUMMARY"].strip() == KITA_OPENING_HOURS_APPOINTEMENT_NAME:
			start_time = event["DTSTART"].dt
			duration = event["DTEND"].dt - event["DTSTART"].dt
			print(f"Found event for today: {KITA_OPENING_HOURS_APPOINTEMENT_NAME} start {start_time} duration {duration}")

			current_time = datetime.now(tz=pytz.timezone('CET'))
			time_left = event["DTEND"].dt - current_time
			#print(f"Kita still open for: {time_left}")
			return time_left

	return None

