import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from src.main_lib.Library import Library
from src.main_lib.Logger import Logger


class WindowInterface:
    def __init__(self, root, library):
        self._root = root
        self._library = library
        self.center_window()
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        if not isinstance(self, (LoginScreen, RegisterScreen)) and not self._library.check_login():
            messagebox.showerror("Error", "Login needed to be for open the system")
            self._root.destroy()

    def display(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def on_closing(self):
        if isinstance(self, LoginScreen):
            self._root.destroy()
        else:
            messagebox.showwarning("Warning", "Please use the proper logout button to exit.")

    def center_window(self):
        """Centers the window on the screen."""
        self._root.update_idletasks()

        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()

        window_width = self._root.winfo_width()
        window_height = self._root.winfo_height()

        x = int((screen_width / 2.5) - (window_width // 2))
        y = int((screen_height / 4.5) - (window_height // 2))

        self._root.geometry(f'+{x}+{y}')


class LoginScreen(WindowInterface):
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
        """
        Handles the user login process.
        If successful, initializes the main screen with the logged-in user.
        """
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        result=self._library.user_login(username, password)
        if result:
            messagebox.showinfo("Welcome", f"hello {username}!")
            self._root.destroy()
            main_screen = MainScreen(tk.Tk(), self._library)
            main_screen.display()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register_new_user(self):
        self._root.destroy()
        RegisterScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        self._root.destroy()


class MainScreen(WindowInterface):
    """
    Main screen of the library management system.
    Handles the display of main menu and navigation.
    """

    def __init__(self, root, library):
        super().__init__(root, library)

    def display(self):
        self._root.title("Main Screen")
        self._root.geometry("600x400")

        tk.Label(self._root, text="Welcome to the Library!", font=("Helvetica", 16, "bold")).pack(pady=20)

        button_frame = tk.Frame(self._root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Book", width=20, command=lambda:
        self.open_add_book_screen()).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Remove Book", width=20, command=lambda:
        self.open_remove_book_screen()).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Search Book", width=20, command=
        self.open_search_screen).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="View Books", width=20, command=lambda:
        self.open_display_books_screen()).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Popular Books", width=20, command=lambda:
        self.open_popular_books_screen()).grid(row=2, columnspan=2, padx=10, pady=10)
        tk.Button(self._root, text="Logout", width=20, command=self.logout).pack(pady=20)

    def open_search_screen(self):
        self._root.destroy()
        SearchScreen(tk.Tk(), self._library).display()

    def open_add_book_screen(self):
        self._root.destroy()
        AddBookScreen(tk.Tk(), self._library).display()

    def open_remove_book_screen(self):
        self._root.destroy()
        RemoveBookScreen(tk.Tk(), self._library).display()

    def open_display_books_screen(self):
        self._root.destroy()
        DisplayBooksScreen(tk.Tk(), self._library).display()

    def open_popular_books_screen(self):
        self._root.destroy()
        PopularBooksScreen(tk.Tk(), self._library).display()

    def logout(self):
        try:
            result = self._library.user_logout()
            if result:
                self._root.destroy()
                LoginScreen(tk.Tk(), self._library).display()
            else:
                messagebox.showerror("Error", "Logout failed. Please try again.")
        except Exception:
            messagebox.showerror("Error", "Logout failed. Please try again.")
            Logger.log_add_message("Logout fail")

    def on_closing(self):
        messagebox.showwarning("Warning", "Please Logout before closing.")



class RegisterScreen(WindowInterface):
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

        register_button = tk.Button(self._root, text="Register",
                                    command=lambda: self.handle_registration(name_entry, username_entry,
                                                                             password_entry))
        register_button.pack(pady=20)
        back_button = tk.Button(self._root, text="Back", command=self.go_back)
        back_button.pack(pady=20)

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the login screen.")

    def handle_registration(self, name_entry, username_entry, password_entry):
        full_name = name_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        result=self._library.user_register(full_name, username, password)
        if not result:
            messagebox.showerror("Error", "Username already registered")
        else:
            messagebox.showinfo("Success", "User registered successfully!")
            self._root.destroy()
            LoginScreen(tk.Tk(), self._library).display()

    def go_back(self):
        self._root.destroy()
        LoginScreen(tk.Tk(), self._library).display()


class SearchScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)
        self._selected_row = None
        self._tree = None
        self._strategy_var = tk.StringVar(value="title")

    def display(self):
        self._root.title("Search Books")
        self._root.geometry("800x650")

        tk.Label(self._root, text="Select Search Strategy:").pack(pady=10)

        tk.Radiobutton(self._root, text="Title", variable=self._strategy_var, value="title").pack(anchor="w")
        tk.Radiobutton(self._root, text="Author", variable=self._strategy_var, value="author").pack(anchor="w")
        tk.Radiobutton(self._root, text="Year", variable=self._strategy_var, value="year").pack(anchor="w")
        tk.Radiobutton(self._root, text="Genre", variable=self._strategy_var, value="genre").pack(anchor="w")

        tk.Label(self._root, text="Enter Search Term:").pack(pady=10)
        search_term_entry = tk.Entry(self._root)
        search_term_entry.pack(pady=5)

        self._tree = ttk.Treeview(self._root, selectmode="browse")
        self._tree.pack(fill="both", expand=True, pady=10)
        self._tree.bind("<<TreeviewSelect>>", self.on_row_select)

        scrollbar = ttk.Scrollbar(self._root, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tk.Button(self._root, text="Search",
                  command=lambda: self.perform_search(self._strategy_var, search_term_entry, self._tree)).pack(pady=10)
        tk.Button(self._root, text="Lend Book", command=self.rent_book).pack(pady=10)
        tk.Button(self._root, text="Return Book", command=self.return_book).pack(pady=10)
        tk.Button(self._root, text="Back", command=self.go_back).pack(pady=10)

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")

    def perform_search(self, strategy_var, search_term_entry, tree):
        strategy = strategy_var.get()
        search_term = search_term_entry.get().strip()

        tree.delete(*tree.get_children())

        results = self._library.search_book(search_term, strategy)

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
            self._selected_row = tree.item(selected_item, "values")

    def rent_book(self):
        if self._selected_row:

            keys = ["title", "author", "is_loaned", "total_books", "genre", "year", "popularity"]
            book_data = {key: value for key, value in zip(keys, self._selected_row)}

            book = self._library.get_book(
                title=book_data["title"],
                author=book_data["author"],
                is_loaned=book_data["is_loaned"],
                total_books=int(book_data["total_books"]),
                genre=book_data["genre"],
                year=int(book_data["year"]),
                popularity=int(book_data["popularity"])
            )

            success = self._library.rent_book(book)

            if success:
                messagebox.showinfo("Success", f"Book '{book_data['title']}' has been rented.")
            else:
                messagebox.showerror("Error", f"Could not rent book '{book_data['title']}'.")
                self.open_add_details_screen(book)

        else:
            messagebox.showerror("Error", "No book selected!")

    def return_book(self):
        if self._selected_row:
            keys = ["title", "author", "is_loaned", "total_books", "genre", "year", "popularity"]
            book_data = {key: value for key, value in zip(keys, self._selected_row)}

            book = self._library.get_book(
                title=book_data["title"],
                author=book_data["author"],
                is_loaned=book_data["is_loaned"],
                total_books=int(book_data["total_books"]),
                genre=book_data["genre"],
                year=int(book_data["year"]),
                popularity=int(book_data["popularity"])
            )

            result = self._library.return_book(book)

            if isinstance(result, str):
                pass
            elif result:
                messagebox.showinfo("Success", f"Book '{book_data['title']}' has been returned successfully.")
            else:
                messagebox.showerror("Error", f"Could not return book '{book_data['title']}'.")

        else:
            messagebox.showerror("Error", "No book selected!")

    def go_back(self):
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def open_add_details_screen(self, book):
        self._root.destroy()
        AddDetailsScreen(tk.Tk(), self._library, book).display()


class AddDetailsScreen(WindowInterface):
    def __init__(self, root, library, book):
        super().__init__(root, library)
        self._selected_book = book

    def display(self):
        self._root.title("Waiting List Entry")
        self._root.geometry("400x200")

        question_label = tk.Label(self._root, text="Do you want to get in waiting list?", font=("Helvetica", 14))
        question_label.pack(pady=20)

        yes_button = tk.Button(self._root, text="Yes", command=self.on_yes)
        yes_button.pack(pady=10)

        no_button = tk.Button(self._root, text="No", command=self.on_no)
        no_button.pack(pady=10)

    def on_yes(self):
        self.show_waiting_list_form()

    def on_no(self):
        self._root.destroy()
        SearchScreen(tk.Tk(), self._library).display()

    def show_waiting_list_form(self):
        self._root.title("Details for waiting list")
        self._root.geometry("400x400")
        for widget in self._root.winfo_children():
            widget.destroy()

        name_label = tk.Label(self._root, text="Enter Your Name:")
        name_label.pack(pady=10)
        name_entry = tk.Entry(self._root)
        name_entry.pack(pady=5)

        phone_label = tk.Label(self._root, text="Enter Your Phone Number (05xxxxxxxx):")
        phone_label.pack(pady=10)
        phone_entry = tk.Entry(self._root)
        phone_entry.pack(pady=5)

        email_label = tk.Label(self._root, text="Enter Your Email Address (name@example...):")
        email_label.pack(pady=10)
        email_entry = tk.Entry(self._root)
        email_entry.pack(pady=5)

        submit_button = tk.Button(self._root, text="Add to Waiting List",
                                  command=lambda: self.add_to_waiting_list(name_entry.get(), phone_entry.get(), email_entry.get()))
        submit_button.pack(pady=20)

        back_button = tk.Button(self._root, text="Back", command=self.go_back)
        back_button.pack(pady=10)

    def add_to_waiting_list(self, name, phone,email):
        if not self.is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number. Must be 10 digits starting with 05.")
            return
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email address.")
            return
        success = self._library.add_to_waiting_list(self._selected_book, name, phone, email)
        if success:
            messagebox.showinfo("Success", f"Successfully added {name} to the waiting list.")
        else:
            messagebox.showerror("Error", "Cannot add to the waiting list.\n Try again later.")

        self._root.destroy()
        SearchScreen(tk.Tk(), self._library).display()

    def is_valid_phone(self, phone):
        return len(phone) == 10 and phone.startswith("05") and phone.isdigit()

    def is_valid_email(self, email):
        if email.count("@")>1 or email.count("@")==0:
            return False
        local, domain = email.split("@")
        if ".." in domain:
            return False
        if ".co.il" in local or ".ac" in local or ".com" in local:
            return False
        return ".co.il" in domain or ".ac" in domain or ".com" in domain

    def go_back(self):
        self._root.destroy()
        SearchScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")


class AddBookScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)
        self.selected_row = None

    def display(self):

        self._root.title("Add Book to Library")
        self._root.geometry("350x400")

        self._title_label = tk.Label(self._root, text="Book Title:")
        self._title_label.grid(row=0, column=0, padx=10, pady=10)
        self._title_entry = tk.Entry(self._root)
        self._title_entry.grid(row=0, column=1, padx=10, pady=10)

        self._author_label = tk.Label(self._root, text="Author:")
        self._author_label.grid(row=1, column=0, padx=10, pady=10)
        self._author_entry = tk.Entry(self._root)
        self._author_entry.grid(row=1, column=1, padx=10, pady=10)

        self._copies_label = tk.Label(self._root, text="Copies:")
        self._copies_label.grid(row=2, column=0, padx=10, pady=10)
        self._copies_entry = tk.Entry(self._root)
        self._copies_entry.grid(row=2, column=1, padx=10, pady=10)

        self._category_label = tk.Label(self._root, text="Genre:")
        self._category_label.grid(row=3, column=0, padx=10, pady=10)
        self._category_combobox = ttk.Combobox(self._root, values=[category.value for category in self._library.get_books_category()])
        self._category_combobox.grid(row=3, column=1, padx=10, pady=10)

        self._year_label = tk.Label(self._root, text="Year:")
        self._year_label.grid(row=4, column=0, padx=10, pady=10)
        self._year_entry = tk.Entry(self._root)
        self._year_entry.grid(row=4, column=1, padx=10, pady=10)

        self._add_button = tk.Button(self._root, text="Add Book", command=self.add_book)
        self._add_button.grid(row=5, column=0, columnspan=2, pady=20)

        self._back_button = tk.Button(self._root, text="Back", command=self.go_back)
        self._back_button.grid(row=6, column=0, columnspan=2, pady=20)

    def add_book(self):
        title = self._title_entry.get()
        author = self._author_entry.get()
        copies = self._copies_entry.get()
        category = self._category_combobox.get()
        year = self._year_entry.get()

        if not title or not author or not copies or not category or not year:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try:
            copies = int(copies)
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Copies and Year must be integers!")
            return

        success = self._library.add_item("Book", title, author, copies, category, year)

        if success:
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.clear_fields()
        else:
            messagebox.showwarning("Warning", f"Book '{title}' already exists. Copies updated.")

    def clear_fields(self):
        self._title_entry.delete(0, tk.END)
        self._author_entry.delete(0, tk.END)
        self._copies_entry.delete(0, tk.END)
        self._category_combobox.set('')
        self._year_entry.delete(0, tk.END)

    def go_back(self):
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")


class RemoveBookScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)
        self.selected_row = None

    def display(self):
        self._root.title("Remove Book from Library")
        self._root.geometry("350x350")

        self._title_label = tk.Label(self._root, text="Book Title:")
        self._title_label.grid(row=0, column=0, padx=10, pady=10)
        self._title_entry = tk.Entry(self._root)
        self._title_entry.grid(row=0, column=1, padx=10, pady=10)

        self._author_label = tk.Label(self._root, text="Author:")
        self._author_label.grid(row=1, column=0, padx=10, pady=10)
        self._author_entry = tk.Entry(self._root)
        self._author_entry.grid(row=1, column=1, padx=10, pady=10)

        self._category_label = tk.Label(self._root, text="Genre:")
        self._category_label.grid(row=2, column=0, padx=10, pady=10)
        self._category_combobox = ttk.Combobox(self._root, values=[category.value for category in self._library.get_books_category()])
        self._category_combobox.grid(row=2, column=1, padx=10, pady=10)

        self._year_label = tk.Label(self._root, text="Year:")
        self._year_label.grid(row=3, column=0, padx=10, pady=10)
        self._year_entry = tk.Entry(self._root)
        self._year_entry.grid(row=3, column=1, padx=10, pady=10)

        self._add_button = tk.Button(self._root, text="Remove Book", command=self.remove_book)
        self._add_button.grid(row=4, column=0, columnspan=2, pady=20)

        self._back_button = tk.Button(self._root, text="Back", command=self.go_back)
        self._back_button.grid(row=5, column=0, columnspan=2, pady=20)

    def remove_book(self):
        ans = False
        title = self._title_entry.get()
        author = self._author_entry.get()
        category = self._category_combobox.get()
        year = self._year_entry.get()

        if not title or not author or not category or not year:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Error", "Year must be integer!")
            return

        try:
            main_lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "main_lib"))
            file_path = os.path.join(main_lib_path, "Excel_Tables", "books.csv")
            df = pd.read_csv(file_path)

            matching_books = df[(df['title'] == title) & (df['author'] == author) &
                                (df['genre'] == category) & (df['year'] == year)]

            if matching_books.empty:
                messagebox.showerror("Error", "Book not found!")
                return

            book_data = matching_books.iloc[0].to_dict()

            book = self._library.get_book(
                title=book_data['title'],
                is_loaned=book_data['is_loaned'],
                author=book_data['author'],
                total_books=book_data["copies"],
                genre=book_data['genre'],
                year=book_data['year'],
                popularity=book_data['popularity']
            )

            try:
                ans = self._library.delete_book(book)
            except Exception as e:
                messagebox.showerror("Error", f"Book could not be deleted!")
                return

            if ans:
                messagebox.showinfo("Success", f"Book '{book_data['title']}' has been deleted.")
                self.clear_fields()
                return
            else:
                messagebox.showerror("Error", "Book could not be deleted!")
                return

        except FileNotFoundError:
            messagebox.showerror("Error", "Books database file not found!")
            return
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return

    def clear_fields(self):
        self._title_entry.delete(0, tk.END)
        self._author_entry.delete(0, tk.END)
        self._category_combobox.set('')
        self._year_entry.delete(0, tk.END)

    def go_back(self):
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")


class DisplayBooksScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)
        self._genre_label = None
        self._genre_combobox = None
        self._tree = None

    def display(self):
        self._root.title("Display Books")
        self._root.geometry("800x600")

        # Create top frame for controls
        control_frame = tk.Frame(self._root)
        control_frame.pack(fill="x", padx=10, pady=10)

        # Dropdown for selecting display option
        self._option_label = tk.Label(control_frame, text="Select Category:")
        self._option_label.pack(pady=5)

        self._options = ["All Books", "Available Books", "Not Available Books", "Popular Books", "Genre"]
        self._option_combobox = ttk.Combobox(control_frame, values=self._options, state="readonly")
        self._option_combobox.pack(pady=5)
        self._option_combobox.set(self._options[0])  # Default selection
        self._option_combobox.bind("<<ComboboxSelected>>", self.toggle_genre_selection)

        # Genre selection (hidden by default)
        self._genre_label = tk.Label(control_frame, text="Select Genre:")
        self._genre_combobox = ttk.Combobox(control_frame,
                                            values=[category.value for category in self._library.get_books_category()])
        # Button to fetch and display books
        self._display_button = tk.Button(control_frame, text="Display Books", command=self.display_books)
        self._display_button.pack(pady=10)

        # Treeview for displaying books in table format
        self._tree = ttk.Treeview(self._root, selectmode="browse")
        self._tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self._root, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Back button
        self._back_button = tk.Button(self._root, text="Back", command=self.go_back)
        self._back_button.pack(pady=10)

    def toggle_genre_selection(self, event):
        current_option = self._option_combobox.get()

        if current_option == "Genre":
            self._display_button.pack_forget()
            self._genre_label.pack(pady=5)
            self._genre_combobox.pack(pady=5)
            self._display_button.pack(pady=10)
        elif self._genre_label.winfo_ismapped():
            self._genre_label.pack_forget()
            self._genre_combobox.pack_forget()

    def go_back(self):
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def display_books(self):
        """Display books based on the selected category."""
        self._tree.delete(*self._tree.get_children())  # Clear the treeview before displaying new results

        option = self._option_combobox.get()

        try:
            if option == "All Books":
                books = self._library.display_all_books()
            elif option == "Available Books":
                books = self._library.display_available_books()
            elif option == "Not Available Books":
                books = self._library.display_not_available_books()
            elif option == "Popular Books":
                books = self._library.display_popular_books()
            elif option == "Genre":
                genre = self._genre_combobox.get()
                if not genre:
                    messagebox.showerror("Error", "Please select a genre.")
                    return
                books = self._library.display_genre(genre)
            else:
                raise ValueError("Invalid option selected.")

            if books:
                # Define columns based on the book dictionary keys
                self._tree["columns"] = list(books[0].keys())
                self._tree["show"] = "headings"

                # Create headings for each column
                for col in books[0].keys():
                    self._tree.heading(col, text=col)
                    self._tree.column(col, width=150)

                # Insert book details into the Treeview
                for index, book in enumerate(books):
                    self._tree.insert("", "end", iid=index, values=list(book.values()))
            else:
                messagebox.showinfo("No Results", "No books found for the selected category.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")


class PopularBooksScreen(WindowInterface):
    def __init__(self, root, library):
        super().__init__(root, library)
        self._tree = None

    def display(self):
        self._root.title("Display Popular Books")
        self._root.geometry("1050x300")

        # Treeview for displaying books in table format
        self._tree = ttk.Treeview(self._root, selectmode="browse")
        self._tree.pack(fill="both", expand=True, pady=10)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self._root, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._back_button = tk.Button(self._root, text="Back", command=self.go_back)
        self._back_button.pack(pady=20)

        self.display_books()

    def display_books(self):
        books = self._library.display_popular_books()
        try:
            if books:
                # Define columns based on the book dictionary keys
                self._tree["columns"] = list(books[0].keys())
                self._tree["show"] = "headings"

                # Create headings for each column
                for col in books[0].keys():
                    self._tree.heading(col, text=col)
                    self._tree.column(col, width=150)

                # Insert book details into the Treeview
                for index, book in enumerate(books):
                    self._tree.insert("", "end", iid=index, values=list(book.values()))
            else:
                messagebox.showinfo("No Results", "No books found for the selected category.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def go_back(self):
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")


if __name__ == '__main__':
    library = Library.get_instance()
    root = tk.Tk()
    LoginScreen(root, library).display()
    root.mainloop()
