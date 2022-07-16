# an Open Source CLI Massenger
import os
from typing import final
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
        accfile.write(f"{name},{password}")
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
                return True
            else:
                print("Username not found")
                return False


def logout():
    pass


run = True 

def main():
    login(input("Username: "))
    return True

if __name__ == "__main__":
    main()