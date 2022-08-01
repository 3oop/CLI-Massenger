# an Open Source CLI Massenger
import os
from datetime import datetime

from numpy import rec

# salt = os.urandom(32)
salt = bytes("salt", 'utf_8')
from hashlib import pbkdf2_hmac
from getpass import getpass

import json

# creating files
try:
    os.mkdir("accounts/")
except FileExistsError:
    pass


def register():
    username = input("Username  (Max Len. 32): ").strip()
    if ' ' in username or username == ' ':
        print("Username Invalid.\n")
        return False
    try:
        with open(f"accounts/{username}.json", "r") as accfile:
            print("Username Taken.\n")
            return False
    except FileNotFoundError:
        password = getpass("Enter a password: ")
        password = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
        acc = {'Username': username, 'Password': str(password), 'Chats': []}
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
        new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
        if acc["Password"] != str(new_key):
            password = getpass("Invalid Password!\nTry Again: ")
        else:
            user = username
            return True
    else:
        new_key = pbkdf2_hmac('sha256', password.encode('utf_8'), salt, 9999)
        if acc["Password"][32:] != new_key:
            print("Invalid Password! Get out.\n"+"+"*30)
            return False
        else:
            user = username
            return True 


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
    reciver = input("To who?\n")
    txt = input("Type your message:\n")
    t = datetime.now()
    seen = False
    try:
        with open(f"{user} {reciver}.json", "a") as msgfile:
            chat = json.loads(msgfile)
            print(type(chat))
            chat.append({"reciver": reciver, "txt" : txt, "t": t, "seen": seen})
    except FileNotFoundError:
        with open(f"{reciver} {user}.json", "a") as msgfile:
            chat = json.loads(msgfile)
            print(type(chat))
            chat.append({"reciver": reciver, "txt" : txt, "t": t, "seen": seen})
    print("Message Saved.\n")



def exit():
    global run
    run = False


menu = ["exit", "login", "register", "accoutlist"]
user_menu = ["exit", "logout", "compose", "chatlist"]
user = None
run = True 


while run == True:
    if user == None:
        print(*menu, sep='\n')
    else:
        with open(f"accounts/{user}.json", "r") as accfile:
            acc = json.loads(accfile.read())
        print(f"\nUser : {user}\n")
        print(f"Chatlist : ")
        for c in acc["Chats"]:
            print(c)
        print('\n')
        print(*user_menu, sep="\n")
    command = input("Type Your Command: ")
    try:
        eval(f"{str(command)}()")
    except:
        print(f"{command} is not a valid command.\n")
