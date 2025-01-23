import tkinter as tk
from src.Gui.LogginScreen import LoginScreen
from src.main_lib.Library import Library

class GUIActivating():
    def __init__(self):
        self.library = Library.get_instance()
        self.root = tk.Tk()
        LoginScreen(self.root, self.library).display()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    """
    in this method we starting the login screen
    the other window will close instantly if there is a trying to open them without log in 
    the only 2 windows can be open without log in is the log in screen and register screen.
    """
    gui = GUIActivating()
    gui.run()
