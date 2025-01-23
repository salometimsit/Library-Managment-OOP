
import tkinter as tk
from tkinter import messagebox

from src.Gui.WindowInterface import WindowInterface


class AddDetailsScreen(WindowInterface):
    """
    This class handles with getting all the client details for the waiting list
    """
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
        from src.Gui.SearchScreen import SearchScreen
        self._root.destroy()
        SearchScreen(tk.Tk(), self._library).display()

    def show_waiting_list_form(self):
        """
        a window that collecting all the details for the waiting list
        :return:
        """
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
                                  command=lambda:self.add_to_waiting_list(name_entry.get(), phone_entry.get(), email_entry.get()))
        submit_button.pack(pady=20)

        back_button = tk.Button(self._root, text="Back", command=self.go_back)
        back_button.pack(pady=10)

    def add_to_waiting_list(self, name, phone, email):
        from src.Gui.SearchScreen import SearchScreen
        """
        adding to the waiting list
        """
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
        """
        check if entered phone number is valid
        """
        return len(phone) == 10 and phone.startswith("05") and phone.isdigit()

    def is_valid_email(self, email):
        """
        check if entered email is valid
        """
        if email.count("@") > 1 or email.count("@") == 0:
            return False
        local, domain = email.split("@")
        if ".." in domain:
            return False
        if ".co.il" in local or ".ac" in local or ".com" in local:
            return False
        return ".co.il" in domain or ".ac" in domain or ".com" in domain

    def go_back(self):
        from src.Gui.SearchScreen import SearchScreen
        self._root.destroy()
        SearchScreen(tk.Tk(), self._library).display()

    def on_closing(self):
        messagebox.showwarning("Warning", "Please use the back button to return to the main screen.")
