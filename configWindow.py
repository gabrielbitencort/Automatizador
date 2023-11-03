import tkinter as tk
from tkinter import ttk
import json


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
        self.smtpTab = ttk.Frame(self.notebook)
        # Add tabs to notebook
        self.notebook.add(self.tab1, text='Aba 1')
        self.notebook.add(self.tab2, text='Aba 2')
        self.notebook.add(self.smtpTab, text='Configurar SMTP')
        # Add content for tabs
        self.smtpTitle = tk.Label(self.smtpTab, text="Configurações do servidor SMTP")
        self.smtpServer = tk.Label(self.smtpTab, text='Servidor SMTP: ')
        self.serverInput = tk.Entry(self.smtpTab, width=22)
        self.smtpPort = tk.Label(self.smtpTab, text='Porta: ')
        self.portInput = tk.Entry(self.smtpTab, width=6)
        self.smtpEmail = tk.Label(self.smtpTab, text='Email: ')
        self.emailInput = tk.Entry(self.smtpTab, width=30)
        self.smtpPassword = tk.Label(self.smtpTab, text='Senha: ')
        self.passwdInput = tk.Entry(self.smtpTab, show='*')
        self.btn_save = tk.Button(self.smtpTab, text='SALVAR', command=self.save_settings)

        # Tab widgets position
        self.smtpTitle.pack(padx=10, pady=10)
        self.smtpServer.place(x=10, y=50)
        self.serverInput.place(x=115, y=50)
        self.smtpPort.place(x=305, y=50)
        self.portInput.place(x=350, y=50)
        self.smtpEmail.place(x=10, y=75)
        self.emailInput.place(x=70, y=75)
        self.smtpPassword.place(x=10, y=100)
        self.passwdInput.place(x=70, y=100)
        self.btn_save.place(x=270, y=175)

        self.notebook.pack(expand=True, fill="both")

    def save_settings(self):
        server = self.serverInput.get()
        port = self.portInput.get()
        email = self.emailInput.get()
        password = self.passwdInput.get()

        data = {
            "Server": server,
            "Port": port,
            "Email": email,
            "Password": password
        }

        with open('settings.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
