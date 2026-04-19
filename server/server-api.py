import fastapi
from fastapi import Request
from fastapi.templating import Jinja2Templates
import pickle
import os
import uvicorn

ip_address = "127.0.0.1"

app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")


if os.path.exists('dico.pkl'):
	with open('dico.pkl', 'rb') as f:
		dico: dict = pickle.load(f)
else: dico: dict = {}

if os.path.exists('user_data.pkl'):
	with open('user_data.pkl', 'rb') as f:
		user_data: dict = pickle.load(f)
else: user_data: dict = {}

def update(file: str, dictionnary: dict):
	with open(file, 'wb') as file: # opening the file securely
		pickle.dump(dictionnary, file) # override the new data
		print(f"'{file}' data had been updated")

@app.get("/")
def home(request: Request):
	return templates.TemplateResponse(request, "home.html", {"dico": dico})

@app.get("/get_dico")
def get_dico_data() -> dict:
	return dico

@app.get("/get_user")
def get_user_data():
	return list(user_data.keys())

@app.post("/verify_research")
def verify_research(data: dict):
	print(f"received data: {data}")
	if data['research'] in dico:
		definition = dico[data['research']]
	else: definition = None
	return {"definition": definition}

@app.post("/change_data")
def change_data(new_data: dict, request: Request) -> None:
	word = list(new_data.keys())[0]
	def_data = list(new_data.values())[0] # -> def real data
	definition = def_data["def"] # -> def string data
	if (len(word) > 30) or (len(definition) > 500): # if word or def too long
		print(f"{request.client} tried to send invalid data")
		return

	print(f"new definition will be created by {request} :\"{new_data}\"")
	dico[word] = def_data # adding def
	update("dico.pkl", dico) # updating with the func

@app.post("/get_info")
def get_info(definition: dict) -> dict:
	print(f"sent data of '{definition["definition"]}' to client")
	return dico[definition["definition"]] # returning data of only specif

@app.post("/username_exist")
def username_exist(username: dict, request: Request) -> bool:
	if username["username"] in user_data:
		print(f"'{request.client}' tried to connect as '{username["username"]}', it already exist")
		return True
	print(f"'{request.client}' tried to connect as '{username["username"]}', that username don't already exist")
	return False

@app.post("/password_check")
def password_check(account_data: dict, request: Request) -> bool:
	if user_data[account_data["username"]] == account_data["password"]:
		print(f"'{request.client}' successfully checked '{account_data["username"]}' password")
		return True
	print(f"'{request.client}' tried to connect to '{account_data["username"]}' but failed because the password was wrong")
	return False

@app.post("/register_account")
def register_user_data(account_data: dict, request: Request):
	username = account_data["username"]
	if len(username) >= 3 and username.lower() != ("guest" or "exit") and username not in user_data:
		user_data[username.lower()] = account_data["password"]
		print(f"{request.client} has successfully register '{username}'")
		update("user_data.pkl", user_data)
	return f"this should not append aren't your a hacker '{request.client}'??"

@app.post("/delete_account")
def delete_account(account_data: dict, request: Request):
	username = account_data["username"]
	if username in user_data and user_data[username] == account_data["password"]:
		user_data.__delitem__(username)
		print(f"'{request.client}' has deleted the account '{username}'")
	return f"this should not append aren't your a hacker '{request.client}'??"


if __name__ == "__main__":
	print(dico)
	print(user_data)
	uvicorn.run("server-api:app", host=ip_address, port=8000)
