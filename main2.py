from loginWindow import LoginWindow
from mainWindow import MainWindow
from registerWindow import RegisterWindow
import sqlite3


def call_main_window(event=None):
    loginWindow.text_message.config(text='')
    user_name = loginWindow.input_name.get()
    password = loginWindow.input_passwd.get()
    if user_name and password:
        try:
            db = sqlite3.connect("Automatizador.db")
            cursor = db.cursor()
            cursor.execute('SELECT * FROM users WHERE name = ? AND passwd = ?', (user_name, password))
            user = cursor.fetchone()
            db.close()

            if user is not None:
                loginWindow.text_message.config(text='Login realizado com secesso')
                loginWindow.window.after(1000, open_mainWindow())
            else:
                loginWindow.text_message.config(text='Dados de login incorretos')
        except sqlite3.Error as error:
            print("Erro ao consultar o banco de dados: ", error)
    else:
        loginWindow.text_message.config(text='Preencha todos os campos.')


def open_mainWindow():
    loginWindow.window.destroy()
    mainWindow = MainWindow(lambda: open_registerWindow(loginWindow))
    mainWindow.window.mainloop()

def open_registerWindow(login_window):
    registerWindow = RegisterWindow(lambda: userRegister(registerWindow))
    registerWindow.window.mainloop()


def userRegister(registerWindow):
    user_login = registerWindow.input_name.get()
    user_email = registerWindow.input_email.get()
    user_passwd = registerWindow.input_passwd.get()
    user_cpass = registerWindow.input_cpass.get()

    if user_login and user_email and user_passwd and user_cpass:
        if user_passwd == user_cpass:
            try:
                db = sqlite3.connect('Automatizador.db')
                cursor = db.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY,
                               name TEXT, 
                               email TEXT, 
                               passwd TEXT
                               )
                ''')
                cursor.execute('INSERT INTO users (name, email, passwd) VALUES (?, ?, ?)', (user_login, user_email, user_passwd))
                db.commit()
                db.close()
                registerWindow.text_message.config(text="Usuário cadastrado com sucesso.")
            except sqlite3.Error as error:
                registerWindow.text_message.config(text="Erro ao inserir os dados!")
                print("Erro ao inserir os dados: ", error)
        else:
            registerWindow.text_message.config(text="As senhas digitadas estão diferentes!")
    else:
        registerWindow.text_message.config(text='Por favor, preencha todos os campos!')


loginWindow = LoginWindow(call_main_window)
loginWindow.window.mainloop()
