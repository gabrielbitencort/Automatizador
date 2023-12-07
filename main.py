import sys
from loginWindow import LoginWindow
from mainWindow import MainWindow
from registerWindow import RegisterWindow
from userSession import userSession
from passlib.hash import pbkdf2_sha256
import tkinter as tk
import logging
import psycopg2
import uuid
import os

from settings import getDatabaseUrl, createDefaultLogging
db_config = getDatabaseUrl()

# Obtém o diretório do script
if getattr(sys, 'frozen', False):
    scriptDir = os.path.dirname(sys.executable)
else:
    scriptDir = os.path.dirname(__file__)

createDefaultLogging(scriptDir)


def get_logged_in_user_id():
    return userSession.get_logged_in_user_id()

def set_logged_in_user_id(current_user_id):
    return userSession.set_logged_in_user_id(current_user_id)

def set_logged_in_user_name(user_name):
    return userSession.set_logged_in_user_name(user_name)

def open_mainWindow():
    try:
        loginWindow.window.destroy()
        mainWindow = MainWindow(lambda: open_registerWindow(loginWindow))
        mainWindow.window.mainloop()
    except Exception as e:
        logging.exception("Erro ao abrir mainWindow: %s", e)
        print(f"Erro ao abrir mainWindow: {e}")


def open_registerWindow(login_window):
    try:
        registerWindow = RegisterWindow(lambda: userRegister(registerWindow))
        registerWindow.window.mainloop()
    except Exception as e:
        logging.exception("Erro ao abrir registerWindow: %s", e)
        print(f"Erro ao abrir registerWindow: {e}")


def clear_input_fields(input_fields):
    for entry in input_fields:
        entry.delete(0, tk.END)


def hash_password(password):
    password = password.encode('utf-8')
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash


def verify_password(stored_password_hash, provided_password):
    return pbkdf2_sha256.verify(provided_password, stored_password_hash)


def login(event=None):
    loginWindow.text_message.config(text='')
    user_name = loginWindow.input_name.get()
    password = loginWindow.input_passwd.get()
    if user_name and password:
        try:
            logging.debug("Usuário e senha inseridos.")
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()

            # Consulta para obter o user_id usando o nome de usuário
            query_user_id = 'SELECT user_id FROM users WHERE name = %s'
            data_user_id = (user_name,)
            cursor.execute(query_user_id, data_user_id)
            user_id_data = cursor.fetchone()
            conn.close()

            if user_id_data:
                user_id = user_id_data[0]

                logging.debug("ID usuário logado: %s", user_id)

                # Consulta para obter a senha hash
                conn = psycopg2.connect(db_config)
                cursor = conn.cursor()

                query_password_hash = 'SELECT password_hash FROM users WHERE user_id = %s'
                data_password_hash = (user_id,)
                cursor.execute(query_password_hash, data_password_hash)
                stored_password_hash = cursor.fetchone()[0]
                conn.close()

                if verify_password(stored_password_hash, password):
                    set_logged_in_user_id(user_id)
                    set_logged_in_user_name(user_name)
                    print("Login realizado com sucesso.")
                    print(f"ID de usuário: {user_id}")

                    logging.info("Login realizado com sucesso.")
                    loginWindow.window.after(2000, open_mainWindow())
                else:
                    loginWindow.text_message.config(text='Dados de login incorretos.')
                    print("Dados de login incorretos.")
            else:
                loginWindow.text_message.config(text="Nome de usuário não encontrado")
                print("Nome de usuário não encontrado.")

        except psycopg2.Error as error:
            logging.exception("Erro ao consultar o banco de dados: %s", error)
            print("Erro ao consultar o banco de dados: ", error)
    else:
        loginWindow.text_message.config(text='Por favor, preencha todos os campos.')
        print("Por favor, preencha todos os campos.")


def create_users_table():
    conn = None
    try:
        conn = psycopg2.connect(db_config)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                   user_id UUID PRIMARY KEY,
                                   name TEXT, 
                                   email TEXT, 
                                   password_hash TEXT
                                   )''')
        conn.commit()
        logging.info("Tabela users criada ou já existe.")
        print("Tabela criada ou já existe.")
    except psycopg2.Error as error:
        logging.exception("Erro ao criar a tabela users: %s", error)
        print("Erro ao criar a tabela users: ", error)
    finally:
        if conn is not None:
            conn.close()


# Function to verify if name and email exists
def check_duplicate_user(name, email):
    conn = None
    try:
        conn = psycopg2.connect(db_config)
        cursor = conn.cursor()
        # Execute a cunsult to verify if exists a user with same name
        query = 'SELECT * FROM users WHERE name = %s OR email = %s'
        data = (name, email)
        cursor.execute(query, data)
        existing_user = cursor.fetchone()

        if existing_user:
            return True
        else:
            return False
    except psycopg2.Error as error:
        logging.exception("Erro ao verificar duplicatas: %s", error)
        print("Erro ao verificar duplicatas: ", error)
        return True
    finally:
        if conn is not None:
            conn.close()


# Function to register users
def userRegister(registerWindow):
    create_users_table()
    user_login = registerWindow.input_name.get()
    user_email = registerWindow.input_email.get()
    user_passwd = registerWindow.input_passwd.get()
    user_cpass = registerWindow.input_cpass.get()

    input_fields = [registerWindow.input_name, registerWindow.input_email, registerWindow.input_passwd,
                    registerWindow.input_cpass]

    if user_login and user_email and user_passwd and user_cpass:
        if user_passwd == user_cpass:
            if check_duplicate_user(user_login, user_email):
                registerWindow.text_message.config(text="Nome ou email já foram cadastrados.")
                # Clear input fields
                clear_input_fields(input_fields)
            else:
                # Generate a UUID for the user
                user_id = str(uuid.uuid4())
                # Create password with hash and salt
                password_hash = hash_password(user_passwd)

                try:
                    conn = psycopg2.connect(db_config)
                    cursor = conn.cursor()

                    query = 'INSERT INTO users (user_id, name, email, password_hash) VALUES (%s, %s, %s, %s)'
                    data = (user_id, user_login, user_email, password_hash)
                    cursor.execute(query, data)
                    conn.commit()
                    conn.close()
                    registerWindow.text_message.config(text="Usuário cadastrado com sucesso.")
                    logging.info("Usuário cadastrado com sucesso.")
                    print("Usuário cadastrado com sucesso.")

                    # Clear input fields
                    clear_input_fields(input_fields)

                except psycopg2.Error as error:
                    logging.exception("Erro ao inserir os dados: %s", error)
                    registerWindow.text_message.config(text="Erro ao inserir os dados!")
                    print("Erro ao inserir os dados: ", error)
        else:
            registerWindow.text_message.config(text="As senhas digitadas estão diferentes!")
    else:
        registerWindow.text_message.config(text='Por favor, preencha todos os campos!')


if __name__ == '__main__':
    logging.info("Script iniciado")
    loginWindow = LoginWindow(login)
    loginWindow.window.mainloop()
