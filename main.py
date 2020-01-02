def login():
    pass


def register():
    pass


def generate_pass():
    pass


def list_services():
    pass


def add_new_password():
    pass


print("==== Welcome to LastPass ====")

choice = input("""(C)reate an account \n(L)ogin""")
if choice.lower == "c":
    register()
else:
    login()
