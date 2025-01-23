
import tkinter as tk
from tkinter import ttk, messagebox

from src.Gui.WindowInterface import WindowInterface


class DisplayBooksScreen(WindowInterface):
    """
    This class handles the displaying books from library in 4 categories:.
    All books
    Available books
    loaned books
    Popular books
    By specific genre
    """
    def __init__(self, root, library):
        super().__init__(root, library)
        self._genre_label = None
        self._genre_combobox = None
        self._tree = None

    def display(self):
        self._root.title("Display Books")
        self._root.geometry("800x600")

        control_frame = tk.Frame(self._root)
        control_frame.pack(fill="x", padx=10, pady=10)

        self._option_label = tk.Label(control_frame, text="Select Category:")
        self._option_label.pack(pady=5)

        self._options = ["All Books", "Available Books", "Not Available Books", "Popular Books", "Genre"]
        self._option_combobox = ttk.Combobox(control_frame, values=self._options, state="readonly")
        self._option_combobox.pack(pady=5)
        self._option_combobox.set(self._options[0])  # Default selection
        self._option_combobox.bind("<<ComboboxSelected>>", self.switch_genre_selection)

        self._genre_label = tk.Label(control_frame, text="Select Genre:")
        self._genre_combobox = ttk.Combobox(control_frame,
                                            values=[category.value for category in self._library.get_books_category()])
        self._display_button = tk.Button(control_frame, text="Display Books", command=self.display_books)
        self._display_button.pack(pady=10)

        self._tree = ttk.Treeview(self._root, selectmode="browse")
        self._tree.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self._root, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._back_button = tk.Button(self._root, text="Back", command=self.go_back)
        self._back_button.pack(pady=10)

    def switch_genre_selection(self, event):
        """
        handling with the genre button
        """
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
        from src.Gui.MainScreen import MainScreen
        self._root.destroy()
        MainScreen(tk.Tk(), self._library).display()

    def display_books(self):
        """
        display books based on the selected category.
        """
        self._tree.delete(*self._tree.get_children())

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

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")
