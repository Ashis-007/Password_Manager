class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__services = []

    def get_usermame(self):
        return self.__username

    def add_new_service(self, service):
        self.__services.append(service)
