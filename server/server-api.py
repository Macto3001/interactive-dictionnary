import fastapi
from fastapi import Request
import pickle
import os

app = fastapi.FastAPI()
if os.path.exists('dico.pkl'):
	with open('dico.pkl', 'rb') as f:
	    dico = pickle.load(f)
	    print(dico) # not definitive just to see
else: dico: dict = {}

if os.path.exists('user_data.pkl'):
	with open('user_data.pkl', 'rb') as f:
		user_data = pickle.load(f)
		print(user_data) # also not definitive
else: user_data: dict = {}

def update(file: str, the_dico: dict):
	with open(file, 'wb') as f:
		pickle.dump(the_dico, f)
		print(f"'{file}' data had been updated")

@app.get("/dico_data")
def get_dico_data():
	return dico

@app.get("/user_data")
def get_user_data():
	return list(user_data.keys())
	
@app.post("/verify_research")
def verify_research(data: dict):
	print(f"received data: {data}")
	if data['research'] in dico:
		defintion = dico[data['research']]
	else: defintion = None
	return {"definition": defintion}

@app.post("/change_data")
def change_data(new_data: dict) -> None:
	print(f"new definition will be created :\"{new_data}\"")
	dico[list(new_data.keys())[0]] = list(new_data.values())[0]
	update("dico.pkl", dico)

@app.post("/get_info")
def get_info(defintion: dict) -> str:
	print(f"sended data of '{defintion["definition"]}' to client")
	return dico[defintion["definition"]]

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
	print(account_data)
	username = account_data["username"]
	if len(username) >= 3 and username.lower() != ("guest" or "exit") and username not in user_data:
		user_data[username] = account_data["password"]
		print(f"{request.client.host} has successfully register '{username}'")
	return f"this should not append aren't your a hacker '{request.client.host}'??"

@app.post("/delete_account")
def delete_account(account_data: dict, request: Request):
	username = account_data["username"]
	if username in user_data and user_data[username] == account_data["password"]:
		user_data.__delitem__(username)
		print(f"'{request.client.host}' has deleted the account '{username}'")
	return f"this should not append aren't your a hacker '{request.client.host}'??"