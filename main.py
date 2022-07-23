# an Open Source CLI Massenger
import os
from datetime import datetime

salt = os.urandom(32)
from hashlib import pbkdf2_hmac
from getpass import getpass


# creating files
with open("messages.txt", "a") as msgfile:
    pass

with open("accounts.txt", "a") as accfile:
    pass


def register():
    name = input("Username: ").strip()
    if ' ' in name:
        print("Username Invalid.\n")
        return False
    with open("accounts.txt", "r") as accfile:
        if accfile.read != '':
            for line in accfile.readlines():
                if name in line:
                    print("Username Taken.\n")
                    return False
            else:
                password = getpass("Enter a password: ")
                password = salt + pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
    with open("accounts.txt", "a") as accfile:
        accfile.write(f"{name.ljust(32)}{password}\n")
        print(f"{name} registered.\n")
        return True


def login():
    name = input("Username: ") 
    with open("accounts.txt", "r") as accfile:
        for line in accfile.readlines():
            if name in line[:32]:
                key = line[32:]
                break
        else:
            print("Username not found.\n")
            return False
        password = getpass()
        new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
        if key[32:] != new_key:
            print("Invalid Password! Get out.\n")
            return False
        else:
            user = name
            return True


def deletehistory():
    if user == None:
        print("No User is Logged in.\n")
        return False
    with open(f"messages.txt", "w") as accfile:
        accfile.flush()

def accountlist():
    with open("accounts.txt", "r") as accfile:
        print("List of registered accounts:")
        for line in accfile.readlines():
            print(f"{line[:32]}")

def logout():
    global user
    if user == None:
        print("No user is logged, Please Log in.\n")
    else:
        user = None

def compose():
    global user
    if user == None:
        print("a user must be Logged in.\n")
        return False
    txt = input("Type your message:\n")
    reciver = input("To who?\n")
    t = datetime.now()
    msg = f"{user} to {reciver},{t},{txt}\n"
    with open("messages.txt", "a") as msgfile:
        msgfile.write(msg)



def exit():
    global run
    run = False


menu = ["exit", "login", "register", "accoutlist"]
user_menu = ["exit", "logout", "compose", "accoutlist", "deletehistory"]
user = None
run = True 


while run == True:
    if user == None:
        print(*menu, sep='\n')
    else:
        print(f"User: {user}")
        print(*user_menu, sep="\n")
    command = input("Type Your Command: ")
    try:
        eval(f"{str(command)}()")
    except:
        print(f"{command} is not a valid command.\n")
