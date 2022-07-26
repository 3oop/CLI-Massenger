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


def register():
    username = input("Username  (Max Len. 32): ").strip()
    if ' ' in username:
        print("Username Invalid.\n")
        return False
    try:
        with open(f"accounts/{username}.json", "r") as accfile:
            print("Username Taken.\n")
            return False
    except FileNotFoundError:
        password = getpass("Enter a password: ")
        password = salt + pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
        acc = {'Username': username, 'Password': str(password), 'Chats': None}
        # print(type(password))
        with open(f"accounts/{username}.json", "w") as accfile:
            json.dump(acc, accfile)
            print(f"{username} registered.\n")
            return True


def login():
    global user
    username = input("Username: ") 
    try:
        with open(f"accounts/{username}.json", "r") as accfile:
            acc = json.loads(accfile.read())   
    except FileNotFoundError:
        print("Username not found.\n")
        return False
    password = getpass()
    for _ in range(3):
        new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 100000)
        if acc["Password"][32:] != new_key:
            password = getpass("Invalid Password!\nTry Again: ")
        else:
            user = username
            return True
    else:
        new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 100000)
        if acc["Password"][32:] != new_key:
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
