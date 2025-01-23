
import tkinter as tk
from tkinter import messagebox

from src.Gui.WindowInterface import WindowInterface


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

##########################################################################################
    """
    open all different screens
    """
    def open_search_screen(self):
        from src.Gui.SearchScreen import SearchScreen
        self._root.destroy()
        SearchScreen(tk.Tk(), self._library).display()

    def open_add_book_screen(self):
        from src.Gui.AddBookScreen import AddBookScreen
        self._root.destroy()
        AddBookScreen(tk.Tk(), self._library).display()

    def open_remove_book_screen(self):
        from src.Gui.RemoveBookScreen import RemoveBookScreen
        self._root.destroy()
        RemoveBookScreen(tk.Tk(), self._library).display()

    def open_display_books_screen(self):
        from src.Gui.DisplayBookScreen import DisplayBooksScreen
        self._root.destroy()
        DisplayBooksScreen(tk.Tk(), self._library).display()

    def open_popular_books_screen(self):
        from src.Gui.PopularBooksScreen import PopularBooksScreen
        self._root.destroy()
        PopularBooksScreen(tk.Tk(), self._library).display()

#############################################################################################################

    def logout(self):
        from src.Gui.LogginScreen import LoginScreen
        """
        in this button the user is logged out.
        and this is the only way for closing the library system.
        :return:
        """
        try:
            result = self._library.user_logout()
            if result:
                self._root.destroy()
                LoginScreen(tk.Tk(), self._library).display()
            else:
                messagebox.showerror("Error", "Logout failed. Please try again.")
        except Exception:
            messagebox.showerror("Error", "Logout failed. Please try again.")

    def on_closing(self):
        messagebox.showwarning("Warning", "Please Logout before closing.")
