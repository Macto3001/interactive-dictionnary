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

def update_dico():
	with open('dico.pkl', 'wb') as f:
		pickle.dump(dico, f)
		print("data had been updated")

@app.get("/data")
def get_data():
	with open("dico.pkl", "rb") as file:
		return pickle.load(file)

@app.post("/verify_research")
def verify_research(data: dict):
	print(f"received data: {data}")
	if data['research'] in dico:
		defintion = dico[data['research']]
	else: defintion = None
	return {"definition": defintion}

@app.post("/change_data")
def change_data(new_data: dict):
	print(f"new definition will be created :\"{new_data}\"")
	dico[list(new_data.keys())[0]] = list(new_data.values())[0]
	update_dico()

@app.post("/get_info")
def get_info(defintion: dict):
	print(f"sended data of {defintion["definition"]} to client")
	return dico[defintion["definition"]]

@app.post("/username_exist")
def username_exist(username: dict, request: Request):
	if username["username"] in user_data: 
		print(f"{request.client.host} tries to connect as {username["username"]}")
		return True
	print(f"{request.client.host} tried to connect as {username["username"]} but that username don't exist")
	return False

@app.post("/password_check")
def password_check(account_data: dict, request: Request):
	if user_data[account_data["username"]] == account_data["password"]:
		print(f"{request.client.host} succesfully connected to {account_data["username"]}")
		return True
	print(f"{request.client.host} tried to connect to {account_data["username"]} but failed because the password was wrong")
