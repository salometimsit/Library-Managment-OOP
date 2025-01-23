import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from src.Gui.WindowInterface import WindowInterface


class RemoveBookScreen(WindowInterface):
    """
    This class handles the removing book from library.
    """
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
        self._category_combobox = ttk.Combobox(self._root, values=[category.value for category in
                                                                   self._library.get_books_category()])
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
        """
        trying to remove book from the library, checking if all th fields are field and valid
        and trying to remove the book from the library.
        """
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

            book = self._library.get_book(title=book_data["title"], author=book_data["author"],
                                          is_loaned=book_data["is_loaned"], total_books=int(book_data["copies"]),
                                          genre=book_data["genre"], year=int(book_data["year"]),
                                          popularity=int(book_data["popularity"]))

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
        """
        clear all the fields in the window
        """
        self._title_entry.delete(0, tk.END)
        self._author_entry.delete(0, tk.END)
        self._category_combobox.set('')
        self._year_entry.delete(0, tk.END)

    def go_back(self):
        from src.Gui.MainScreen import MainScreen
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")
