from loginWindow import LoginWindow
from mainWindow import MainWindow
from registerWindow import RegisterWindow
import tkinter as tk
import sqlite3, hashlib, os, json

database = 'Automatizador.db'


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


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)   # Generate a random "salt"

    password = password.encode('utf-8') # Converts password string into bytes
    password_hash = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    return salt, password_hash


def verify_password(stored_salt, stored_password_hash, provided_password):
    provided_password = provided_password.encode('utf-8')
    calculated_password_hash = hashlib.pbkdf2_hmac('sha256', provided_password, stored_salt, 100000)
    return stored_password_hash == calculated_password_hash


def call_main_window(event=None):
    loginWindow.text_message.config(text='')
    user_name = loginWindow.input_name.get()
    password = loginWindow.input_passwd.get()
    if user_name and password:
        try:
            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute('SELECT salt, password_hash FROM users WHERE name = ?', (user_name,))
            user_data = cursor.fetchone()
            db.close()

            if user_data:
                stored_salt, stored_password_hash = user_data
                if verify_password(stored_salt, stored_password_hash, password):
                    loginWindow.text_message.config(text='Login realizado com secesso.')
                    loginWindow.window.after(1000, open_mainWindow())
                else:
                    loginWindow.text_message.config(text='Dados de login incorretos.')
            else:
                loginWindow.text_message.config(text='Dados de login incorretos.')
        except sqlite3.Error as error:
            print("Erro ao consultar o banco de dados: ", error)
    else:
        loginWindow.text_message.config(text='Preencha todos os campos.')


# Function to verify if name and email exists
def check_duplicate_user(name, email):
    try:
        db = sqlite3.connect(database)
        cursor = db.cursor()
        # Execute a cunsult to verify if exists a user with same name
        cursor.execute('SELECT * FROM users WHERE name = ? OR email = ?', (name, email))
        existing_user = cursor.fetchone()

        if existing_user:
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Erro ao verificar duplicatas: ", error)
        return True
    finally:
        db.close()


# Function to register users
def userRegister(registerWindow):
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
                salt, password_hash = hash_password(user_passwd)
                try:
                    db = sqlite3.connect(database)
                    cursor = db.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                   id INTEGER PRIMARY KEY,
                                   name TEXT, 
                                   email TEXT, 
                                   salt BLOB, 
                                   password_hash BLOB
                                   )
                    ''')
                    cursor.execute('INSERT INTO users (name, email, salt, password_hash) VALUES (?, ?, ?, ?)',
                                   (user_login, user_email, salt, password_hash))
                    db.commit()
                    db.close()
                    registerWindow.text_message.config(text="Usuário cadastrado com sucesso.")

                    # Clear input fields
                    clear_input_fields(input_fields)

                except sqlite3.Error as error:
                    registerWindow.text_message.config(text="Erro ao inserir os dados!")
                    print("Erro ao inserir os dados: ", error)
        else:
            registerWindow.text_message.config(text="As senhas digitadas estão diferentes!")
    else:
        registerWindow.text_message.config(text='Por favor, preencha todos os campos!')


loginWindow = LoginWindow(call_main_window)
loginWindow.window.mainloop()
