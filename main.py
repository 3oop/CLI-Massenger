# an Open Source CLI Massenger
import os

salt = os.urandom(32)
from hashlib import pbkdf2_hmac
from getpass import getpass


with open("messages.txt", "a") as msgfile:
    pass

with open("accounts.txt", "a") as accfile:
    pass


def register():
    name = input("Username: ").strip()
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
                password = salt + pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
    with open("accounts.txt", "a") as accfile:
        accfile.write(f"{name.ljust(32)},{password}\n")
        print(f"{name} registered.")
        return True


def login():
    name = input("Username: ") 
    with open("accounts.txt", "r") as accfile:
        for line in accfile.readlines():
            if name in line[32]:
                password = getpass()
                new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
                if line[32:] != new_key:
                    print("Invalid Password! Get out.\n"+"+"*30)
                    return False
                else:
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
    with open("accounts.txt", "r") as accfile:
        print("List of registered accounts:")
        while accfile.readline():
            print(f"{accfile.readline()[:32]}")

def logout():
    if user == None:
        print("No user is logged, Please Log in")
    else:
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

acc_list()
    


while run == True:
    if user == None:
        print(*[f"{i} : {menu[i][1]}" for i in ['0', '1', '2'] ], sep='\n')
    else:
        print(f"User: {user}")
    command = input("Type Your Command: ")
    command = f"{str(command)}()"
    # print(command)
    try:
        eval(command)
    except:
        print(f"{command[:-2]} is not a valid command.")
    