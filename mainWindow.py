import os
import csv
import sys
import json
import logging
import smtplib
import datetime
import threading
import tkinter as tk
from tkinter import filedialog
from tkhtmlview import HTMLLabel
from tkcalendar import DateEntry
from email.mime.text import MIMEText
from builtins import FileNotFoundError
from email.mime.multipart import MIMEMultipart
import psycopg2

from configWindow import ConfigWindow
from updateWindow import UpdateSoftware
from managerWindow import ManagerWindow

from timePicker import TimePicker
from userSession import userSession
from settings import getDatabaseUrl, createDefaultLogging

db_config = getDatabaseUrl()

# Caminho do arquivo recent_files.json
if getattr(sys, 'frozen', False):
    scriptDir = os.path.dirname(sys.executable)
else:
    scriptDir = os.path.dirname(__file__)
recent_file_path = os.path.join(scriptDir, 'recent_files.json')

createDefaultLogging(scriptDir)


def get_logged_in_user_id():
    return userSession.get_logged_in_user_id()

def get_logged_in_user_name():
    return userSession.get_logged_in_user_name()

def open_configWindow():
    configWindow = ConfigWindow()
    configWindow.window.mainloop()

def open_updateWindow():
    updateWindow = UpdateSoftware()
    updateWindow.window.mainloop()

def open_managerWindow():
    managerWindow = ManagerWindow()
    managerWindow.window.mainloop()

def show_current_id():
    user_id = get_logged_in_user_id()
    print(f"ID do usuário atual: {user_id}")


class MainWindow:
    def __init__(self, open_registerWindow):
        # User_ID do usuário logado
        self.current_user_id = get_logged_in_user_id()
        self.current_user_name = get_logged_in_user_name()

        self.timer_id = None

        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry('800x600')
        self.window.title("Tela principal")

        self.window.protocol("WM_DELETE_WINDOW", self.save_recent_files_on_exit)

        #   Maximize window if system is windows
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

        # Frame do textWidget
        self.tframe = tk.Frame(self.window)
        self.tframe.pack(side=tk.TOP, padx=10, pady=10)

        # Frame dos botões
        self.btn_frame = tk.Frame(self.window)
        self.btn_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Frame do botão view_file
        self.view_frame = tk.Frame(self.window)
        self.view_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Frame informações usuário
        self.infoFrame = tk.Frame(self.window)
        self.infoFrame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.email_status = tk.Label(self.infoFrame, text="")
        self.email_status.grid(row=0, column=0, pady=5, sticky='w')

        self.user_text = tk.Label(self.infoFrame, text=f"Usuário atual: {self.current_user_name}")
        self.user_text.grid(row=0, column=1, pady=5, sticky='w')

        # textWidget para mostrar e editar conteúdo do arquivo html
        self.text_widget = tk.Text(self.tframe, wrap=tk.WORD, width=160, height=30)
        self.text_widget.grid(row=0, column=0, columnspan=2)

        # botão para visualizar email
        self.btn_view = tk.Button(self.view_frame, text="VISUALIZAR E-MAIL", command=self.view_file)
        self.btn_view.grid(row=1, column=0, pady=10, sticky='e')

        # botão para enviar emails
        self.btn_send = tk.Button(self.btn_frame, text='ENVIAR EMAIL', command=self.handle_sendEmails,
                                  state=tk.DISABLED)
        self.btn_send.grid(row=1, column=0, pady=10, sticky='w')

        # checkbox para programar horário
        self.var_checkbox = tk.IntVar()
        self.checkbox = tk.Checkbutton(self.btn_frame, text="Programar horário", variable=self.var_checkbox,
                                       command=self.verify_checkbox)
        self.checkbox.grid(row=1, column=1, pady=10, padx=10, sticky='w')

        # entrada para selecionar data de envio
        self.cal = DateEntry(self.btn_frame, width=16, background='gray', foreground='white', bd=2)
        self.cal.grid_remove()

        # entrada para selecionar horário de envio
        self.time = TimePicker(self.btn_frame)
        self.time.get_time(row=1, column=3, padx=10, pady=10, sticky='w')
        self.time.hide_time_picker()

        # botão para selecionar arquivo CSV
        self.contacts = tk.Button(self.btn_frame, text='Selecionar arquivo de contatos', command=self.open_contactFile)
        self.contacts.grid(row=2, column=0, pady=10, sticky='w')

        # texto para mostrar arquivo CSV selecionado
        self.sendLabel = tk.Label(self.btn_frame, text='')
        self.sendLabel.grid(row=2, column=1, pady=10, sticky='w')

        self.contacts_file_path = None

        self.center_window(1024, 760)

        self.recent_files = self.load_recent_files(recent_file_path)
        self.update_recent_submenu()
        show_current_id()

    def handle_sendEmails(self):
        try:
            # Verifica se a checkbox está marcada
            if self.var_checkbox.get() == 1:
                # Verifica se a thread do temporizador está ativa
                if not self.timer_id or not self.timer_id.is_alive():
                    # Chama a função sendEmails imediatamente se a checkbox estivar ativa
                    logging.info("Enviando email temporizado")
                    print("Enviando email temporizado.")
                    self.start_timer()
            else:
                logging.info("A checkbox não está marcada, enviando email imediatamente")
                print("A checkbox não está marcada, enviando email imediatamente.")
                self.sendEmails()
                self.cancel_timer()
        except Exception as e:
            logging.exception(f"Erro ao enviar email temporizado: {e}")
            print(f"Erro ao enviar email temporizado: {e}")

    def verify_checkbox(self):
        if self.var_checkbox.get() == 1:
            print("A checkbox está marcada.")
            self.cal.grid(row=1, column=2, pady=10, padx=10, sticky='w')
            self.time.show_time_picker()
        else:
            print("A checkbox está desmarcada.")
            self.cal.grid_remove()
            self.time.hide_time_picker()

    def start_timer(self):
        try:
            # Cancela o temporizador se estiver ativo
            self.cancel_timer()

            # Obtém a data e hora programada
            scheduled_date = self.cal.get_date()
            scheduled_time = self.time.get_selected_time()

            # Combina a data e a hora
            scheduled_datetime = datetime.datetime.combine(scheduled_date, datetime.time(hour=scheduled_time[0],
                                                                                         minute=scheduled_time[1]))

            # Calcula o tempo restante até a data e hora programada em segundos
            current_time = datetime.datetime.now()
            time_difference = (scheduled_datetime - current_time).total_seconds()

            # Inicia o temporizador apenas se o tempo restante for positivo
            if time_difference > 0:
                self.timer_id = self.window.after(int(time_difference * 1000), self.sendEmails_on_timer)
            print(f"")

        except threading.ThreadError as e:
            logging.exception(f"Erro de threading: {e}")
            print(f"Erro de threading: {e}")
        except Exception as e:
            logging.exception(f"Erro: {e}")
            print(f"Erro: {e}")

    def sendEmails_on_timer(self):
        logging.info("Enviando email temporizado")
        print("Enviando email temporizado")
        self.sendEmails()

        # Decide se deve iniciar o temporizador novamente
        if self.var_checkbox.get() == 1 and self.timer_id is not None:
            self.start_timer()

    def cancel_timer(self):
        # Cancela o temporizador se estiver ativo
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    def open_contactFile(self):
        try:
            contacts_dir = 'Contacts'
            contact_path = filedialog.askopenfilename(initialdir=contacts_dir)
            if contact_path:
                file_name = os.path.basename(contact_path)
                self.contacts = self.load_contacts(contact_path)
                self.sendLabel.config(text=f'enviando para {file_name}')
                self.btn_send.config(state=tk.NORMAL)
        except Exception as e:
            logging.exception(f"Erro ao abrir arquivo de contatos: {e}")
            print(f"Erro ao abrir arquivo de contatos: {e}")

    @staticmethod
    def load_contacts(contact_path):
        names = []
        emails = []
        try:
            with open(contact_path, 'r') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    if len(row) >= 2:
                        names.append(row[0])
                        emails.append(row[1])
            return names, emails
        except Exception as e:
            logging.exception(f"Erro ao carregar lista de contatos")
            print(f"Erro ao carregar lista de contatos: {e}")

    def read_smtpConfig(self):
        conn = None
        try:
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()
            query = 'SELECT server, port, email, password FROM smtp WHERE user_id = %s'
            data = (self.current_user_id,)
            cursor.execute(query, data)
            smtp_data = cursor.fetchone()

            if smtp_data:
                self.smtpServer, self.smtpPort, self.smtpEmail, self.smtpPassword = smtp_data
            else:
                logging.error("Nenhuma configuração SMTP encontrada no banco de dados")
                print("Nenhuma configuração SMTP encontrada no banco de dados.")
        except psycopg2.Error as e:
            logging.exception(f"Erro ao consultar tabela: {e}")
            print(f"Erro ao consultar tabela: {e}")
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
                        print("Enviando emails com arquivo: ", self.current_file)
                        print(f"Enviando emails com o user_id {self.current_user_id}")
                        logging.info("Enviando email imediato")
                        self.email_status.config(text="Enviando E-mails...")
                        for email in emails:
                            # Create MIMEMultipart object for email
                            msg = MIMEMultipart("alternative")
                            msg['From'] = self.smtpEmail
                            msg['To'] = email
                            msg['Subject'] = 'Teste Automatizador de Emails'

                            # Attach html_file to email body
                            with open(self.current_file, 'r', encoding='utf-8') as html_file:
                                email_body = MIMEText(html_file.read().replace("=", "@"), 'html', 'utf-8')
                            msg.attach(email_body)
                            logging.basicConfig(level=logging.DEBUG)
                            # Initialize SMTP connection
                            server = smtplib.SMTP(self.smtpServer, self.smtpPort)
                            server.set_debuglevel(1)
                            server.ehlo()
                            server.starttls()
                            server.login(self.smtpEmail, self.smtpPassword)

                            # Send email for recipients
                            server.sendmail(self.smtpEmail.replace("=", "@"), email.replace("=", "@"), msg.as_string())
                            server.quit()
                            logging.info("Email enviado")
                            print("Email enviado.")
                            self.email_status.config(text="E-mails enviados")
                    except Exception as e:
                        logging.exception(f"Erro ao enviar email: {e}")
                        print(f"Erro ao enviar email: {str(e)}")
                        self.email_status.config(text=f"Erro ao enviar E-mails: {str(e)}")

                # Create a new thread and execute email sending func
                email_thread = threading.Thread(target=send_email_func)
                email_thread.start()
            else:
                logging.error("Arquivo html não selecionado")
                print("Arquivo html não selecionado.")

    def new_file(self):
        self.current_file = None
        self.text_widget.delete(1.0, tk.END)

    # Open files
    def open_file(self):
        try:
            file_dir = 'Messages'
            file_path = filedialog.askopenfilename(initialdir=file_dir, defaultextension='.html',
                                                   filetypes=[("Arquivo html", "*.html")])
            if file_path:
                self.add_to_recent(file_path)
                self.current_file = file_path
                self.add_to_recent(file_path)
                self.update_recent_submenu()
                self.load_file_content(file_path)
                self.save_recent_file()
        except Exception as e:
            logging.exception(F"Não foi possivel abrir o arquivo: {e}")
            print(f"Não foi possível abrir o arquivo: {e}")

    def save_recent_file(self):
        try:
            with open(recent_file_path, 'w') as file:
                json.dump(self.recent_files, file)
                logging.info(f"Arquivo recente salvo: {self.recent_files}")
                print(f"Arquivo recente salvo: {self.recent_files}")
        except Exception as e:
            logging.exception(f"Erro ao salvar arquivos recentes: {e}")
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
        except FileNotFoundError as e:
            logging.exception(f"Erro ao carregar JSON: {e}")
            print(f"Erro ao carregar JSON: {e}")
            return []
        except PermissionError as e:
            logging.exception(f"Erro de prmissão ao abrir JSON: {e}")
            print(f"Erro de permissão ao abrir JSON: {e}")
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
            logging.exception(f"Erro ao abrir o arquivo: {str(e)}")
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

    def view_file(self):
        if not hasattr(self, 'view_window') or not self.view_window.winfo_exists():
            self.view_window = tk.Toplevel(self.window)
            self.view_window.title("VISUALIZAR E-MAIL")
            self.view_label = HTMLLabel(self.view_window)
            self.view_label.pack(expand=True, fill='both')

            if self.current_file:
                with open(self.current_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.view_label.set_html(content)
        else:
            self.view_window.lift()

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
