import tkinter as tk
from tkinter import ttk


class ConfigWindow:
    def __init__(self):
        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry('600x300')
        self.window.title("Configurações")

        # Create notebook widget
        self.notebook = ttk.Notebook(self.window)
        # Create an individual tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        # Add tabs to notebook
        self.notebook.add(self.tab1, text='Aba 1')
        self.notebook.add(self.tab2, text='Aba 2')
        self.notebook.add(self.tab3, text='Aba 3')

        self.notebook.pack(expand=True, fill="both")


config = ConfigWindow()
config.window.mainloop()
