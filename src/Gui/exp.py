
'''
Not relevant
'''

# import tkinter as tk
# from tkinter import messagebox
# from src.main_lib.Users import User
# from src.main_lib.Library import Library
# from src.main_lib.Books import Books
#
#
# class GuiForLibrary:
#
#     def __init__(self):
#         self.library = Library.get_instance()
#         self.current_user = None
#
#     def login(self, role_var, username_entry, password_entry):
#         role = role_var.get()
#         username = username_entry.get().strip()
#         password = password_entry.get().strip()
#
#         users = User.get_all_users()
#         user = next((u for u in users if u.get_username() == username and u.get_role() == role), None)
#
#         if user is None:
#             messagebox.showerror("Error", "User not found")
#             return
#
#         if user.check_password(password):
#             self.current_user = user
#             messagebox.showinfo("Welcome", f"Welcome, {user.get_name()}!")
#             self.show_role_based_view(role)
#         else:
#             messagebox.showerror("Error", "Password is incorrect")
#
#     def show_role_based_view(self, role):
#         if role == "librarian":
#             self.show_librarian_view()
#         elif role == "student":
#             self.show_student_view()
#
#     def show_librarian_view(self):
#         librarian_window = tk.Toplevel()
#         librarian_window.title("Librarian Dashboard")
#
#         tk.Label(librarian_window, text="Librarian Dashboard", font=("Arial", 16)).pack(pady=10)
#
#         # Add Book Section
#         tk.Label(librarian_window, text="Add a New Book").pack(pady=5)
#         title_entry = tk.Entry(librarian_window, width=30)
#         title_entry.insert(0, "Title")
#         title_entry.pack(pady=2)
#
#         author_entry = tk.Entry(librarian_window, width=30)
#         author_entry.insert(0, "Author")
#         author_entry.pack(pady=2)
#
#         year_entry = tk.Entry(librarian_window, width=30)
#         year_entry.insert(0, "Year")
#         year_entry.pack(pady=2)
#
#         copies_entry = tk.Entry(librarian_window, width=30)
#         copies_entry.insert(0, "Copies")
#         copies_entry.pack(pady=2)
#
#         genre_entry = tk.Entry(librarian_window, width=30)
#         genre_entry.insert(0, "Genre")
#         genre_entry.pack(pady=2)
#
#         add_book_button = tk.Button(
#             librarian_window,
#             text="Add Book",
#             command=lambda: self.library.add_book(
#                 title_entry.get(),
#                 author_entry.get(),
#                 "No",  # Default value for `is_loaned`
#                 copies_entry.get(),
#                 genre_entry.get(),
#                 year_entry.get()
#             )
#         )
#         add_book_button.pack(pady=10)
#
#         # View Books Button
#         tk.Button(
#             librarian_window,
#             text="View Available Books",
#             command=self.view_books,
#         ).pack(pady=5)
#
#     def show_student_view(self):
#         student_window = tk.Toplevel()
#         student_window.title("Student Dashboard")
#
#         tk.Label(student_window, text="Available Books", font=("Arial", 16)).pack(pady=10)
#
#         # Display available books
#         books = self.library.get_books()
#         for book in books:
#             tk.Label(student_window, text=str(book)).pack()
#
#     def view_books(self):
#         books_window = tk.Toplevel()
#         books_window.title("Available Books")
#
#         tk.Label(books_window, text="Available Books", font=("Arial", 16)).pack(pady=10)
#
#         books = self.library.get_books()
#         for book in books:
#             tk.Label(books_window, text=str(book)).pack()
#
#     def start(self):
#         root = tk.Tk()
#         root.title("Library System Login")
#
#         # Create variables
#         role_var = tk.StringVar(value="student")
#
#         # Title
#         tk.Label(root, text="Login to Library System", font=("Arial", 16)).pack(pady=15)
#
#         # Role selection
#         tk.Label(root, text="Choose your role").pack(pady=10)
#         tk.Radiobutton(root, text="Student", variable=role_var, value="student").pack()
#         tk.Radiobutton(root, text="Librarian", variable=role_var, value="librarian").pack()
#
#         # Username and Password Inputs
#         tk.Label(root, text="Username:").pack(pady=10)
#         username_entry = tk.Entry(root)
#         username_entry.pack()
#
#         tk.Label(root, text="Password:").pack(pady=10)
#         password_entry = tk.Entry(root, show="*")
#         password_entry.pack()
#
#         # Login Button
#         tk.Button(
#             root, text="Login", command=lambda: self.login(role_var, username_entry, password_entry)
#         ).pack(pady=20)
#
#         root.mainloop()
#
#
# if __name__ == "__main__":
#     # Initialize Library and Add Sample Users
#     lib = Library.get_instance()
#     lib.add_user("Itay Segev", "itay", "student", "it")
#     lib.add_user("Admin Librarian", "admin", "librarian", "1234")
#
#     GuiForLibrary().start()
