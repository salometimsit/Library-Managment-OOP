
import tkinter as tk
from tkinter import ttk, messagebox

from src.Gui.WindowInterface import WindowInterface


class PopularBooksScreen(WindowInterface):
    """
    This class handles the popular books screen.
    in this screen all the popular books of the library shown
    """
    def __init__(self, root, library):
        super().__init__(root, library)
        self._tree = None

    def display(self):
        self._root.title("Display Popular Books")
        self._root.geometry("1050x300")

        self._tree = ttk.Treeview(self._root, selectmode="browse")
        self._tree.pack(fill="both", expand=True, pady=10)

        scrollbar = ttk.Scrollbar(self._root, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._back_button = tk.Button(self._root, text="Back", command=self.go_back)
        self._back_button.pack(pady=20)

        self.display_books()

    def display_books(self):
        """
        in this method we display the popular books of the library
        :return:
        """
        books = self._library.display_popular_books()
        try:
            if books:
                self._tree["columns"] = list(books[0].keys())
                self._tree["show"] = "headings"

                for col in books[0].keys():
                    self._tree.heading(col, text=col)
                    self._tree.column(col, width=150)

                for index, book in enumerate(books):
                    self._tree.insert("", "end", iid=index, values=list(book.values()))
            else:
                messagebox.showinfo("No Results", "No books found for the selected category.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def go_back(self):
        from src.Gui.MainScreen import MainScreen
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")