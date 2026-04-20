import dico
import login
import global_var
import requests

class Main:
    def __init__(self):
        self.admin_list = ('admin', 'macto3001')

    def panel(self):
        # here is the panel where the user come first
        try:
            while True:
                choice = input("Welcome to the interactive-Dictionnary\n"
                               "What do you want to do?:\n"
                               "- search word 'search'\n"
                               "- account managment 'account'\n"
                               "- stop the script (nothing)\n"
                               ": ")
                if choice == "search": dico.dictionary()
                elif choice == "account": login.connection()
                elif choice == "": break
                elif choice == "admin" and login.user_connected in self.admin_list: self.admin_panel()
                else: print("This option do not exist.")
        except KeyboardInterrupt: print("program ended") # if ctrl+c

    def admin_panel(self):
        while True:
            admin_choice = input("Welcome to the admin panel\n"
            "What do you want to do?\n"
            "- see data list 'data_list'\n"
            "- see user list 'user_list'\n"
            "- delete def 'del_def'\n"
            "- delete user 'del_user'\n"
            "- exit (nothing)\n"
            ": ")
            if admin_choice == "data_list": print(f"dico data:\n{requests.get(global_var.server_adress+"/get_dico").json()}")
            elif admin_choice == "user_list": print(f"user data:\n{requests.get(global_var.server_adress+"/get_user").json()}")

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