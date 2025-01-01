import hashlib


class User:
    # observer design pattern

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"Username: {self.username}, Role: {self.role},password:{self.password} "

    def register(self, file_path="clientregister.csv"):
        # here we need to write the client in the new excel file!
        try:
            with open(file_path, 'a') as file:
                file.write(f"{self.username},{self.password},{self.role}\n")
            print(f"User {self.username} registered successfully.")
        except Exception as e:
            print(f"Failed to register user {self.username}: {e}")

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def update(self, message):
        print(f"Notification for {self.username}: {message}")
