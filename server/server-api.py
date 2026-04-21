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
def change_data(package: dict, request: Request) -> None:
	password_check(package["account_data"], request) # verify the password for security

	word = package["word"]
	def_data = package["definition"] # -> def real data

	if (len(word) > 30) or (len(def_data["def"]) > 500): # if word or def too long
		print(f"{request.client.host} tried to send unvalid data")
		return

	print(f"new definition will be created by {request.client.host} :\"{word}: {def_data}\"")
	dico[word] = def_data # adding def
	update("dico.pkl", dico) # updating with the func

@app.post("/remove_data")
def remove_data(username: str, password: str, request: Request, data_word: str = None, data_id: int = None) -> str:
	if not data_word and not data_id:
		return "there is nothing to delete"
	
	if username in admin_list and password_check({"username": username, "password": password}, request):
		dico.__delitem__(data_word if data_word else data_id)
		return f"'{request.client.host}' as uccesfully removed {data_word if data_word else data_id}"
	
	return f"'{request.client.host}' tried removing {data_word} but something went wrong"

@app.post("/get_info")
def get_info(defintion: dict, request: Request) -> dict:
	print(f"sended data of '{defintion["definition"]}' to {request.client.host}")
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
	if  not account_data["username"] in user_data:
		return False
	if user_data[account_data["username"]] == account_data["password"]:
		print(f"'{request.client.host}' succesfully checked '{account_data["username"]}' password")
		return True
	print(f"'{request.client.host}' tried to connes to '{account_data["username"]}' but failed because the password was wrong")
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
	if username in user_data and password_check(account_data, request):
		user_data.__delitem__(username)
		print(f"'{request.client.host}' has deleted the account '{username}'")
	return f"this should not append aren't your a hacker '{request.client.host}'??"

@app.post("/admin_account_del")
def admin_account_del(username: str, password: str, account_name: str, request: Request) -> str:
	if username in admin_list and password_check({"username": username, "password": password}, request):
		user_data.__delitem__(account_name)
		return f"{request.client.host} as succesfully deleted account {account_name}"
	return f"'{request.client.host}' tried deleting {account_name} but something went wrong"

# if file not imported
if __name__ == "__main__":
	print(dico)
	print(user_data)
	uvicorn.run("server-api:app", host=ip_adresse, port=8000)