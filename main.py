from PyQt5 import uic, QtWidgets
import sqlite3


def call_main_screen():
    login.label_4.setText("")
    user_name = login.edit_name.text()
    password = login.edit_passwd.text()
    if user_name == "gabriel" and password == "123456":
        login.close()
        main.show()
    else:
        login.label_4.setText("Dados de login incorretos!")


def logout():
    main.close()
    login.show()


def call_register_screen():
    register.show()

def user_register():
    name = register.input_name.text()
    user_login = register.input_login.text()
    passwd = register.input_passwd.text()
    c_passwd = register.input_cpasswd.text()

    if passwd == c_passwd:
        try:
            db = sqlite3.connect('db_register.db')
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS register (name, login, passwd)")
            cursor.execute("INSERT INTO register (name, login, passwd) VALUES ('"+name+", "+user_login+", "+passwd+"')")
            db.commit()
            db.close()
            register.label_5.setText("Usuário cadastrado com sucesso.")
        except sqlite3.Error as error:
            register.label_5.setText("Erro ao inserir os dados!")
            print("Erro ao inserir os dados: ", error)
    else:
        register.label_5.setText("As senhas digitadas estão diferentes!")


app = QtWidgets.QApplication([])
login = uic.loadUi("UI/login.ui")
main = uic.loadUi("UI/main.ui")
register = uic.loadUi("UI/register.ui")
login.btn_enter.clicked.connect(call_main_screen)
login.edit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
login.btn_register.clicked.connect(call_register_screen)
register.btn_register.clicked.connect(user_register)

login.show()
app.exec()
