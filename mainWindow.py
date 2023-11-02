import os
import platform
import tkinter as tk
from tkinter import filedialog


class MainWindow:
    def __init__(self, open_registerWindow):
        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title("Tela principal")

        #   Maximize window if sytem is windows
        if platform.system() == "Windows":
            self.window.state("zoomed")
        else:
            # Maximize window in other systems
            self.window.attributes('-zoomed', 1)

        # List to save recent files
        self.recent_files = []

        # Current file name
        self.current_file = None

        # Create a menu
        self.menuBar = tk.Menu(self.window)

        # Archives menu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Novo", command=self.new_file)
        self.fileMenu.add_command(label='Abrir...', command=self.open_file)
        self.recent_submenu = tk.Menu(self.fileMenu, tearoff=0)
        self.fileMenu.add_cascade(label='Abrir recentes', menu=self.recent_submenu)
        self.fileMenu.add_command(label='Fechar', command=self.close_file)
        self.fileMenu.add_command(label='Salvar', command=self.save_file)
        self.fileMenu.add_command(label='Salvar como...', command=self.save_file_as)
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
        self.usersMenu.add_command(label="Gerenciar")
        self.menuBar.add_cascade(label="Usuários", menu=self.usersMenu)

        # Help menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="Sobre")
        self.menuBar.add_cascade(label='Ajuda', menu=self.helpMenu)

        self.window.config(menu=self.menuBar)

        self.text_widget = tk.Text(self.window, wrap=tk.WORD, width=200, height=40)
        self.text_widget.pack()

        self.center_window(1024, 760)

    def new_file(self):
        self.current_file = None
        self.text_widget.delete(1.0, tk.END)

    # Open files
    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.add_to_recent(file_path)
            self.update_recent_submenu()
            self.load_file_content(file_path)
            self.current_file = file_path

    # Add the recent file to recent files list
    def add_to_recent(self, file_path):
        if file_path not in self.recent_files:
            self.recent_files.append(file_path)

    # Update the recent files submenu
    def update_recent_submenu(self):
        self.recent_submenu.delete(0, tk.END)
        for file_path in self.recent_files:
            base_name = os.path.basename(file_path)
            self.recent_submenu.add_command(label=base_name,
                                            command=lambda path=file_path: self.open_recent(path))

    # Open recent files
    def open_recent(self, file_path):
        self.load_file_content(file_path)
        self.current_file = file_path

    def load_file_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
        except Exception as e:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f'Erro ao abrir o arquivo: {str(e)}')

    def save_file(self):
        if self.current_file:
            content = self.text_widget.get(1.0, tk.END)
            with open(self.current_file, 'w') as file:
                file.write(content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.html', filetypes=[("Arquivo html", "*.html")])
        if file_path:
            self.current_file = file_path
            self.save_file()

    def close_file(self):
        self.current_file = None
        self.text_widget.delete(1.0, tk.END)

    # Centralize the window
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
