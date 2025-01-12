import base64
import csv
import hashlib
import os
from src.main_lib.Library import Library

class User:
    """
    Represents a user in the library system, primarily librarians.

    Attributes:
        library (Library): The library instance associated with the user.
        __name (str): Name of the user.
        __username (str): Username of the user.
        __role (str): Role of the user (e.g., Librarian).
        __password (str): Encrypted password of the user.
    """

    def __init__(self, name, username, role, password, is_encrypted=False):
        """
        Initializes a User instance.

        Args:
            name (str): Name of the user.
            username (str): Username of the user.
            role (str): Role of the user.
            password (str): Plaintext or encrypted password.
            is_encrypted (bool): Indicates if the provided password is already encrypted.
        """
        self.library = Library.get_instance()
        self.__name = name
        self.__username = username
        self.__role = role
        self.__password = password if is_encrypted else self.do_encriptation(str(password))
        if not is_encrypted:
            self.save_to_file()

    def get_name(self):
        """Returns the name of the user."""
        return self.__name

    def get_username(self):
        """Returns the username of the user."""
        return self.__username

    def get_role(self):
        """Returns the role of the user."""
        return self.__role

    @staticmethod
    def do_encriptation(password):
        """
        Encrypts the provided password using PBKDF2 and a random salt.

        Args:
            password (str): Plaintext password to be encrypted.

        Returns:
            str: Encrypted password.
        """
        if isinstance(password, str):
            password = password.encode()
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
        return base64.b64encode(salt + hashed_password).decode('utf-8')

    def check_password(self, password):
        """
        Validates a plaintext password against the stored encrypted password.

        Args:
            password (str): Plaintext password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        password_bytes = base64.b64decode(self.__password)
        salt = password_bytes[:16]
        stored_hash = password_bytes[16:]
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hashed_password == stored_hash

    def convert_dictionary(self):
        """
        Converts the user's attributes to a dictionary format.

        Returns:
            dict: Dictionary representation of the user.
        """
        return {'name': self.__name, 'username': self.__username, 'role': self.__role, 'password': self.__password}

    def save_to_file(self):
        """
        Saves the user's data to the users.csv file if the username does not already exist.
        """
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
        """
        Retrieves all users from the users.csv file.

        Returns:
            list: List of User instances.
        """
        users = []
        file_path = os.path.join(os.path.dirname(__file__), "Excel_Tables/users.csv")
        file_path = os.path.abspath(file_path)
        if os.path.isfile(file_path):
            with open(file_path, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = User(row["name"], row["username"], row["role"], row["password"], is_encrypted=True)
                    users.append(user)
        return users

    def notify_all(self, message):
        """
        Sends a notification message to all users in the library system.

        Args:
            message (str): The notification message to send.
        """
        self.library.notify(message)