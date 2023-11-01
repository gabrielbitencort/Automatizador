import os
import tkinter as tk
from tkinter import filedialog


class MainWindow:
    def __init__(self, open_registerWindow):
        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("Tela principal")

        # List to save recent files
        self.recent_files = []

        # Create a menu
        self.menuBar = tk.Menu(self.window)

        # Archives menu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Novo")
        self.fileMenu.add_command(label='Abrir...', command=self.open_file)
        self.recent_submenu = tk.Menu(self.fileMenu, tearoff=0)
        self.fileMenu.add_cascade(label='Abrir recentes', menu=self.recent_submenu)
        self.fileMenu.add_command(label='Fechar')
        self.fileMenu.add_command(label='Salvar')
        self.fileMenu.add_command(label='Salvar como...')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Configurações')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Avançado')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Sair')
        self.menuBar.add_cascade(label='Arquivo', menu=self.fileMenu)

        # Users menu
        self.usersMenu = tk.Menu(self.menuBar, tearoff=0)
        self.usersMenu.add_command(label="Cadastrar", command=open_registerWindow)
        self.menuBar.add_cascade(label="Usuários", menu=self.usersMenu)

        # Help menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="Sobre")
        self.menuBar.add_cascade(label='Ajuda', menu=self.helpMenu)

        self.window.config(menu=self.menuBar)

        self.file_label = tk.Label(self.window, text='')
        self.file_label.pack()

        self.center_window(600, 500)

    # Open files
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=f"Arquivo selecionado: {file_path}")
            self.add_to_recent(file_path)
            self.update_recent_submenu()

    # Add the recent file to recent files list
    def add_to_recent(self, file_path):
        if file_path not in self.recent_files:
            self.recent_files.append(file_path)

    # Update the recent files submenu
    def update_recent_submenu(self):
        self.recent_submenu.delete(0, tk.END)
        for index, file_path in enumerate(self.recent_files):
            base_name = os.path.basename(file_path)
            self.recent_submenu.add_command(label=base_name,
                                            command=lambda path=file_path: self.open_recent(path))

    # Open recent files
    def open_recent(self, file_path):
        self.file_label.config(text=f'Arquivo recente: {file_path}')

    # Centralize the window
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
