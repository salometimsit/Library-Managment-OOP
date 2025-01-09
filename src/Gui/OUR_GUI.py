import tkinter as tk
from tkinter import ttk, messagebox
from src.main_lib.Users import User
from src.main_lib.Library import Library


class WindowInterface:
    def __init__(self, root, library):
        self.root = root
        self.library = library

    def display(self):
        raise NotImplementedError("This method should be implemented by subclasses.")


class LoginScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self.root.title("Library Management System")
        self.root.geometry("300x300")

        tk.Label(self.root, text="Username:").pack(pady=10)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", command=lambda: self.login(username_entry, password_entry))
        login_button.pack(pady=10)

        register_button = tk.Button(self.root, text="Register", command=self.register_new_user)
        register_button.pack(pady=10)

    def login(self, username_entry, password_entry):
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        users = User.get_all_users()
        user = next((u for u in users if u.get_username() == username), None)

        if user and user.check_password(password):
            messagebox.showinfo("Welcome", f"{user.get_name()}!")
            self.root.destroy()
            MainScreen(tk.Tk(), self.library).display()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register_new_user(self):
        self.root.destroy()
        RegisterScreen(tk.Tk(), self.library).display()


class MainScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self.root.title("Main Screen")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Welcome to the Library!", font=("Helvetica", 16, "bold")).pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Book", width=20, command=lambda: print("Add Book selected")).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=10,
                                                                                                            pady=10)
        tk.Button(button_frame, text="Remove Book", width=20, command=lambda: print("Remove Book selected")).grid(row=0,
                                                                                                                  column=1,
                                                                                                                  padx=10,
                                                                                                                  pady=10)
        tk.Button(button_frame, text="Search Book", width=20, command=self.open_search_screen).grid(row=1, column=0,
                                                                                                    padx=10, pady=10)
        tk.Button(button_frame, text="View Books", width=20, command=lambda: print("View Books selected")).grid(row=1,
                                                                                                                column=1,
                                                                                                                padx=10,
                                                                                                                pady=10)
        tk.Button(button_frame, text="Lend Book", width=20, command=lambda: print("Lend Book selected")).grid(row=2,
                                                                                                              column=0,
                                                                                                              padx=10,
                                                                                                              pady=10)
        tk.Button(button_frame, text="Return Book", width=20, command=lambda: print("Return Book selected")).grid(row=2,
                                                                                                                  column=1,
                                                                                                                  padx=10,
                                                                                                                  pady=10)

        tk.Button(self.root, text="Logout", width=20, command=self.logout).pack(pady=20)

    def open_search_screen(self):
        self.root.destroy()
        SearchScreen(tk.Tk(), self.library).display()

    def logout(self):
        self.root.destroy()
        LoginScreen(tk.Tk(), self.library).display()


class RegisterScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self.root.title("Register New User")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Full Name:").pack(pady=10)
        name_entry = tk.Entry(self.root)
        name_entry.pack(pady=5)

        tk.Label(self.root, text="Username:").pack(pady=10)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=10)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        register_button = tk.Button(self.root, text="Register",
                                    command=lambda: self.handle_registration(name_entry, username_entry,
                                                                             password_entry))
        register_button.pack(pady=20)

    def handle_registration(self, name_entry, username_entry, password_entry):
        full_name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        users = User.get_all_users()
        if any(u.get_username() == username for u in users):
            messagebox.showerror("Error", "Username already registered")
        else:
            self.library.add_user(username, full_name, "librarian", password)
            messagebox.showinfo("Success", "User registered successfully!")
            self.root.destroy()
            LoginScreen(tk.Tk(), self.library).display()


class SearchScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self.root.title("Search Books")
        self.root.geometry("800x600")

        tk.Label(self.root, text="Select Search Strategy:").pack(pady=10)
        strategy_var = tk.StringVar(value="title")

        tk.Radiobutton(self.root, text="Title", variable=strategy_var, value="title").pack(anchor="w")
        tk.Radiobutton(self.root, text="Author", variable=strategy_var, value="author").pack(anchor="w")
        tk.Radiobutton(self.root, text="Year", variable=strategy_var, value="year").pack(anchor="w")
        tk.Radiobutton(self.root, text="Genre", variable=strategy_var, value="genre").pack(anchor="w")

        tk.Label(self.root, text="Enter Search Term:").pack(pady=10)
        search_term_entry = tk.Entry(self.root)
        search_term_entry.pack(pady=5)

        tree = ttk.Treeview(self.root)
        tree.pack(fill="both", expand=True, pady=10)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Search",
                  command=lambda: self.perform_search(strategy_var, search_term_entry, tree)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=10)

    def perform_search(self, strategy_var, search_term_entry, tree):
        strategy = strategy_var.get()
        search_term = search_term_entry.get().strip()
        results = self.library.search_book(search_term, strategy)

        tree.delete(*tree.get_children())
        if results.empty:
            messagebox.showinfo("Info", "No results found.")
        else:
            tree["columns"] = list(results.columns)
            tree["show"] = "headings"
            for col in results.columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            for _, row in results.iterrows():
                tree.insert("", "end", values=list(row))

    def go_back(self):
        self.root.destroy()
        MainScreen(tk.Tk(), self.library).display()


if __name__ == '__main__':
    library = Library()
    root = tk.Tk()
    LoginScreen(root, library).display()
    root.mainloop()
