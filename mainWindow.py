import os, platform, csv, json, smtplib
import tkinter as tk
from tkinter import filedialog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configWindow import ConfigWindow


def open_configWindow():
    configWindow = ConfigWindow()
    configWindow.window.mainloop()


class MainWindow:
    def __init__(self, open_registerWindow):

        self.recent_files = self.load_recent_files()

        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title("Tela principal")

        self.window.protocol("WM_DELETE_WINDOW", self.save_recent_files_on_exit)

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
        self.usersMenu.add_command(label="Gerenciar")
        self.menuBar.add_cascade(label="Usuários", menu=self.usersMenu)

        # Help menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="Sobre")
        self.menuBar.add_cascade(label='Ajuda', menu=self.helpMenu)

        self.window.config(menu=self.menuBar)

        self.text_widget = tk.Text(self.window, wrap=tk.WORD, width=200, height=40)
        self.text_widget.pack()

        self.btn_send = tk.Button(self.window, text='ENVIAR EMAIL', command=self.sendEmails, state=tk.DISABLED)
        self.btn_send.place(x=40, y=700)
        self.sendLabel = tk.Label(self.window, text='')
        self.sendLabel.place(x=135, y=700)
        self.contacts = tk.Button(self.window, text='Selecionar arquivo de contatos', command=self.open_contactFile)
        self.contacts.place(x=40, y=735)
        self.contacts_file_path = None

        self.center_window(1024, 760)

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

    @staticmethod
    def read_smtpConfig():
        smtpConfig_path = 'smtp.json'
        if smtpConfig_path:
            with open(smtpConfig_path, 'r') as file:
                data = json.load(file)
                smtpServer = data.get("Server")
                smtpPort = data.get("Port")
                smtpEmail = data.get("Email")
                smtpPassword = data.get("Password")
            return smtpServer, smtpPort, smtpEmail, smtpPassword

    def sendEmails(self):
        if self.contacts is not None:
            smtpServer, smtpPort, smtpEmail, smtpPassword = self.read_smtpConfig()
            names, emails = self.contacts
            print(names)
            print(emails)

            try:
                if self.current_file is not None:
                    print("Enviando email com arquivo: ", self.current_file)
                    for email in emails:
                        # Create MIMEMultipart object for email
                        msg = MIMEMultipart("alternative")
                        msg['From'] = smtpEmail
                        msg['To'] = ', '.join(email)
                        msg['Subject'] = 'Teste Automatizador de Emails'

                        # Attach html_file to email body
                        with open(self.current_file, 'r', encoding='utf-8') as html_file:
                            email_body = MIMEText(html_file.read(), 'html', 'utf-8')
                        msg.attach(email_body)

                        # Initialize SMTP connection
                        server = smtplib.SMTP(smtpServer, smtpPort)
                        server.starttls()
                        server.login(smtpEmail, smtpPassword)

                        # Send email for recipients
                        server.sendmail(smtpEmail, email, msg.as_string())
                        server.quit()
                        print("Email enviado.")
                else:
                    print("Arquivo html não selecionado.")
            except Exception as e:
                print(f"Erro ao enviar email: {str(e)}")

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
        with open('recent_files.json', 'w') as file:
            json.dump(self.recent_files, file)
            print("Arquivo recente salvo")

    @staticmethod
    def load_recent_files():
        try:
            with open('recent_files.json', 'r') as file:
                recent_files = json.load(file)
            return recent_files
        except FileNotFoundError:
            print("Erro ao carregar JSON")

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

    def save_recent_files_on_exit(self):
        self.save_recent_file()
        self.window.destroy()
