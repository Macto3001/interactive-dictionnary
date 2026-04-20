import fastapi # type: ignore
from fastapi import Request # type: ignore
import pickle
import sys
import os
import uvicorn # type: ignore

ip_adresse = "127.0.0.1"
admin_list = ["admin", "macto3001"]

app = fastapi.FastAPI()
if os.path.exists('dico.pkl'):
	with open('dico.pkl', 'rb') as f:
	    dico = pickle.load(f)
else: dico: dict = {}

if os.path.exists('user_data.pkl'):
	with open('user_data.pkl', 'rb') as f:
		user_data = pickle.load(f)
else: user_data: dict = {}

# update dictionnary
def update(file: str, the_dico: dict):
	with open(file, 'wb') as f: # opening the file securly
		pickle.dump(the_dico, f) # ecrasing the new data
		print(f"'{file}' data had been updated")

# get data

@app.get("/get_dico")
def get_dico_data() -> dict:
	return dico

@app.get("/get_user")
def get_user_data():
	return list(user_data.keys())
	
# dico fonction

@app.post("/verify_research")
def verify_research(data: dict):
	print(f"received data: {data}")
	if data['research'] in dico:
		defintion = dico[data['research']]
	else: defintion = None
	return {"definition": defintion}

@app.post("/change_data")
def change_data(new_data: dict, request: Request) -> None:
	word = list(new_data.keys())[0]
	def_data = list(new_data.values())[0] # -> def real data
	definition = list(new_data.values())[0]["def"] # -> def string data

	if (len(word) > 30) or (len(definition) > 500): # if word or def too long
		print(f"{request.client.host} tried to send unvalid data")
		return

	print(f"new definition will be created by {request} :\"{new_data}\"")
	dico[word] = def_data # adding def
	update("dico.pkl", dico) # updating with the func

@app.post("/remove_data")
def remove_data(username: str, password: str, data_word: str = None, data_id: int = None) -> str:
	if username in admin_list and user_data[username] == password:
		dico.__delitem__(data_word if data_word else data_id)
		return f"{data_word if data_word else data_id} succesfully removed"
	return "something is wrong"

@app.post("/get_info")
def get_info(defintion: dict) -> dict:
	print(f"sended data of '{defintion["definition"]}' to client")
	return dico[defintion["definition"]] # returning data of only specif

# account fonction

@app.post("/username_exist")
def username_exist(username: dict, request: Request) -> bool:
	if username["username"] in user_data: 
		print(f"'{request.client.host}' tried to connect as '{username["username"]}', it already exist")
		return True
	print(f"'{request.client.host}' tried to connect as '{username["username"]}', that username don't already exist")
	return False

@app.post("/password_check")
def password_check(account_data: dict, request: Request) -> bool:
	if user_data[account_data["username"]] == account_data["password"]:
		print(f"'{request.client.host}' succesfully checked '{account_data["username"]}' password")
		return True
	print(f"'{request.client.host}' tried to connesousouct to '{account_data["username"]}' but failed because the password was wrong")
	return False

@app.post("/register_account")
def register_user_data(account_data: dict, request: Request):
	username = account_data["username"]
	if len(username) >= 3 and username.lower() != ("guest" or "exit") and username not in user_data:
		user_data[username.lower()] = account_data["password"]
		print(f"{request.client.host} has successfully register '{username}'")
		update("user_data.pkl", user_data)
	return f"this should not append aren't your a hacker '{request.client.host}'??"

@app.post("/delete_account")
def delete_account(account_data: dict, request: Request):
	username = account_data["username"]
	if username in user_data and user_data[username] == account_data["password"]:
		user_data.__delitem__(username)
		print(f"'{request.client.host}' has deleted the account '{username}'")
	return f"this should not append aren't your a hacker '{request.client.host}'??"

@app.post("/admin_account_del")
def admin_account_del(username: str, password: str, account_name: str) -> str:
	if username in admin_list and user_data[username] == password:
		user_data.__delitem__(account_name)
		return f"account {account_name} succesfully deleted"
	return "something went wrong"

# if file not imported
if __name__ == "__main__":
	print(dico)
	print(user_data)
	uvicorn.run("server-api:app", host=ip_adresse, port=8000)
