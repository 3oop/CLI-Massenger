# an Open Source CLI Massenger
import os

salt = os.urandom(32)
from hashlib import pbkdf2_hmac
from getpass import getpass

user = None

def register(name):
    name = str(name).strip()
    if ' ' in name:
        print("Username Invalid")
        return False
    with open("accounts.txt", "r") as accfile:
        if accfile.read != '':
            for line in accfile.readlines():
                if name in line:
                    print("Username Taken")
                    return False
            else:
                password = getpass("Enter a password: ")
                password = salt + pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 100000)
    with open("accounts.txt", "a") as accfile:
        accfile.write(f"{name.ljust(32)},{password}")
        print(f"{name} registered.")
        return True


def login(name):
    with open("accounts.txt", "r") as accfile:
        for line in accfile.readlines():
            if name in line[32]:
                password = getpass()
                for _ in range(3):
                    new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 100000)
                    if line[32:] != new_key:
                        password = getpass("Invalid Password!\nTry Again: ")
                    else:
                        break
                else:
                    print("Invalid Password! Get out.\n"+"+"*30)
                    return False
                user = name
                return True
            else:
                print("Username not found")
                return False


def del_history():
    if user == None:
        print("No User is Logged in")
        return False
    with open(f"{user}.text", "w") as accfile:
        accfile.flush()

def acc_list():
    print()

def logout():
    user = None

def exit():
    run == False

menu = {
    '0': [exit , "Exit"],
    '1': [login , "Login"],
    '2': [register, "Register"],
    '3': [logout, "Log out"],
    '4': [del_history, "Delete History"],
    '5': [acc_list, "Account List"]
}

user_menu = []
user = None
run = True 

def main():
    while run == True:
        if user == None:
            print(*[f"{i} : {menu[i][1]}" for i in ['0', '1', '2'] ], sep='\n')
        else:
            print(*[f"{i} : {menu[i][1]}" for i in ['3', '4'] ], sep='\n')
            with open(f"{user}.txt", 'r') as accfile:
                eval(f"user_name = {accfile.readline()}")
            print("Chats:")
            print(*[f"{i}" for i in user_menu])
            


if __name__ == "__main__":
    main()