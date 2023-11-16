from loginWindow import LoginWindow
from mainWindow import MainWindow
from registerWindow import RegisterWindow
from passlib.hash import pbkdf2_sha256
import tkinter as tk
# import os
import psycopg2

db_config = "dbname=automatizador user=postgres password=mpti3562 host=127.0.0.1"


def open_mainWindow():
    loginWindow.window.destroy()
    mainWindow = MainWindow(lambda: open_registerWindow(loginWindow))
    mainWindow.window.mainloop()


def open_registerWindow(login_window):
    registerWindow = RegisterWindow(lambda: userRegister(registerWindow))
    registerWindow.window.mainloop()


def clear_input_fields(input_fields):
    for entry in input_fields:
        entry.delete(0, tk.END)


def hash_password(password):
    password = password.encode('utf-8')
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash


def verify_password(stored_password_hash, provided_password):
    return pbkdf2_sha256.verify(provided_password, stored_password_hash)


def call_main_window(event=None):
    loginWindow.text_message.config(text='')
    user_name = loginWindow.input_name.get()
    password = loginWindow.input_passwd.get()
    if user_name and password:
        try:
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()
            query = 'SELECT password_hash FROM users WHERE name = %s'
            data = (user_name,)
            cursor.execute(query, data)
            user_data = cursor.fetchone()
            conn.close()

            if user_data:
                stored_password_hash = user_data[0]

                if verify_password(stored_password_hash, password):
                    loginWindow.text_message.config(text='Login realizado com secesso.')
                    loginWindow.window.after(2000, open_mainWindow())
                else:
                    loginWindow.text_message.config(text='Dados de login incorretos.')
            else:
                loginWindow.text_message.config(text='Dados de login incorretos.')
        except psycopg2.Error as error:
            print("Erro ao consultar o banco de dados: ", error)
    else:
        loginWindow.text_message.config(text='Preencha todos os campos.')


def create_users_table():
    conn = None
    try:
        conn = psycopg2.connect(db_config)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                   id SERIAL PRIMARY KEY,
                                   name TEXT, 
                                   email TEXT, 
                                   password_hash TEXT
                                   )''')
        conn.commit()
        print("Tabela criada ou já existe.")
    except psycopg2.Error as error:
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
                # Create password with hash and salt
                password_hash = hash_password(user_passwd)

                try:
                    conn = psycopg2.connect(db_config)
                    cursor = conn.cursor()

                    query = 'INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)'
                    data = (user_login, user_email, password_hash)
                    cursor.execute(query, data)
                    conn.commit()
                    conn.close()
                    registerWindow.text_message.config(text="Usuário cadastrado com sucesso.")
                    print("Usuário cadastrado")

                    # Clear input fields
                    clear_input_fields(input_fields)

                except psycopg2.Error as error:
                    registerWindow.text_message.config(text="Erro ao inserir os dados!")
                    print("Erro ao inserir os dados: ", error)
        else:
            registerWindow.text_message.config(text="As senhas digitadas estão diferentes!")
    else:
        registerWindow.text_message.config(text='Por favor, preencha todos os campos!')


if __name__ == '__main__':
    loginWindow = LoginWindow(call_main_window)
    # open_mainWindow()
    loginWindow.window.mainloop()
