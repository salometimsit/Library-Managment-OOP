
import tkinter as tk
from tkinter import messagebox

from src.Gui.WindowInterface import WindowInterface


class LoginScreen(WindowInterface):
    """
    in this class we dealing with the login screen
    """
    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self._root.title("Library Management System")
        self._root.geometry("300x300")

        tk.Label(self._root, text="Username:").pack(pady=10)
        username_entry = tk.Entry(self._root)
        username_entry.pack(pady=5)

        tk.Label(self._root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self._root, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(self._root, text="Login", command=lambda: self.login(username_entry, password_entry))
        login_button.pack(pady=10)

        register_button = tk.Button(self._root, text="Register", command=self.register_new_user)
        register_button.pack(pady=10)

    def login(self, username_entry, password_entry):
        from src.Gui.MainScreen import MainScreen
        """
        Handles the user login process.
        If successful, initializes the main screen with the logged-in user.
        """
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        result = self._library.user_login(username, password)
        if result:
            messagebox.showinfo("Welcome", f"hello {username}!")
            self._root.destroy()
            main_screen = MainScreen(tk.Tk(), self._library)
            main_screen.display()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register_new_user(self):
        from src.Gui.RegisterScreen import RegisterScreen
        """
        activating the register window
        """
        self._root.destroy()
        RegisterScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        self._root.destroy()

