
'''
Not relevant
'''

# import tkinter as tk
# from tkinter import ttk, messagebox
# from BooksCategory import BooksCategory
# from src.main_lib.Library import Library
# from src.main_lib.Users import User
#
#
# class LibraryGUI:
#     def __init__(self, root, library):
#         self.root = root
#         self.library = library
#         self.current_user = None
#
#         # Title and window size
#         root.title("Library Management System")
#         root.geometry("600x400")
#
#         self.show_login_window()
#
#     def show_login_window(self):
#         """Window for login and registration."""
#         login_window = tk.Toplevel(self.root)
#         login_window.title("Login")
#         login_window.geometry("400x300")
#
#         ttk.Label(login_window, text="Username:").pack(pady=5)
#         username_entry = ttk.Entry(login_window)
#         username_entry.pack(pady=5)
#
#         ttk.Label(login_window, text="Password:").pack(pady=5)
#         password_entry = ttk.Entry(login_window, show="*")
#         password_entry.pack(pady=5)
#
#         def login():
#             username = username_entry.get()
#             password = password_entry.get()
#             if not (username and password):
#                 messagebox.showerror("Error", "Please fill all fields.")
#                 return
#
#             try:
#
#                 users=User.get_all_users()
#                 for us in users:
#                     if us.username == username and us.check_password(password):
#                         user = self.library.authenticate_user(username, password)
#                     else:
#                         user=None
#                 if user:
#                     self.current_user = user
#                     messagebox.showinfo("Success", f"Welcome, {user.get_name()}!")
#                     login_window.destroy()
#                     self.show_main_menu()
#                 else:
#                     messagebox.showerror("Error", "Invalid username or password.")
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))
#
#         def register():
#             username = username_entry.get()
#             password = password_entry.get()
#             if not (username and password):
#                 messagebox.showerror("Error", "Please fill all fields.")
#                 return
#
#             try:
#                 self.library.register_user(username, password, role="Librarian")
#                 messagebox.showinfo("Success", "Registration successful! Please log in.")
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))
#
#         ttk.Button(login_window, text="Login", command=login).pack(pady=10)
#         ttk.Button(login_window, text="Register", command=register).pack(pady=5)
#
#     def show_main_menu(self):
#         """Main menu after login."""
#         ttk.Label(self.root, text="Library Management System", font=("Arial", 16)).pack(pady=10)
#
#         ttk.Button(self.root, text="Add Book", command=self.add_book_window).pack(pady=5)
#         ttk.Button(self.root, text="Lend Book", command=self.lend_book_window).pack(pady=5)
#         ttk.Button(self.root, text="View Books", command=self.view_books_window).pack(pady=5)
#         ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)
#
#     def add_book_window(self):
#         """Window to add a new book."""
#         add_window = tk.Toplevel(self.root)
#         add_window.title("Add Book")
#         add_window.geometry("400x400")
#
#         # Labels and inputs
#         ttk.Label(add_window, text="Title:").pack(pady=5)
#         title_entry = ttk.Entry(add_window)
#         title_entry.pack(pady=5)
#
#         ttk.Label(add_window, text="Author:").pack(pady=5)
#         author_entry = ttk.Entry(add_window)
#         author_entry.pack(pady=5)
#
#         ttk.Label(add_window, text="Category:").pack(pady=5)
#         categories = [category.value for category in BooksCategory]
#         category_combobox = ttk.Combobox(add_window, values=categories)
#         category_combobox.pack(pady=5)
#
#         ttk.Label(add_window, text="Year:").pack(pady=5)
#         year_entry = ttk.Entry(add_window)
#         year_entry.pack(pady=5)
#
#         ttk.Label(add_window, text="Total Copies:").pack(pady=5)
#         copies_entry = ttk.Entry(add_window)
#         copies_entry.pack(pady=5)
#
#         def submit_book():
#             title = title_entry.get()
#             author = author_entry.get()
#             category = category_combobox.get()
#             year = year_entry.get()
#             copies = copies_entry.get()
#
#             if not (title and author and category and year.isdigit() and copies.isdigit()):
#                 messagebox.showerror("Error", "Please fill all fields correctly.")
#                 return
#
#             try:
#                 self.library.add_book(title, author, category, int(year), int(copies))
#                 messagebox.showinfo("Success", f"Book '{title}' added successfully!")
#                 add_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))
#
#         ttk.Button(add_window, text="Add Book", command=submit_book).pack(pady=10)
#
#     def lend_book_window(self):
#         """Window to lend a book."""
#         lend_window = tk.Toplevel(self.root)
#         lend_window.title("Lend Book")
#         lend_window.geometry("400x200")
#
#         ttk.Label(lend_window, text="Title:").pack(pady=5)
#         title_entry = ttk.Entry(lend_window)
#         title_entry.pack(pady=5)
#
#         def lend_book():
#             title = title_entry.get()
#             if not title:
#                 messagebox.showerror("Error", "Please enter a book title.")
#                 return
#
#             try:
#                 self.library.lend_book(title, self.current_user)
#                 messagebox.showinfo("Success", f"Book '{title}' lent successfully!")
#                 lend_window.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", str(e))
#
#         ttk.Button(lend_window, text="Lend Book", command=lend_book).pack(pady=10)
#
#     def view_books_window(self):
#         """Window to view all books."""
#         view_window = tk.Toplevel(self.root)
#         view_window.title("View Books")
#         view_window.geometry("600x400")
#
#         books = self.library.get_all_books()
#         if not books:
#             ttk.Label(view_window, text="No books available.").pack(pady=10)
#             return
#
#         tree = ttk.Treeview(view_window, columns=("Title", "Author", "Category", "Year", "Copies"), show="headings")
#         tree.heading("Title", text="Title")
#         tree.heading("Author", text="Author")
#         tree.heading("Category", text="Category")
#         tree.heading("Year", text="Year")
#         tree.heading("Copies", text="Copies")
#
#         for book in books:
#             tree.insert("", "end", values=(book.get_title(), book.get_author(), book.get_genre(),
#                                            book.get_year(), book.get_total_books()))
#         tree.pack(fill="both", expand=True)
#
#     def logout(self):
#         """Logout the current user."""
#         self.current_user = None
#         self.root.destroy()
#         self.root = tk.Tk()
#         self.show_login_window()
#
# if __name__ == '__main__':
#     if __name__ == '__main__':
#         root = tk.Tk()
#         library = Library.get_instance()
#         g = LibraryGUI(root, library)
#         root.mainloop()
