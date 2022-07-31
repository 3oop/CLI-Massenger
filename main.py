# an Open Source CLI Massenger
import os
import json
from datetime import datetime

salt = os.urandom(32)
from hashlib import pbkdf2_hmac
from getpass import getpass


# creating files
try:
    os.mkdir("accounts/")
except FileExistsError:
    pass

try:
    with open("accounts.txt", "a") as accfile:
        pass
except FileNotFoundError:
    with open("accounts.txt", "w") as accfile:
        pass

def register():
    username = input("Username  (Max Len. 32): ").strip()
    if ' ' in username:
        print("Username Invalid.\n")
        return False
    with open("accounts.txt", "r") as accfile:
        if accfile.read != '':
            for line in accfile.readlines():
                if username == line[:32].strip():
                    print("Username Taken.\n")
                    return False
            else:
                password = getpass("Enter a password: ")
                password = salt + pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
    with open("accounts.txt", "a") as accfile:
        accfile.write(f"{username.ljust(32)}{password}\n")
        print(f"{username} registered.\n")
        return True



def login():
    global user
    username = input("Username: ") 
    with open("accounts.txt", "r") as accfile:
        for line in accfile.readlines():
            if username == line[:32].strip():
                salt = line[34:66]
                key = line[32:]
                break
        else:
            print("Username not found.\n")
            return False
    password = getpass()
    print(type(password))
    for _ in range(3):
        salt = bytes(salt)
        new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
        print(key)
        print(salt)
        print(new_key)
        if key[32:] != new_key:
            password = getpass("Invalid Password!\nTry Again: ")
        else:
            user = username
            return True
    else:
        new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
        if key[32:] != new_key:
            print("Invalid Password! Get out.\n"+"+"*30)
            return False
        else:
            user = username
            return True 


# def deletehistory():
#     if user == None:
#         print("No User is Logged in.\n")
#         return False
#     with open(f"messages.txt", "w") as accfile:
#         accfile.flush()


def accountlist():
    print("List of registered accounts:")
    for d in os.listdir("accounts/"):
        print(d[:-4])
    print("\n")


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
    msg = {"Sender": user, "to": reciver, "Time": t, "Body": txt} 
    with open(f"account/{user}.json", "w") as msgfile:
        json.dump(msg, msgfile)



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
    # try:
    eval(f"{str(command)}()")
    # except:
        # print(f"{str(command)} is not a valid command.\n")
