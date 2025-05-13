""" Main entry point for the application. """
import tkinter as tk
# pylint: disable=import-error
from p_to_md.ui import Gui

if __name__ == "__main__":
    root : tk.Tk = Gui()
    root.mainloop() # Start the Tkinter main loop
