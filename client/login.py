import requests
import json
import dico

# here is where you log in


user_connected = "Guest"
user_data = {"admin": "123456e*"}

def login():
    global user_connected
    while True:
        username = input("what is you username ?:\n(exit to get out)\n")
        if username == "exit": return user_connected
        if i := requests.post(dico.server_adress+'/username_exist', json={"username": username}).json():
            print(i)
            break
        else: 
            print(i)
            print("Your username does not exist please retry or register.")
            continue
    while True:
        password = input("What is your password ?:\n")
        if not requests.post(dico.server_adress+"/password_check", json={"username": username, "password": password}).json():
            print("This is not the right password please retry.")
            continue
        else:
            user_connected = username
            print(f"Your are now logged in as {username}.")
            break
        
def register():
    global user_connected
    while True:
        username = input("What will be your username ?:\n(exit to get out)\n")
        if len(username) < 3:
            print("Your username need to be at least 3 character long. Please retry")
            continue
        elif username.lower() == "guest":
            print("You are already Guest. Please retry")
        elif username == "exit": return
        lower_usernames_data = [i.lower() for i in user_data]
        if username.lower() in lower_usernames_data:
            print("This username is already taken please try another one.")
        else: break
    while True:
        password = input("What will be your password ?:\n(exit to get out)\n")
        if password == 'exit': return
        if input("Please confirm your password:\n") != password:
            print("The password aren't the same please retry.")
            continue
        else:
            # user_data[username] = password
            print(f"Your account had been register as {username}, you can now connect yourself to it.")
            break
        
def logout():
    global user_connected
    if user_connected != "Guest":
        print(f"You are connected as {user_connected} right now.")
    else: 
        print("You need to be connected to do that. Please retry once connected")
        return 
    disconnect = input("Are you sure to want to disconnect from your account ?:\n(yes or no)\n")
    if disconnect == "yes":
        print("You have successfully been disconnected.")
        user_connected = "Guest"
        return
    return
    
def delete_account():
    global user_connected
    if user_connected != "Guest":
        print(f"You are connected as {user_connected} right now.")
    else: 
        print("You need to be connected to do that. Please retry once connected")
        return "Guest"
    password = input("Please enter your password:\n")
    if password == user_data[user_connected]:
        delete = input("Are you sure to want to delete from your account ?:\n(yes or no)\n")
        if delete == "yes": delete = input("Are you really sure of doing that? All your data will be lost and you will never be able to come back from this point:\n(yes or no)\n")
        if delete == "yes": 
            print(f"Say goodbye to {user_connected}")
            user_data.__delitem__(user_connected)
            user_connected = "Guest"
            return None
    return user_connected
def connection():
    try:
        while True:
            print(f"Hey {user_connected}, welcome to the connection page.")
            choice = input("What do you want to do ?:\n"
                           "- login?('login')\n"
                           "- register('register')\n"
                           "- disconnect('disconnect')\n"
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

if __name__ == "__main__":
    connection()