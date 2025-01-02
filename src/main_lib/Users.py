import base64
import csv
import hashlib
import os

from src.main_lib.Library import Library

"""
This class is a for the librarians in the library cause all the system is for them
"""


class User:
    def __init__(self, name, username, role, password):
        self.__name = name
        self.__username = username
        self.__role = role
        self.__password = self.do_encriptation(str(password))
        self.save_to_file()

    def get_name(self):
        return self.__name

    def get_username(self):
        return self.__username

    def get_role(self):
        return self.__role

    def do_encriptation(self, password):
        if isinstance(password, str):
            password = password.encode()
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
        return base64.b64encode(salt + hashed_password).decode('utf-8')

    def check_password(self, password):
        password_bytes = base64.b64decode(self.__password)
        salt = password_bytes[:16]
        stored_hash = password_bytes[16:]
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hashed_password == stored_hash

    def convert_dictionary(self):
        return {'name': self.__name, 'username': self.__username, 'role': self.__role,
                'password': self.__password}

    def save_to_file(self):
        file_exists = os.path.isfile("users.csv")
        existing_users = set()
        if file_exists:
            with open("users.csv", mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_users.add(row['username'])
        if self.__username not in existing_users:
            with open("users.csv", mode='a', newline='') as file:
                fieldnames = ['name', 'username', 'role', 'password']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(self.convert_dictionary())

    @staticmethod
    def get_all_users():
        users = []
        if os.path.isfile("users.csv"):
            with open("users.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User(row["name"], row["username"], row["role"], row["password"])
                    user._User__password = row["password"]  # Prevent re-encryption
                    users.append(user)
        return users

    def notify_all(self, message):
        lib = Library.get_instance()
        lib.notify(message)
