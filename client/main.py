import dico

class Main:
    def __init__(self):
        self.admin_list = ('admin', 'macto3001')

    def panel(self):
        # here is the panel where the user come first
        try:
            while True:
                choice = input("Bienvenue sur le disctionnaire.\n"
                               "Que voulez vous faire ?:\n"
                               "- chercher des mots 'search'\n"
                               "- gestion du compte 'compte'\n"
                               "- couper le programme (rien)\n"
                               ": ")
                if choice == "search": dico.dictionary()
                elif choice == "compte": print("not added yet, sorry")#login.connection()
                elif choice == "": break
                # elif choice == "admin" and login.user_connected in self.admin_list: self.admin_panel()
                else: print("Cette option n'existe pas.")
        except KeyboardInterrupt: print("program ended") # if ctrl+c

if __name__ == "__main__":
    Main().panel()