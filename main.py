import pickle
import time
from datetime import datetime

from ical import load_ical, is_kita_open, get_time_left_until_kita_closes
from gmaps import check_for_congestion
from email_service import send_email
from config import *


class User:
	def __init__(self, username, email_adress, route_start, route_end, calendar_url):
		self.username = username
		self.email_adress = email_adress
		self.route_start = route_start
		self.route_end = route_end
		self.calendar_url = calendar_url

	def __repr__(self):
		return f"User: {self.username}, {self.email_adress}, {self.route_start}, {self.route_end}, {self.calendar_url}"


def load():
	with open("Userdata.p", "rb") as f:
		users = pickle.load(f)
		return users

def save(users):
	with open("Userdata.p", "wb") as f:
		pickle.dump(users, f)

def register_user():
	username = input("Benutzername: ").strip()
	email_adress = input("E-Mail_Adresse: ").strip()
	route_start = input("Route (Start): ").strip()
	route_end = input("Route (Ende): ").strip()
	calendar_url = input("Kalender url: ").strip()

	new_user = User(username, email_adress, route_start, route_end, calendar_url)
	print(f"Folgender Benutzer wurde erfolgreich erstellt: ")
	print(new_user)

	users = load()
	users.append(new_user)
	save(users)

def remove_user():
	username = input("Benutzername des zu entfernenden Benutzers: ").strip()
	users = load()
	for user in users: 
		if user.username == username:
			users.remove(user)
			print(f'Der Benutzer mit dem Benutzernamen "{username}" wurde erfolgreich entfernt.')

	save(users)

def menu():
	print("Anwendung wurde gestartet.")

	cmds = [("a", "Benutzer anlegen", "register_user"), ("b", "Benutzer entfernen", "remove_user"), ("c", "Scan starten", "scan")]

	while True:
		users = load()
		if not users: 
			print("Es existieren keine Benutzer.")

		else: 
			print("Registrierte Benutzer:")
			for user in users: 
				print(user)

		print("-"*20)
		print("Befehle:")
		for cmd in cmds:
			print(f"({cmd[0]}) {cmd[1]}")
		selection = input("---")

		found_cmd = False
		for cmd in cmds:
			if selection.strip() == cmd[0]:
				globals()[cmd[2]]()
				found_cmd = True
				break 

		if not found_cmd:
			print ("ungültiger Befehl!")


def scan():
	while True: 
		print("Scannen...")
		users = load()
		for user in users: 
			cal = load_ical(user.calendar_url, user.username)

			print(f"{datetime.now()} Für Nutzer {user.username}:")
			if is_kita_open(cal):
				time_left = get_time_left_until_kita_closes(cal)
				print(f"Kita ist noch {time_left} geöffnet")

				res = check_for_congestion(user.route_start, user.route_end)

				dur_in_traffic = res[1]

				if res: 
					if True: #res[0]: #if there is congestion
						#structure: (True, dur_in_traffic, dur, obj["routes"][0]["legs"][0]["start_address"], obj["routes"][0]["legs"][0]["end_address"])
						if dur_in_traffic > time_left.total_seconds():

							message = f"""Auf der Strecke von {res[3]} nach {res[4]} kommt es aufgrund der Verkehrslage zu Verspätungen.
							Die Dauer beträgt ca. {str(int(dur_in_traffic / 60))} Minuten (statt {str(int(res[2] / 60))}). 
							"""

							print(message)
							print("E-Mail wird gesendet...")
							send_email(user.email_adress, message)

							time.sleep(6*60*60) #heute keine Abfragen mehr notwendig

						else:
							print(f"Überprüfung der Verkehrslage: Verspätungen!. Geschätze Fahrzeit: {str(int(dur_in_traffic / 60))} (statt {str(int(res[2] / 60))}).")

					else:
						print(f"Überprüfung der Verkehrslage: keine Verspätungen. Geschätze Fahrzeit: {str(int(dur_in_traffic / 60))} Minuten")

				else: 
					print("Error in check_for_congestion()")

			else:
				print("Kita ist geschlossen")

		time.sleep(SCAN_FREQUENCY)


if __name__ == "__main__":
	menu()