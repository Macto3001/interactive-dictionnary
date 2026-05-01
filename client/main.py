import dico
import login
import global_var
import requests

class Main:
    def __init__(self):
        pass
    
    def panel(self):
        # here is the panel where the user come first
        try:
            login.auto_connect()
            while True:
                requests.get(global_var.server_adress) # connection test to the server
                choice = input("Welcome to the interactive-Dictionnary\n"
                               "What do you want to do?:\n"
                               "- search word 'search'\n"
                               "- account managment 'account'\n"
                               "- stop the script (nothing)\n"
                               ": ")
                if choice == "search": dico.dictionary()
                elif choice == "account": login.connection()
                elif choice == "": break
                elif choice == "admin" and requests.post(global_var.server_adress+"/is_admin", json=login.load_token()).json(): self.admin_panel()
                else: print("This option do not exist.")

        # exeption catch
        except KeyboardInterrupt: print("\nprogram ended") # if ctrl + C
        except EOFError: print("\nprogram stopped") # if ctrl + D
        except requests.exceptions.ConnectionError: # if server not found 
            print("The server seems to have issues or being offline. Please contact an admin or retry later.")
            
        except requests.exceptions.Timeout: # if client cannot connect
            print("Connection timed out. Please check your internet connection or retry later.")

        except requests.exceptions.RequestException as error: # every other server error
            print(f"The request went wrong: {error}")

        # except Exception as e: print(f"\nSomething went wrong but i don't why. Error:\n{e}")

    def admin_panel(self):
        while True:
            admin_choice = input("Welcome to the admin panel\n"
            "What do you want to do?\n"
            "- see data list 'data_list'\n"
            "- see user list 'user_list'\n"
            "- see admin list 'admin_list'\n"
            "- add new admin 'new_admin'\n"
            "- delete admin 'del_admin'\n"
            "- delete def 'del_def'\n"
            "- delete user 'del_user'\n"
            "- exit (nothing)\n"
            ": ")
            if admin_choice == "data_list": print(f"dico data:\n{requests.get(global_var.server_adress+"/get_dico").json()}")
            elif admin_choice == "user_list": print(f"user data:\n{requests.get(global_var.server_adress+"/get_user").json()}")
            elif admin_choice == "admin_list": print(f"admin list:\n{requests.get(global_var.server_adress+"/get_admin", params={
                "username": login.user_connected,
                "password": input("please enter your password\n: "),
                }).json()}")

            elif admin_choice == "new_admin":
                admin_name = input("who will that be?\n: ")
                password = input("please enter your password\n: ")
                response = requests.post(global_var.server_adress+"/new_admin", params={
                    "username": login.user_connected,
                    "password": password,
                    "account_name": admin_name,
                })

                if response.status_code == 200: print(f"admin {admin_name} succesfully added")
                elif response.status_code == 401: print(f"password was wrong please retry")
                else: print("something went wrong, please retry")
                
            elif admin_choice == "del_admin":
                admin_name = input("who will that be?\n: ")
                password = input("please enter your password\n: ")
                response = requests.post(global_var.server_adress+"/del_admin", params={
                    "username": login.user_connected,
                    "password": password,
                    "admin_name": admin_name,
                })
                
                if response.status_code == 200: print(f"admin {admin_name} succesfully removed")
                elif response.status_code == 401: print(f"password was wrong please retry")
                else: print("something went wrong, please retry")

            elif admin_choice == "del_def": 
                deletion = input("what do you want to delete?\n: ")
                if not requests.post(global_var.server_adress+"/verify_research", json={"research": deletion}).json()["definition"]:
                    print(f"'{deletion}' does not exist")
                    continue
                if input(f"are you sure to delete '{deletion}'?\n: ") == "yes":
                    password = input("please enter your password\n: ")
                    print(requests.post(global_var.server_adress+"/remove_data", params={
                        "username": login.user_connected,
                        "password": password,
                        "data_word": deletion,
                        }).json())
                    
            elif admin_choice == "del_user":
                deletion = input("who do you want to delete?\n: ")
                if not requests.post(global_var.server_adress+"/username_exist", json={"username": deletion}).json():
                    print(f"'{deletion}' does not exist")
                    continue
                if not input(f"are you sure to delete '{deletion}'?\n: ") == "yes":
                    continue
                password = input("please enter your password\n: ")
                print(requests.post(global_var.server_adress+"/admin_account_del", params={
                    "username": login.user_connected,
                    "password": password,
                    "account_name": deletion,
                    }).json())
                    
            elif admin_choice == "": break
            else: print("this option does not exist")

if __name__ == "__main__":
    Main().panel()