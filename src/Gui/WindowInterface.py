from tkinter import messagebox

class WindowInterface:
    """
    This is an abstract class that represents the windows interface
    handles with closing windows and centerized them.
    """
    def __init__(self, root, library):
        from src.Gui.LogginScreen import LoginScreen
        from src.Gui.RegisterScreen import RegisterScreen
        self._root = root
        self._library = library
        self.center_window()
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        if not isinstance(self, (LoginScreen, RegisterScreen)) and not self._library.check_login():
            messagebox.showerror("Error", "Login needed to be for open the system")
            self._root.destroy()

    def display(self):
        """
        This method is a display all the enters and the buttons of the windows.
        in each child this method implemented differently
        :return:
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def on_closing(self):
        from src.Gui.LogginScreen import LoginScreen
        """
        prevent closing of the window
        """
        if isinstance(self, LoginScreen):
            self._root.destroy()
        else:
            messagebox.showwarning("Warning", "Please use the proper logout button to exit.")

    def center_window(self):
        """
        Centers the window on the screen.
        """
        self._root.update_idletasks()

        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()

        window_width = self._root.winfo_width()
        window_height = self._root.winfo_height()

        x = int((screen_width / 2.5) - (window_width // 2))
        y = int((screen_height / 4.5) - (window_height // 2))

        self._root.geometry(f'+{x}+{y}')

