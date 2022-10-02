import googlemaps
from datetime import datetime
from config import *

import requests
import urllib.parse
import json


#will return None (Error) or Tuple with results
def check_for_congestion(origin, destination, departure_time="now"):
	origin = urllib.parse.quote(str(origin))
	destination = urllib.parse.quote(str(destination))

	url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&departure_time={str(departure_time)}&key={API_KEY}"

	payload={}
	headers = {}

	response = requests.request("GET", url, headers=headers, data=payload)

	if not response.ok: 
		print(f"Error: Google Maps API Request failed ({response.error})")
		return


	obj = json.loads(response.text)

	try: 
	   obj["routes"][0]["legs"][0]["duration"]["value"]
	   obj["routes"][0]["legs"][0]["duration_in_traffic"]["value"]
	   obj["routes"][0]["legs"][0]["start_address"]
	   obj["routes"][0]["legs"][0]["end_address"]

	except:
	   print("Error: Google Maps Response has unexpected format")
	   return 


	dur = obj["routes"][0]["legs"][0]["duration"]["value"]
	dur_in_traffic = obj["routes"][0]["legs"][0]["duration_in_traffic"]["value"]

	if dur_in_traffic > dur + ALERT_TIME_LIMIT:
	   return (True, dur_in_traffic, dur, obj["routes"][0]["legs"][0]["start_address"], obj["routes"][0]["legs"][0]["end_address"])
	else:
	   return (False, dur_in_traffic, dur, obj["routes"][0]["legs"][0]["start_address"], obj["routes"][0]["legs"][0]["end_address"])


