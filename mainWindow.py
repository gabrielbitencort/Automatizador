import os
# import platform
import csv
import json
import smtplib
import threading
# import logging
import tkinter as tk
from builtins import FileNotFoundError
from tkinter import filedialog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import psycopg2

from configWindow import ConfigWindow
from updateWindow import UpdateSoftware
from managerWindow import ManagerWindow

db_config = "dbname=automatizador user=postgres password=mpti3562 host=127.0.0.1"


def open_configWindow():
    configWindow = ConfigWindow()
    configWindow.window.mainloop()


def open_updateWindow():
    updateWindow = UpdateSoftware()
    updateWindow.window.mainloop()


def open_managerWindow():
    managerwindow = ManagerWindow()
    managerwindow.window.mainloop()


class MainWindow:
    def __init__(self, open_registerWindow):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.recent_file_path = os.path.join(self.script_dir, 'recent_files.json')

        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title("Tela principal")

        self.window.protocol("WM_DELETE_WINDOW", self.save_recent_files_on_exit)

        #   Maximize window if sytem is windows
        # if platform.system() == "Windows":
        #     self.window.state("zoomed")
        # else:
        #     # Maximize window in other systems
        #     self.window.attributes('-zoomed', 1)

        # Current file name
        self.current_file = None

        # Create a menu
        self.menuBar = tk.Menu(self.window)

        # Archives menu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Novo", command=self.new_file, accelerator='Alt+Insert')
        self.fileMenu.add_command(label='Abrir...', command=self.open_file)
        self.recent_submenu = tk.Menu(self.fileMenu, tearoff=0)
        self.fileMenu.add_cascade(label='Abrir recentes', menu=self.recent_submenu)
        self.fileMenu.add_command(label='Fechar', command=self.close_file)
        self.fileMenu.add_command(label='Salvar', command=self.save_file, accelerator='Ctrl+S')
        self.fileMenu.add_command(label='Salvar como...', command=self.save_file_as, accelerator='Ctrl+Shift+S')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Configurações', command=open_configWindow)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Avançado')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Sair')
        self.menuBar.add_cascade(label='Arquivo', menu=self.fileMenu)

        # Users menu
        self.usersMenu = tk.Menu(self.menuBar, tearoff=0)
        self.usersMenu.add_command(label="Cadastrar", command=open_registerWindow)
        self.usersMenu.add_command(label="Gerenciar", command=open_managerWindow)
        self.menuBar.add_cascade(label="Usuários", menu=self.usersMenu)

        # Help menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="Sobre")
        self.helpMenu.add_command(label="Procurar por atualizações...", command=open_updateWindow)
        self.menuBar.add_cascade(label='Ajuda', menu=self.helpMenu)

        self.window.config(menu=self.menuBar)

        self.text_widget = tk.Text(self.window, wrap=tk.WORD, width=160, height=30)
        self.text_widget.pack()

        self.btn_send = tk.Button(self.window, text='ENVIAR EMAIL', command=self.sendEmails, state=tk.DISABLED)
        self.btn_send.place(x=40, y=500)
        self.sendLabel = tk.Label(self.window, text='')
        self.sendLabel.place(x=135, y=500)
        self.contacts = tk.Button(self.window, text='Selecionar arquivo de contatos', command=self.open_contactFile)
        self.contacts.place(x=40, y=535)
        self.contacts_file_path = None

        self.center_window(1024, 760)

        self.recent_files = self.load_recent_files(self.recent_file_path)
        self.update_recent_submenu()

    def open_contactFile(self):
        contacts_dir = 'Contacts'
        contact_path = filedialog.askopenfilename(initialdir=contacts_dir)
        if contact_path:
            self.contacts = self.load_contacts(contact_path)
            self.sendLabel.config(text=f'enviando para {contact_path}')
            self.btn_send.config(state=tk.NORMAL)

    @staticmethod
    def load_contacts(contact_path):
        names = []
        emails = []

        with open(contact_path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) >= 2:
                    names.append(row[0])
                    emails.append(row[1])
        return names, emails

    def read_smtpConfig(self):
        conn = None
        try:
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()
            query = 'SELECT server, port, email, password FROM smtp'
            cursor.execute(query)
            smtp_data = cursor.fetchone()

            if smtp_data:
                self.smtpServer, self.smtpPort, self.smtpEmail, self.smtpPassword = smtp_data
            else:
                print("Nenhuma configuração SMTP encontrada no banco de dados.")
        except psycopg2.Error as e:
            print("Erro ao consultar tabela: ", e)
        finally:
            if conn is not None:
                conn.close()

    def sendEmails(self):
        if self.contacts is not None:
            self.read_smtpConfig()
            names, emails = self.contacts
            print(names)
            print(emails)

            if self.current_file is not None:
                def send_email_func():
                    try:
                        print("Enviando email com arquivo: ", self.current_file)
                        for email in emails:
                            # Create MIMEMultipart object for email
                            msg = MIMEMultipart("alternative")
                            msg['From'] = self.smtpEmail
                            msg['To'] = email
                            msg['Subject'] = 'Teste Automatizador de Emails'

                            # Attach html_file to email body
                            with open(self.current_file, 'r', encoding='utf-8') as html_file:
                                email_body = MIMEText(html_file.read(), 'html', 'utf-8')
                            msg.attach(email_body)
                            # logging.basicConfig(level=logging.DEBUG)
                            # Initialize SMTP connection
                            server = smtplib.SMTP(self.smtpServer, self.smtpPort)
                            server.set_debuglevel(1)
                            server.starttls()
                            server.login(self.smtpEmail, self.smtpPassword)

                            # Send email for recipients
                            server.sendmail(self.smtpEmail, email, msg.as_string())
                            server.quit()
                            print("Email enviado.")
                    except Exception as e:
                        print(f"Erro ao enviar email: {str(e)}")

                # Create a new thread and execute email sending func
                email_thread = threading.Thread(target=send_email_func)
                email_thread.start()
            else:
                print("Arquivo html não selecionado.")

    def new_file(self):
        self.current_file = None
        self.text_widget.delete(1.0, tk.END)

    # Open files
    def open_file(self):
        file_dir = 'Messages'
        file_path = filedialog.askopenfilename(initialdir=file_dir)
        if file_path:
            self.add_to_recent(file_path)
            self.current_file = file_path
            self.add_to_recent(file_path)
            self.update_recent_submenu()
            self.load_file_content(file_path)
            self.save_recent_file()

    def save_recent_file(self):
        try:
            with open(self.recent_file_path, 'w') as file:
                json.dump(self.recent_files, file)
                print(f"Arquivo recente salvo: {self.recent_files}")
        except Exception as e:
            print(f"Erro ao salvar arquivos recentes: {e}")

    @staticmethod
    def load_recent_files(recent_file_path):
        try:
            with open(recent_file_path, 'r') as file:
                # Verifica se o arquivo não está vazio
                if os.path.getsize(recent_file_path) > 0:
                    recent_files = json.load(file)
                else:
                    recent_files = []
                return recent_files
        except FileNotFoundError:
            print("Erro ao carregar JSON")
            return []
        except PermissionError:
            print("Erro de permissão ao abrir JSON")
            return []

    # Add the recent file to recent files list
    def add_to_recent(self, file_path):
        if file_path not in self.recent_files:
            self.recent_files.append(file_path)

    # Update the recent files submenu
    def update_recent_submenu(self):
        self.recent_submenu.delete(0, tk.END)
        for file_path in self.recent_files:
            base_name = os.path.basename(file_path)
            self.recent_submenu.add_command(label=base_name, command=lambda path=file_path: self.open_recent(path))

    # Open recent files
    def open_recent(self, file_path):
        self.load_file_content(file_path)
        self.current_file = file_path

    def load_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
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

    def save_recent_files_on_exit(self):
        self.save_recent_file()
        self.window.destroy()
