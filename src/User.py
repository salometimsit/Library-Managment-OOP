import hashlib


class User:
    # observer design pattern

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"Username: {self}", f"Role: {self}"

    def register(self, file_path="data/users.csv"):
        # here we need to write the client n the new excel file!
        pass

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
