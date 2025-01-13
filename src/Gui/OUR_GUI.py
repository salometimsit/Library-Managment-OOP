import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from src.main_lib.Books import Books
from src.main_lib.BooksCategory import BooksCategory
from src.main_lib.Delete_Books import DeleteBooks
from src.main_lib.Logger import Logger
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
            Logger.log_add_message("logged in successfully")
            messagebox.showinfo("Welcome", f"hello {user.get_name()}!")
            self.root.destroy()
            MainScreen(tk.Tk(), self.library).display()
        else:
            Logger.log_add_message("logged in fail")
            messagebox.showerror("Error", "Invalid username or password")

    def register_new_user(self):
        self.root.destroy()
        RegisterScreen(tk.Tk(), self.library).display()


class MainScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self.root.title("Main Screen")
        self.root.geometry("600x400")

        tk.Label(self.root, text="Welcome to the Library!", font=("Helvetica", 16, "bold")).pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Book", width=20, command=lambda:
        self.open_add_book_screen()).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Remove Book", width=20, command=lambda:
        self.open_remove_book_screen()).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Search Book", width=20, command=
        self.open_search_screen).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="View Books", width=20, command=lambda:
        print("View Books selected")).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Lend Book", width=20, command=lambda:
        print("Lend Book selected")).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Return Book", width=20, command=lambda:
        print("Return Book selected")).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Logout", width=20, command=self.logout).pack(pady=20)

    def open_search_screen(self):
        self.root.destroy()
        SearchScreen(tk.Tk(), self.library).display()

    def open_add_book_screen(self):
        self.root.destroy()
        AddBookScreen(tk.Tk(), self.library).display()

    def open_remove_book_screen(self):
        self.root.destroy()
        RemoveBookScreen(tk.Tk(), self.library).display()

    def logout(self):
        try:
            self.root.destroy()
            Logger.log_add_message("logged out successfully")
            LoginScreen(tk.Tk(), self.library).display()
        except Exception as e:
            Logger.log_add_message(f"Logout failed: {str(e)}")
            messagebox.showerror("Error", "Logout failed. Please try again.")


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
            Logger.log_add_message("registered fail")
            messagebox.showerror("Error", "Username already registered")
        else:
            self.library.add_user(username, full_name, "librarian", password)
            Logger.log_add_message("registered successfully")
            messagebox.showinfo("Success", "User registered successfully!")
            self.root.destroy()
            LoginScreen(tk.Tk(), self.library).display()


class SearchScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)
        self.selected_row = None

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

        tree = ttk.Treeview(self.root, selectmode="browse")
        tree.pack(fill="both", expand=True, pady=10)
        tree.bind("<<TreeviewSelect>>", self.on_row_select)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Search",
                  command=lambda: self.perform_search(strategy_var, search_term_entry, tree)).pack(pady=10)
        tk.Button(self.root, text="Rent Book", command=self.rent_book).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.go_back).pack(pady=10)

    def perform_search(self, strategy_var, search_term_entry, tree):
        strategy = strategy_var.get()
        search_term = search_term_entry.get().strip()

        tree.delete(*tree.get_children())

        results = self.library.search_book(search_term, strategy)

        if not results:
            messagebox.showinfo("Info", "No results found.")
            return

        tree["columns"] = list(results[0].keys())
        tree["show"] = "headings"

        for col in results[0].keys():
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for index, book in enumerate(results):
            tree.insert("", "end", iid=index, values=list(book.values()))

    def on_row_select(self, event):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            self.selected_row = tree.item(selected_item, "values")

    def rent_book(self):
        if self.selected_row:

            keys = ["title", "author", "is_loaned", "total_books", "genre", "year", "popularity"]
            book_data = {key: value for key, value in zip(keys, self.selected_row)}

            book = Books.create_book(
                title=book_data["title"],
                author=book_data["author"],
                is_loaned=book_data["is_loaned"],
                total_books=int(book_data["total_books"]),
                genre=book_data["genre"],
                year=int(book_data["year"]),
                popularity=int(book_data["popularity"])
            )

            success = self.library.rent_book(book)

            if success:
                messagebox.showinfo("Success", f"Book '{book_data['title']}' has been rented.")
            else:
                messagebox.showerror("Error", f"Could not rent book '{book_data['title']}'.")
        else:
            messagebox.showerror("Error", "No book selected!")

    def go_back(self):
        self.root.destroy()
        MainScreen(tk.Tk(), self.library).display()


class AddBookScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)
        self.selected_row = None

    def display(self):

        self.root.title("Add Book to Library")
        self.root.geometry("350x350")

        self.title_label = tk.Label(self.root, text="Book Title:")
        self.title_label.grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        self.author_label = tk.Label(self.root, text="Author:")
        self.author_label.grid(row=1, column=0, padx=10, pady=10)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1, padx=10, pady=10)

        self.copies_label = tk.Label(self.root, text="Copies:")
        self.copies_label.grid(row=2, column=0, padx=10, pady=10)
        self.copies_entry = tk.Entry(self.root)
        self.copies_entry.grid(row=2, column=1, padx=10, pady=10)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=3, column=0, padx=10, pady=10)
        self.category_combobox = ttk.Combobox(self.root, values=[category.value for category in BooksCategory])
        self.category_combobox.grid(row=3, column=1, padx=10, pady=10)

        self.year_label = tk.Label(self.root, text="Year:")
        self.year_label.grid(row=4, column=0, padx=10, pady=10)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=4, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.grid(row=6, column=0, columnspan=2, pady=20)


    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        copies = self.copies_entry.get()
        category = self.category_combobox.get()
        year = self.year_entry.get()

        if not title or not author or not copies or not category or not year:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try:
            copies = int(copies)
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Copies and Year must be integers!")
            return

        success = self.library.add_book(title, author, copies, category, year)

        if success:
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.clear_fields()
        else:
            messagebox.showwarning("Warning", f"Book '{title}' already exists. Copies updated.")

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.copies_entry.delete(0, tk.END)
        self.category_combobox.set('')
        self.year_entry.delete(0, tk.END)

    def go_back(self):
        self.root.destroy()
        MainScreen(tk.Tk(), self.library).display()

class RemoveBookScreen(WindowInterface):
    from src.main_lib.Books import Books
    def __init__(self, root, library):
        super().__init__(root, library)
        self.selected_row = None

    def display(self):
        self.root.title("Remove Book from Library")
        self.root.geometry("350x350")

        self.title_label = tk.Label(self.root, text="Book Title:")
        self.title_label.grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        self.author_label = tk.Label(self.root, text="Author:")
        self.author_label.grid(row=1, column=0, padx=10, pady=10)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1, padx=10, pady=10)


        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=2, column=0, padx=10, pady=10)
        self.category_combobox = ttk.Combobox(self.root, values=[category.value for category in BooksCategory])
        self.category_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.year_label = tk.Label(self.root, text="Year:")
        self.year_label.grid(row=3, column=0, padx=10, pady=10)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=3, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Remove Book", command=self.remove_book)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.grid(row=5, column=0, columnspan=2, pady=20)

    def remove_book(self):
        ans=False
        title = self.title_entry.get()
        author = self.author_entry.get()
        category = self.category_combobox.get()
        year = self.year_entry.get()
        if not title or not author or not category or not year:
            messagebox.showerror("Error", "All fields must be filled!")
            return
        try:
            year = int(year)
        except ValueError:
            Logger.log_add_message("book removed fail")
            messagebox.showerror("Error", "Year must be integer!")
            return
        try:
            main_lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "main_lib"))
            file_path = os.path.join(main_lib_path, "Excel_Tables", "books.csv")
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            Logger.log_add_message("book removed fail")
            messagebox.showerror("Error", "Books database file not found!")
            return
        matching_books = df[(df['title'] == title) &(df['author'] == author) &(df['genre'] == category) &
            (df['year'] == year)]
        if matching_books.empty:
            Logger.log_add_message("book removed fail")
            messagebox.showerror("Error", "Book not found!")
            return
        book_data = matching_books.iloc[0].to_dict()
        book = Books(title=book_data['title'],is_loaned=book_data['is_loaned'],author=book_data['author'],total_books=book_data["copies"],
                    genre=book_data['genre'],year=book_data['year'],popularity=book_data['popularity'])
        try:
            ans=self.library.remove_book(book)
        except Exception:
            Logger.log_add_message("book removed fail")
            messagebox.showerror("Error", "Book could not be deleted!")
            return
        if ans:
            messagebox.showinfo("Success", f"Book '{book_data['title']}' has been deleted.")
            self.clear_fields()
            return
        else:
            Logger.log_add_message("book removed fail")
            messagebox.showerror("Error", "Book could not be deleted!")
            return

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_combobox.set('')
        self.year_entry.delete(0, tk.END)

    def go_back(self):
        self.root.destroy()
        MainScreen(tk.Tk(), self.library).display()









if __name__ == '__main__':
    library = Library()
    root = tk.Tk()
    LoginScreen(root, library).display()
    root.mainloop()
