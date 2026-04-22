import requests
import json
import global_var
import os

# here is where you log in

user_connected: str = "Guest"

def load_token() -> str:
    path = "auto_connect/token.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else: return {}

def update_token(token):
   with open("auto_connect/token.json", "w") as f:
        json.dump(token, f)

def login(username: str = None, password: str = None):
    global user_connected
    if user_connected != "Guest":
        print("you are already connected please logout")
        return
    while True:
        if not username:
            username = input("what is you username ?:\n(empty to get out)\n") # asking for username
        if username == "": return user_connected # verifying if user want to quit
        if requests.post(global_var.server_adress+'/username_exist', 
                         json={"username": username}).json(): # sending server username for check existence
            break
        else: 
            print("Your username does not exist please retry or register.")
            continue
    while True:
        if not password:
            password = input("What is your password ?:\n") # asking for password
        
        account_package = {"username": username, "password": password}
        if not requests.post(global_var.server_adress+"/password_check",
                            json=account_package).json(): # checking if username and password correspond
            print("This is not the right password please retry.")
            continue
        else:
            user_connected = username # setting the user
            print(f"Your are now logged in as {username}.")
            token = requests.post(global_var.server_adress+"/create_token", json=account_package).json() # creating token for 30 days
            update_token(token)
            print("token had been created you can now connect without auth within 30 days")
            break
        
def register():
    global user_connected
    while True:
        username = input("What will be your username ?:\n(empty to get out)\n") # asking username
        # verifying if username valid
        if len(username) < 3:
            print("Your username need to be at least 3 character long. Please retry")
            continue
        elif username.lower() == "guest":
            print("You are already Guest. Please retry")
        elif username == "": return

        if requests.post(global_var.server_adress+"/username_exist", json={"username": username}).json(): # sending data to server
            print("This username is already taken please try another one.")
        else: break
    while True:
        password = input("What will be your password ?:\n(exit to get out)\n") # asking user for password
        if password == 'exit': return
        if input("Please confirm your password:\n") != password: # password confirmation
            print("The password aren't the same please retry.")
            continue
        else:
            requests.post(global_var.server_adress+"/register_account", json={"username": username, "password": password}) # sending account to the server
            print(f"Your account had been register as {username}")
            login(username, password)
            break
        
def logout():
    global user_connected
    token = load_token()
    if user_connected != "Guest":
        print(f"You are connected as {user_connected} right now.")
    else: 
        print("You need to be connected to do that. Please retry once connected")
        return 
    disconnect = input("Are you sure to want to disconnect from your account ?:\n(yes or no)\n")
    if disconnect == "yes":
        print("You have successfully been disconnected.")
        requests.post(global_var.server_adress+"/del_token", json=token)
        update_token({})
        print("your token had been deleted")
        user_connected = "Guest"
        return
    return
    
def delete_account():
    global user_connected
    token = load_token()
    if user_connected != "Guest":
        print(f"You are connected as {user_connected} right now.")
    else: 
        print("You need to be connected to do that. Please retry once connected")
        return "Guest"
    password = input("Please enter your password:\n")
    if requests.post(global_var.server_adress+"/password_check", json={"username": user_connected, "password": password}):
        delete = input("Are you sure to want to delete from your account ?:\n(yes or no)\n")
        if delete == "yes": delete = input("Are you really sure of doing that? All your data will be lost and you will never be able to come back from this point:\n(yes or no)\n")
        if delete == "yes": 
            print(f"Say goodbye to {user_connected}")
            requests.post(global_var.server_adress+"/delete_account", json={"username": user_connected, "password": password})
            user_connected = "Guest"
            requests.post(global_var.server_adress+"/del_token", json=token)
            update_token({})
            print("your token had been deleted")
            return None
    return user_connected

def change_password():
    current_password = input("what is your current password?:\nif you don't remember please contact an admin(macto3001 on discord)")
    if not requests.post(global_var.server_adress+"/password_check",
                          json={"username": user_connected, "password": current_password}).json(): # checking if username and password correspond
        print("This is not the right password please retry.")
        return
    new_password = input("what will be your new password?:\n")

def auto_connect():
    global user_connected
    token = load_token()
    if not token:
        return None
    if token != {}:
        response = requests.post(global_var.server_adress+"/verify_token", json=token)
        if response.status_code == 200:
            user_connected = response.json()["username"]
            print(f"connected to {user_connected}")
        else:
            print("token is not valid please login yourself")
            login()
    
def connection():
    try:
        while True:
            print(f"Hey {user_connected}, welcome to the connection page.")
            choice = input("What do you want to do ?:\n"
                           "- login?('login')\n"
                           "- register('register')\n"
                           "- disconnect('disconnect')\n"
                           "- change password('password')\n"
                           "- delete account('delete')\n"
                           "- get out (nothing)\n")

            if choice == "register": register()
            elif choice == "login": login()
            elif choice == "disconnect": logout()
            elif choice == "delete": delete_account()
            elif choice == "": break
            else: print("Use one of the proposition over, please retry.")
            
            
                
        return user_connected
    except KeyboardInterrupt:
        print("login stopped")

    except UnicodeDecodeError as e:
        print(f"the input you just used wasn't formatted well please retry: '{e}'")

if __name__ == "__main__":
    connection()