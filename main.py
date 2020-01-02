import sqlite3
from user import User


def show_options():
    choice = input(
        "(A)dd new password, (G)et password or (C)hange password, (L)ist all services, (S)ign out")
    if choice.lower() == "a":
        pass
    elif choice.lower() == "g":
        pass
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
    cursor.execute(
        "SELECT * FROM users where username = ? AND password = ? ;", (username, password))
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
        cursor.execute("INSERT INTO users VALUES (?,?);", (username, pass1))
        conn.commit()
        user = User(username, pass1)
        print("Your account has been created successfully.")
        print("Please login")
        login()

    else:
        print("Passwords do not match.\nPlease try again.")
        register()


def generate_pass():
    pass


def list_services():
    user.show_services()


def add_new_password():
    pass


user = None
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# cursor.execute("""CREATE TABLE users
#                   (username TEXT PRIMARY KEY NOT NULL ,
#                   password TEXT NOT NULL) ;
# """)

print("==== Welcome to LastPass ====")

choice = input("(C)reate an account, (L)ogin\n")
if choice.lower() == "c":
    register()
elif choice.lower() == "l":
    login()
else:
    print("Wrong input!")
