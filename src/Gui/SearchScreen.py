
import tkinter as tk
from tkinter import ttk, messagebox

from src.Gui.WindowInterface import WindowInterface


class SearchScreen(WindowInterface):
    """
    This class handles with all the user searching books,.
    it displayed by trees, for the user can choose a book and choose if he want to lend or return it.
    """
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
        """
        here the search is performed.

        """
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
        """
        here we are taking the selected row from the tree if there is one
        :param event:
        :return:
        """
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            self._selected_row = tree.item(selected_item, "values")

    def rent_book(self):
        """
        checking if there is selected book, and then activate the library method that handle with renting
        if the rent wasn't successfully it opens the screen for putting details
        :return:
        """
        if self._selected_row:

            keys = ["title", "author", "is_loaned", "total_books", "genre", "year", "popularity"]
            book_data = {key: value for key, value in zip(keys, self._selected_row)}

            book = self._library.get_book(title=book_data["title"], author=book_data["author"],
                                          is_loaned=book_data["is_loaned"], total_books=int(book_data["total_books"]),
                                          genre=book_data["genre"], year=int(book_data["year"]),
                                          popularity=int(book_data["popularity"]))

            success = self._library.rent_book(book)

            if success:
                messagebox.showinfo("Success", f"Book '{book_data['title']}' has been rented.")
            else:
                messagebox.showerror("Error", f"Could not rent book '{book_data['title']}'.")
                self.open_add_details_screen(book)

        else:
            messagebox.showerror("Error", "No book selected!")

    def return_book(self):
        """
        checking if there is selected book, and then activate the library method that handle with renting

        :return:
        """
        if self._selected_row:
            keys = ["title", "author", "is_loaned", "total_books", "genre", "year", "popularity"]
            book_data = {key: value for key, value in zip(keys, self._selected_row)}

            book = self._library.get_book(title=book_data["title"], author=book_data["author"],
                                          is_loaned=book_data["is_loaned"], total_books=int(book_data["total_books"]),
                                          genre=book_data["genre"], year=int(book_data["year"]),
                                          popularity=int(book_data["popularity"]))

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
        from src.Gui.MainScreen import MainScreen
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def open_add_details_screen(self, book):
        from src.Gui.AddDeatailsScreen import AddDetailsScreen
        self._root.destroy()
        AddDetailsScreen(tk.Tk(), self._library, book).display()

