import requests
import json
import time
from datetime import datetime
import login

print(login.user_connected)
server_adress = "http://127.0.0.1:8000"

def dictionary():
	while True:
		try:
			research: str = input("What's definition do you want to find ?(let empty to go back)\n: ") # input the word to research 
			if research == "": break
			elif len(research) > 30: # if definition too long
				print("This is too long please retry.")
				continue
			definition: str = requests.post(server_adress+"/verify_research", json={'research': research}).json()["definition"] # research the word on the server
			if definition: # if definition already exist
				while True:
					print(f'The definition of "{research}" is "{definition['def']}"')
					choice: str = input("what do you want to do?:\n" # choice of possible action
									"\n modify the definition ? 'edit'"
									"\n get information 'info'"
									"\n quit to research other def (nothing)"
									"\n: ")
					if choice == "edit":
						if login.user_connected == "Guest": # if user not connected
							print("Vous devez être connecter pour modifier une définition. Veuillez réessayer une fois connecter")
							continue
						elif input(f"voulez vous modfier cette definition en tant que {login.user_connected} ? \n:") == "oui": # asking the user if he want to show who he is
							new_def = input("What will be the new definition?\n: ")
							if len(new_def) > 500:
								print("This is too long the limit is 500 char please retry.")
								continue
							data: dict = {"def": new_def, "time": time.time(), "user": login.user_connected} # creating data dict
							requests.post(server_adress+"/change_data", json={research: data}) # changing the definition on the server side
							definition = requests.post(server_adress+"/verify_research", json={'research': research}).json()["definition"] # update the definition data
							continue
					elif choice == "info":
						info = requests.post(server_adress+"/get_info", json={"definition": research}).json() # getting server info
						def_length = len(info["def"])
						date = datetime.fromtimestamp(info["time"])
						try: user = info["user"]
						except KeyError: user = "Guest"
						print(f"there is {def_length} caractere in this definition, it had been wrote the {date.strftime("%d/%m/%Y")} at {date.strftime("%H:%M:%S")}(UTC+1 CET) by {user}.")
						continue
					elif choice == "":
						break
					else :
						print("you must respond with a proper anwser")
						continue
			else: # if definition do not exist
				print(f"{research} have no definition yet")
				do_new_def = input("do you want to create one ?:\n")
				if do_new_def == "yes": # ask to create a new definition
					new_def = input("what will be the new definition?:\n")
					if len(new_def) > 500:
						print("it's too long the limit is 500 char for now please retry.")
						continue
					requests.post(server_adress+"/change_data", json={research: {"def": new_def, "time": time.time(), "user": "Guest"}}) # sending new defintion data to the server
		except KeyboardInterrupt: # if ctrl+c is pressed
			break
		except requests.exceptions.ConnectionError: # if server not found
			print("The server seems to have issues or being offline. Please contact an admin or retry later.")
		except requests.exceptions.Timeout: # if client cannot search
			print("Connection timed out. Please check your internet connection or retry later.")
		except requests.exceptions.RequestException as error: # every other server error
			print(f"The request went wrong: {error}")
if __name__ == "__main__":
	dictionary()