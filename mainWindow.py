import tkinter as tk

class MainWindow:
    def __init__(self, open_registerWindow):
        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("Tela principal")

        # Create a menu
        self.menuBar = tk.Menu(self.window)

        # Archives menu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Novo")
        self.fileMenu.add_command(label='Abrir')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Sair')
        self.menuBar.add_cascade(label='Arquivo', menu=self.fileMenu)

        # Help menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="Sobre")
        self.menuBar.add_cascade(label='Ajuda', menu=self.helpMenu)

        # Users menu
        self.usersMenu = tk.Menu(self.menuBar, tearoff=0)
        self.usersMenu.add_command(label="Cadastrar", command=open_registerWindow)
        self.menuBar.add_cascade(label="Usuários", menu=self.usersMenu)

        self.window.config(menu=self.menuBar)
