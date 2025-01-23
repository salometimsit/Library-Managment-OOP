
import tkinter as tk
from tkinter import ttk, messagebox

from src.Gui.WindowInterface import WindowInterface


class AddBookScreen(WindowInterface):
    """
    This class handles the adding book.
    """
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
        self._category_combobox = ttk.Combobox(self._root, values=[category.value for category in
                                                                   self._library.get_books_category()])
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
        """
        trying to add book to the library, checking if all th fields are field and valid
        and trying to add the book to the library.
        """
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
            messagebox.showwarning("Warning", f"Book '{title}' Cannot be added!\ncheck if copies updated")

    def clear_fields(self):
        """
        clear all the fields in the window
        """
        self._title_entry.delete(0, tk.END)
        self._author_entry.delete(0, tk.END)
        self._copies_entry.delete(0, tk.END)
        self._category_combobox.set('')
        self._year_entry.delete(0, tk.END)

    def go_back(self):
        from src.Gui.MainScreen import MainScreen
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")

