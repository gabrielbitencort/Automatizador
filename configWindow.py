import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import psycopg2

from settings import getDatabaseUrl
db_config = getDatabaseUrl()


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

        # Add content for tab1
        self.title1 = tk.Label(self.tab1, text="EM DESENVOLVIMENTO")
        self.title1.pack(padx=10, pady=30)

        # Add content for tab2
        self.title2 = tk.Label(self.tab2, text='EM DESENVOLVIMENTO')
        self.title2.pack(padx=10, pady=30)

        # Add content for smtpTab
        self.smtpTitle = tk.Label(self.smtpTab, text="Configurações do servidor SMTP")

        self.smtpServer = tk.Label(self.smtpTab, text='Servidor SMTP: ')
        self.serverInput = tk.Entry(self.smtpTab, width=30)

        self.smtpPort = tk.Label(self.smtpTab, text='Porta: ')
        self.portInput = tk.Entry(self.smtpTab, width=10)

        self.smtpEmail = tk.Label(self.smtpTab, text='Email: ')
        self.emailInput = tk.Entry(self.smtpTab, width=30)

        self.smtpPassword = tk.Label(self.smtpTab, text='Senha: ')
        self.passwdInput = tk.Entry(self.smtpTab, show='*')

        self.btn_save = tk.Button(self.smtpTab, text='SALVAR', width=10, height=1, command=self.save_settings)
        self.configMessage3 = tk.Label(self.smtpTab, text='')

        self.btn_cancel = tk.Button(self.smtpTab, text='CANCELAR', width=10, height=1, command=self.cancel)

        # smtpTab widgets position
        self.smtpTitle.pack(padx=10, pady=10)
        self.smtpServer.place(x=10, y=50)
        self.serverInput.place(x=100, y=50)
        self.smtpPort.place(x=305, y=50)
        self.portInput.place(x=350, y=50)
        self.smtpEmail.place(x=10, y=75)
        self.emailInput.place(x=70, y=75)
        self.smtpPassword.place(x=10, y=100)
        self.passwdInput.place(x=70, y=100)
        self.btn_save.place(x=190, y=150)
        self.btn_cancel.place(x=320, y=150)
        self.configMessage3.place(x=10, y=185)

        self.notebook.pack(expand=True, fill="both")

    def cancel(self):
        input_fields = [self.serverInput, self.portInput, self.emailInput, self.passwdInput]
        for entry in input_fields:
            entry.delete(0, tk.END)

    @staticmethod
    def create_smtp_table():
        conn = None
        try:
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS smtp (
                                    id SERIAL PRIMARY KEY,
                                    server TEXT, 
                                    port TEXT,
                                    email TEXT, 
                                    password TEXT
                                    )''')
            conn.commit()
            print("Tabela criada ou já existe.")
        except psycopg2.Error as error:
            print("Erro ao criar a tabela smtp: ", error)
        finally:
            if conn is not None:
                conn.close()

    def save_settings(self):
        self.create_smtp_table()
        smtpServer = self.serverInput.get()
        smtpPort = self.portInput.get()
        smtpEmail = self.emailInput.get()
        smtpPassword = self.passwdInput.get()

        if smtpServer and smtpPort and smtpEmail and smtpPassword:
            # converte o email para minusculas para comparação
            smtpEmailLower = smtpEmail.lower()

            # usando o bloco "with" para lidar com a conexão automaticamente
            with psycopg2.connect(db_config) as conn:
                try:
                    cursor = conn.cursor()

                    # verifica se já existe uma entrada com o mesmo servidor de e-mail
                    query_check = 'SELECT id FROM smtp WHERE LOWER(server) = LOWER(%s) OR LOWER(email) = %s'
                    data_check = (smtpServer, smtpEmailLower)
                    cursor.execute(query_check, data_check)
                    existing_id = cursor.fetchone()

                    print(f"Existing ID: {existing_id}")

                    if existing_id:
                        # Se já existir, atualiza dados
                        print("Updating existing entry.")
                        query_update = "UPDATE smtp SET server = %s, port = %s, email = %s, password = %s WHERE id = %s"
                        data_update = (smtpServer, smtpPort, smtpEmail, smtpPassword, existing_id[0])
                        cursor.execute(query_update, data_update)
                    else:
                        # Se não existir, criar nova entrada
                        print("Creating new entry.")
                        query_insert = "INSERT INTO smtp (server, port, email, password) VALUES (%s, %s, %s, %s)"
                        data_insert = (smtpServer, smtpPort, smtpEmail, smtpPassword)
                        cursor.execute(query_insert, data_insert)

                    conn.commit()
                    print("Dados SMTP inseridos ou atualizados com sucesso.")
                    tk.messagebox.showinfo("Sucesso", "Informações atualizadas com sucesso.", parent=self.window)
                except psycopg2.Error as e:
                    print("Erro ao inserir ou atualizar dados SMTP na tabela: ", e)
        else:
            self.configMessage3.config(text='Por favor, preencha todos os campos!')
