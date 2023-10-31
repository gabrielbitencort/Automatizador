
def logout():
    main.close()
    login.show()

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