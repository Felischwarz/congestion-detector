import pickle


class User:
	def __init__(self, username, email_adress, route, calendar_url):
		self.username = username
		self.email_adress = email_adress
		self.route = route
		self.calendar_url = calendar_url

	def __repr__(self):
		return f"User: {self.username}, {self.email_adress}, {self.route}, {self.calendar_url}"


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
	route = input("Route: ").strip()
	calendar_url = input("Kalender url: ").strip()

	new_user = User(username, email_adress, route, calendar_url)
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

	cmds = [("a", "Benutzer anlegen", "register_user"), ("b", "Benutzer entfernen", "remove_user")]

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


	

if __name__ == "__main__":
	menu()
'''
TO_DO:
mehrere tokens gleichzeitig verwenden
zugriffe per mail anfragen?

billing account anfordern!
'''