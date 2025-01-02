import base64
import csv
import hashlib
import os
from src.main_lib.Library import Library

"""
This class is a for the librarians in the library cause all the system is for them
"""
class User:
    def __init__(self, name, username, role, password, is_encrypted=False):
        self.library=Library.get_instance()
        self.__name = name
        self.__username = username
        self.__role = role
        self.__password = password if is_encrypted else self.do_encriptation(str(password))
        if not is_encrypted:
            self.save_to_file()

    def get_name(self):
        return self.__name

    def get_username(self):
        return self.__username

    def get_role(self):
        return self.__role

    @staticmethod
    def do_encriptation(password):
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
        file_path = os.path.join(os.path.dirname(__file__), "Excel_Tables/users.csv")
        file_path = os.path.abspath(file_path)
        file_exists = os.path.isfile(file_path)
        existing_users = set()
        if file_exists:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_users.add(row['username'])
        if self.__username not in existing_users:
            with open(file_path, mode='a', newline='') as file:
                fieldnames = ['name', 'username', 'role', 'password']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(self.convert_dictionary())

    @staticmethod
    def get_all_users():
        users = []
        if os.path.isfile("Excel_Tables/users.csv"):
            with open("Excel_Tables/users.csv", mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User(row["name"], row["username"], row["role"], row["password"],is_encrypted=True)
                    users.append(user)
        return users

    def notify_all(self, message):
        self.library.notify(message)
