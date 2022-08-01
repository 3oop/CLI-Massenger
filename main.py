# an Open Source CLI Massenger
import os
from datetime import datetime
from tokenize import Name

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

try:
    os.mkdir("chats/")
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
    try:
        with open(f"accounts/{reciver}.json", "r") as accfile:
            pass
    except FileNotFoundError:
        print(f"{reciver} is not a registered user.\n")
        return False
    txt = input("Type your message:\n")
    t = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    seen = False
    for chat in os.listdir("chats/"):
        if chat == f"{user} {reciver}.json" or chat == f"{reciver} {user}.json":
            chatpath = chat
            break
    else:
        chatpath = f"{user} {reciver}.json"
        with open(f"chats/{chatpath}", 'w') as chatfile:
            first_msg = {"sender": "system", "txt" : "This Chat has begun", "t": datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "seen": True}
            x = json.dumps(first_msg)
            chatfile.write(x)

    with open(f"chats/{chatpath}", "a") as chatfile:
        msg = {"sender": user, "txt" : txt, "t": t, "seen": seen}
        x = json.dumps(msg)
        chatfile.write('\n'+x)

    with open(f"accounts/{user}.json", "r") as accfile:
        acc = json.loads(accfile.read())
    if chatpath not in acc["Chats"]:
        acc["Chats"].append(chatpath)
    with open(f"accounts/{user}.json", "w") as accfile:
        x = json.dumps(acc)
        accfile.write(x)

    with open(f"accounts/{reciver}.json", "r") as accfile:
        acc = json.loads(accfile.read())
    if chatpath not in acc["Chats"]:
        acc["Chats"].append(chatpath)
    with open(f"accounts/{reciver}.json", "w") as accfile:
        accfile.write(x)
    print("Message Saved.\n")


def viewchat():
    chatpath = input("Choose from Chatlist: ").strip() + ".json"
    with open(f"chats/{chatpath}", 'r+') as chatfile:
        pos = 0
        for l in chatfile.readlines():
            pos += len(l)+1
            x = json.loads(l)
            t = x['t']
            sen = x["sender"]
            txt = x["txt"]
            print(f"{t} {sen}: {txt}")
            if x["sender"] != user and x["seen"] == False:
                x["seen"] = True
                chatfile.seek(pos, 0)
                chatfile.write(len(l)*' ')
                chatfile.seek(pos, 0)
                y = json.dumps(x)
                chatfile.write(y)
    if input("Press Enter.."):
        return True


def exit():
    global run
    run = False


menu = ["exit", "login", "register", "accoutlist"]
user_menu = ["exit", "logout", "compose", "viewchat"]
user = None
run = True 


while run == True:
    if user == None:
        print(*menu, sep='\n')
    else:
        with open(f"accounts/{user}.json", "r") as accfile:
            acc = json.loads(accfile.read())
        print(f"\nUser : {user}\n")
        print(f"Chatlist : (* means you have unread messages.)")
        for c in acc["Chats"]:
            with open(f"chats/{c}", "r") as chatfile:
                for l in chatfile.readlines():
                    x = json.loads(l)
                    if x["seen"] == False and x["sender"] != user:
                        s = '*'
                        break
                    else:
                        s = ''
            print(c[:-5], s)
        print('\n')
        print(*user_menu, sep="\n")
    command = input("Type Your Command: ")
    try:
        eval(f"{str(command)}()")
    except (NameError, TypeError):
        print(f"{command} is not a valid command.\n")
