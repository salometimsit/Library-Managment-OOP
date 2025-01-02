import tkinter as tk
from tkinter import messagebox
from src.main_lib.Users import User


class GuiForLibrary:
    class GuiForLibrary:
        def login(self, role_var, username_entry, password_entry):
            from src.main_lib.Library import Library
            print("Logging in...")
            role = role_var.get()
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            print(f"Trying to login with username: {username} and role: {role}")

            users = User.get_all_users()
            print(users)

            user = next((u for u in users if u.get_username() == username and u.get_role() == role), None)

            if user is None:
                print("User not found.")
                messagebox.showerror("Error", "User not found")
                return

            print(f"User found: {user.get_username()}")  # Debug: Print the found user

            if user.check_password(password):
                messagebox.showinfo("Welcome", f"{user.get_name()}!")
            else:
                print("Password is incorrect.")  # Debug: Check why password is incorrect
                messagebox.showerror("Error", "Password is incorrect")

    def start(self):
        root = tk.Tk()
        root.title("Entry")

        # creating vaiables
        role_var = tk.StringVar(value="student")

        # creating title
        tk.Label(root, text="Choose your role").pack(pady=15)

        # role titles
        tk.Radiobutton(root, text="Student", variable=role_var, value="student").pack()
        tk.Radiobutton(root, text="Librarian", variable=role_var, value="librarian").pack()

        # input
        tk.Label(root, text="Username:").pack(pady=10)
        username_entry = tk.Entry(root)
        username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(root, show="*")
        password_entry.pack(pady=5)

        # login button
        login_button = tk.Button(root, text="login", command=lambda: self.login(role_var, username_entry, password_entry))
        login_button.pack(pady=20)

        root.mainloop()  # Make sure to call this to display the window

if __name__ == '__main__':
    lib = Library.get_instance()
    lib.add_user("itay segev","itay","librarian","it")
    GuiForLibrary().start()
