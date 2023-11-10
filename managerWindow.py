import tkinter as tk
import tkinter.messagebox
import psycopg2
from passlib.hash import pbkdf2_sha256

db_config = "dbname=automatizador user=postgres password=mpti3562 host=127.0.0.1"

def check_duplicate_user(name, email):
    db_manager = DatabaseManager()
    try:
        db_manager.connect()
        # Execute a cunsult to verify if exists a user with same name
        query = 'SELECT * FROM users WHERE name = %s OR email = %s'
        data = (name, email)
        cursor = db_manager.execute_query(query, data)
        existing_user = cursor.fetchone()

        if existing_user:
            return True
        else:
            return False
    except psycopg2.Error as error:
        print("Erro ao verificar duplicatas: ", error)
        return True
    finally:
        db_manager.close()


def hash_password(password):
    password = password.encode('utf-8')
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash


class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(db_config)
            return self.conn
        except psycopg2.Error as e:
            print("Erro ao conectar ao banco de dados: ", e)
            return None

    def close(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, data=None):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(query, data)
                self.conn.commit()
                return cursor
            except psycopg2.Error as e:
                print("Erro ao executar consulta no banco de dados: ", e)
                return None


class ManagerWindow:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("Gerenciador de Usuários")

        self.users_listbox = tk.Listbox(self.window, width=50, height=20)
        self.users_listbox.pack()

        self.btn_edit = tk.Button(self.window, text="Editar Usuário", command=self.edit_user)
        self.btn_edit.pack()

        self.btn_delete = tk.Button(self.window, text="Excluir Usuário", command=self.delete_user)
        self.btn_delete.pack()

        self.btn_register = tk.Button(self.window, text="Cadastrar Usuário")
        self.btn_register.pack()

        self.load_users()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_users(self):
        try:
            self.db_manager.connect()
            self.users_listbox.delete(0, tk.END)
            cursor = self.db_manager.execute_query("SELECT id, name, email FROM users")
            if cursor:
                users = cursor.fetchall()
                for user in users:
                    self.users_listbox.insert(tk.END, f"{user[0]} - {user[1]} - {user[2]}")
            self.db_manager.close()
        except psycopg2.Error as e:
            print("Erro ao listar usuários: ", e)

    def edit_user(self):
        try:
            selected_user = self.users_listbox.get(tk.ACTIVE)
            print(f"Editando o usuário: {selected_user}")
            if not selected_user:
                tk.messagebox.showerror("Erro", "Selecione um usuário para editar.", parent=self.window)
                return
            user_id = int(selected_user.split(" - ")[0])
            edit = EditUser(user_id)
            edit.window.mainloop()
        except Exception as e:
            print("Erro ao tentar editar usuário: ", e)

    def delete_user(self):
        num_users = self.users_listbox.size()

        if num_users == 0:
            tk.messagebox.showerror("Erro", "Não há usuários para excluir.", parent=self.window)
            return
        elif num_users == 1:
            tk.messagebox.showerror("Erro", "Não é permitido excluir o único usuário.", parent=self.window)
            return

        selected_user = self.users_listbox.get(tk.ACTIVE)
        if not selected_user:
            tk.messagebox.showerror("Erro", "Selecione um usuário para excluir.", parent=self.window)
            return

        confirmed = tk.messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o usuário: {selected_user}?", parent=self.window)
        if confirmed:
            print(f"Excluindo o usuário: {selected_user}")
            user_id = int(selected_user.split(" - ")[0])
            self.db_manager.connect()
            query = "DELETE FROM users WHERE id = %s"
            data = (user_id,)
            cursor = self.db_manager.execute_query(query, data)

            if cursor:
                tk.messagebox.showinfo("Sucesso", f"Usuário {user_id}, excluido com sucesso.", parent=self.window)
                print("Usuário excluido com sucesso")
                self.load_users()
            else:
                tk.messagebox.showerror("Erro", "Erro ao excluir o usuário.", parent=self.window)

            self.db_manager.close()

    def on_closing(self):
        self.db_manager.close()
        self.window.destroy()


class EditUser:
    def __init__(self, user_id):
        self.db_manager = DatabaseManager()
        # Create window
        self.user_id = user_id
        self.window = tk.Tk()
        self.window.geometry("300x150")
        self.window.title("Editar Usuário")

        # Labels
        tk.Label(self.window, text="Nome:").grid(row=0, column=0, sticky="E")
        tk.Label(self.window, text="Email:").grid(row=1, column=0, sticky="E")
        tk.Label(self.window, text="Senha:").grid(row=2, column=0, sticky="E")
        tk.Label(self.window, text="Confirmar Senha:").grid(row=3, column=0, sticky="E")

        # Inputs
        self.name_input = tk.Entry(self.window)
        self.name_input.grid(row=0, column=1)
        self.email_input = tk.Entry(self.window)
        self.email_input.grid(row=1, column=1)
        self.password_input = tk.Entry(self.window, show="*")
        self.password_input.grid(row=2, column=1)
        self.cpassword_input = tk.Entry(self.window, show="*")
        self.cpassword_input.grid(row=3, column=1)

        # Button
        tk.Button(self.window, text="CONFIRMAR", command=self.confirm_edit).grid(row=4, column=1, pady=10)

    def confirm_edit(self):
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()
        cpassword = self.cpassword_input.get()

        if not (name and email and password and cpassword):
            tk.messagebox.showerror("Erro", "Preencha todos os campos.", parent=self.window)
            return
        if password != cpassword:
            tk.messagebox.showerror("Erro", "As senhas não coincidem.", parent=self.window)
            return
        confirmed = tk.messagebox.askyesno("Confirmação", f"Tem certeza que deseja editar o usuário?", parent=self.window)
        if confirmed:
            if check_duplicate_user(name, email):
                tk.messagebox.showerror("Erro", "Nome ou email já foram cadastrados.", parent=self.window)
            else:
                password_hash = hash_password(password)
                try:
                    self.db_manager.connect()
                    query = '''UPDATE users SET name = %s, 
                                                email = %s,
                                                password_hash = %s 
                                                WHERE id = %s'''
                    data = (name, email, password_hash, self.user_id)
                    cursor = self.db_manager.execute_query(query, data)
                    if cursor:
                        tk.messagebox.showinfo("Sucesso", "Usuário editado com sucesso.", parent=self.window)
                        print("Usuário editado com sucesso.")
                        self.window.destroy()
                    else:
                        tk.messagebox.showerror("Erro", "Erro ao editar o usuário", parent=self.window)
                except psycopg2.Error as error:
                    tk.messagebox.showerror("Erro", "Erro ao inserir os dados!", parent=self.window)
                    print("Erro ao inserir os dados: ", error)
                finally:
                    self.db_manager.close()

# manage = ManagerWindow()
# manage.window.mainloop()
