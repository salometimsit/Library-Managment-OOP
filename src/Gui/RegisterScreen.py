
import tkinter as tk
from tkinter import messagebox

from src.Gui.WindowInterface import WindowInterface


class RegisterScreen(WindowInterface):
    """
    This class handles with all the user registration.
    """
    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self._root.title("Register New User")
        self._root.geometry("400x400")

        tk.Label(self._root, text="Full Name:").pack(pady=10)
        name_entry = tk.Entry(self._root)
        name_entry.pack(pady=5)

        tk.Label(self._root, text="Username:").pack(pady=10)
        username_entry = tk.Entry(self._root)
        username_entry.pack(pady=5)

        tk.Label(self._root, text="Password:").pack(pady=10)
        password_entry = tk.Entry(self._root, show="*")
        password_entry.pack(pady=5)

        register_button = tk.Button(self._root, text="Register", command=lambda: self.handle_registration
        (name_entry, username_entry, password_entry))
        register_button.pack(pady=20)
        back_button = tk.Button(self._root, text="Back", command=self.go_back)
        back_button.pack(pady=20)

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the login screen.")

    def handle_registration(self, name_entry, username_entry, password_entry):
        from src.Gui.LogginScreen import LoginScreen
        """
        here the system checks if the user is already registered. and register if not.
        """
        full_name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        result = self._library.user_register(full_name, username, password)
        if not result:
            messagebox.showerror("Error", "Username already registered")
        else:
            messagebox.showinfo("Success", "User registered successfully!")
            self._root.destroy()
            LoginScreen(tk.Tk(), self._library).display()

    def go_back(self):
        from src.Gui.LogginScreen import LoginScreen
        self._root.destroy()
        LoginScreen(tk.Tk(), self._library).display()

