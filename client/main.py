import dico
import login

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
                elif choice == "compte": login.connection()
                elif choice == "": break
                # elif choice == "admin" and login.user_connected in self.admin_list: self.admin_panel()
                else: print("This option do not exist.")
        except KeyboardInterrupt: print("program ended") # if ctrl+c

if __name__ == "__main__":
    Main().panel()