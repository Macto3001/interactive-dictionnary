import requests
import json
import time
from datetime import datetime
import login
import global_var

server_adress = global_var.server_adress

def dictionary():
	while True:
		try:
			research: str = input("What's definition do you want to find ?(let empty to go back)\n: ") # input the word to research 
			if research == "": break
			elif len(research) > 30: # if definition too long
				print("This is too long please retry.")
				continue
			definition_response: str = requests.post(server_adress+"/verify_research", json={'research': research}) # research the word on the server
			if definition_response.status_code == 200: # if definition already exist
				definition = definition_response.json()["definition"]
				while True:
					print(f'The definition of "{research}" is "{definition['def']}"')
					choice: str = input("what do you want to do?:\n" # choice of possible action
									"\n modify the definition ? 'edit'"
									"\n get information 'info'"
									"\n quit to research other def (nothing)"
									"\n: ")
					if choice == "edit":
						if login.user_connected == "Guest": # if user not connected
							print("You need to be connected to modify definition")
							continue
						elif input(f"do you want to modify this definition as {login.user_connected}?\n:") == "yes": # asking the user if he want to show who he is
							new_def = input("What will be the new definition?\n: ")
							if len(new_def) > 500:
								print("This is too long the limit is 500 char please retry.")
								continue
							data: dict = {"def": new_def, "time": time.time(), "user": login.user_connected} # creating data dict
							# sending the definition to the server
							response = requests.post(server_adress+"/change_data",json={
								"word": research,
								"definition": data,
								"token": login.load_token()})
							if response.status_code == 200:
								print("Definition added succesfully")
							else: print("Something went wrong while adding the definition sorry.")

							definition = requests.post(server_adress+"/verify_research", json={'research': research}).json()["definition"] # update the definition data
							continue
					elif choice == "info":
						info = requests.post(server_adress+"/get_info", json={"definition": research}).json() # getting server info
						def_length = len(info["def"])
						date = datetime.fromtimestamp(info["time"])
						try: user = info["user"]
						except KeyError: user = "Guest"
						print(f"there is {def_length} caractere in this definition.\n"
			 				f"It had been wrote the {date.strftime("%d/%m/%Y")} at {date.strftime("%H:%M:%S")}(UTC+1 CET) by user: {user}.")
						continue
					elif choice == "":
						break
					else :
						print("you must respond with a proper anwser")
						continue
			else: # if definition do not exist
				print(f"'{research}' have no definition yet")
				if login.user_connected == "Guest":
					print("Connect yourself to create one.")
					continue

				do_new_def = input(f"Do you want to create one as {login.user_connected} ?:\n")
				if do_new_def == "yes": # ask to create a new definition
					new_def = input("what will be the new definition?:\n")
					if len(new_def) > 500:
						print("It's too long the limit is 500 char for now please retry.")
						continue
					 # sending new defintion data to the server
					response = requests.post(server_adress+"/change_data",json={
						"word": research,
						"definition": {"def": new_def, "time": time.time(), "user": login.user_connected}, 
						"token": login.load_token()})
					if response.status_code == 200:
						print("Definition added succesfully")
					else: print("Something went wrong while adding the definition sorry.")
		
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