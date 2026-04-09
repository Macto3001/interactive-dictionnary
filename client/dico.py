import requests
import json
import time
from datetime import datetime

server_adress = "http://127.0.0.1:8000"

def dictionary():
	while True:
		try:
			research: str = input("What's definition do you want to find ?(let empty to go back)\n: ") # input the word to research 
			if research == "": break
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
		                # if login.user_connected == "Guest":
		                #     print("Vous devez être connecter pour modifier une définition. Veuillez réessayer une fois connecter")
		                #     continue
		                # elif input(f"voulez vous modfier cette definition en tant que {login.user_connected} ? \n:") == "oui":
						data: dict = {"def": input("What will be the new definition?\n: "), "time": time.time(), "user": "Guest"} # creating data dict
						requests.post(server_adress+"/change_data", json={research: data}) # changing the definition on the server side
						definition = requests.post(server_adress+"/verify_research", json={'research': research}).json()["definition"] # update the definition data
						continue
					elif choice == "info":
						info = requests.post(server_adress+"/get_info", json={"definition": research}).json() # récupération des info du serveur
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