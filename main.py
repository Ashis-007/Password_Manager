import sqlite3
import secrets
import hashlib
import string
import base64
import os
import pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from user import User


salt = b'\xc3?\xedU\xb9\xd8<8\xc6\xf5\xf0\xce\xb6W|\xaa'
my_dict = {}


def show_options():
    choice = input(
        "(A)dd new password, (G)et password or (C)hange password, (L)ist all services, (S)ign out")
    if choice.lower() == "a":
        pass
    elif choice.lower() == "g":
        size = int(input("Enter the length of password you wish to keep: "))
        generate_pass(size)

    elif choice.lower() == "c":
        pass
    elif choice.lower() == "l":
        list_services()
    elif choice.lower() == "s":
        pass
    else:
        print("Wrong input!")

    show_options()


def login():
    global user
    username = input("Enter username: ")
    password = input("Enter master password: ")
    hash_mp = hash_pass(password)
    cursor.execute(
        "SELECT * FROM users where username = ? AND password = ? ;", (username, hash_mp))
    result = cursor.fetchall()

    if result:
        print(f"Welcome {username}")
        user = User(username, password)
        show_options()
    else:
        print("Invalid credentials. Please try again.")
        login()


def register():
    username = input("Enter username: ")
    pass1 = input(
        "Enter master password(Caution: You must remember this at all times!)\n: ")
    pass2 = input("Repeat master password: ")
    global user

    if pass1 == pass2:
        user = User(username)

        hash_mp = hash_pass(pass1)
        cursor.execute("INSERT INTO users VALUES (?,?);", (username, hash_mp))
        conn.commit()

        # generating key from master password
        master_pass = pass1.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_256,
            length=16,
            salt=salt,
            iterations=100000,
            backend=default_backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_pass))

        # storing the key in a file
        file = open("key.key", "wb")
        file.write(key)
        file.close()

        # creating a file to store passwords
        file = open("List.pkl", "wb")
        pickle.dump(my_dict, file)
        file.close()

        print("Your account has been created successfully.")
        print("Please login")
        login()

    else:
        print("Passwords do not match.\nPlease try again.")
        register()


# generate random password
def generate_pass(size):

    special_char = "!@#$%&*?."
    my_string = string.ascii_letters + string.digits + special_char
    password = None

    while True:
        password = ''.join(secrets.choice(my_string) for i in range(size))

        # one uppercase, one lowercase and 3 digits atleast
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    print(f"Here is your password: {password}")

    choice = input("Press Y to keep this / Press any key to get a new one: ")
    if choice.lower == "y":
        add_new_password(password)
    else:
        generate_pass(size)


# hashing the password
def hash_pass(password):
    b_pass = str.encode(password)
    b_salt = salt
    crypt = hashlib.pbkdf2_hmac("sha512", b_pass, b_salt, 100000, 16)
    new_pass = crypt.hex()
    return new_pass


def list_services():
    cursor.execute("SELECT services from list")


def add_new_password(password):
    service = input("Enter the name of the service: ")

    # getting the key from file
    file = open("key.key", "rb")
    key = file.read()
    file.close

    # encrypting the password and storing in dict
    password = password.encode()
    f = Fernet(key)
    pass_encrypted = f.encrypt(password)
    my_dict[service] = pass_encrypted

    # removing the previous file
    os.remove("C: \\Users\\ashis\\Desktop\\Password_Manager\\List.pkl")

    # creating a new file and
    # writing the dict into it
    file = open("List.pkl", "wb")
    pickle.dump(my_dict, file)
    file.close()


user = None
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# cursor.execute("""CREATE TABLE users
#                   (username TEXT PRIMARY KEY NOT NULL ,
#                   password TEXT NOT NULL) ;
# """)

# cursor.execute("""CREATE TABLE list
#                   (password TEXT PRIMARY KEY NOT NULL,
#                    services TEXT NOT NULL);""")

print("==== Welcome to LastPass ====")

choice = input("(C)reate an account, (L)ogin\n")
if choice.lower() == "c":
    register()
elif choice.lower() == "l":
    login()
else:
    print("Wrong input!")
