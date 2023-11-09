import tkinter as tk
import tkinter.messagebox
import psycopg2

db_config = "dbname=automatizador user=postgres password=mpti3562 host=127.0.0.1"

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

    def delete_user(self, user_id):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                self.conn.commit()
            except psycopg2.Error as e:
                print("Erro ao excluir usuário: ", e)
                return None


class ManagerWindow:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("Gerenciador de Usuários")

        self.users_listbox = tk.Listbox(self.window)
        self.users_listbox.pack()

        self.edit_button = tk.Button(self.window, text="Editar Usuário", command=self.edit_user)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.window, text="Excluir Usuário", command=self.delete_user)
        self.delete_button.pack()

        self.load_users()

    def load_users(self):
        self.db_manager.connect()
        cursor = self.db_manager.execute_query("SELECT id, name, email FROM users")
        if cursor:
            users = cursor.fetchall()
            for user in users:
                self.users_listbox.insert(tk.END, f"{user[0]} - {user[1]} - {user[2]}")
        self.db_manager.close()

    def edit_user(self):
        selected_user = self.users_listbox.get(tk.ACTIVE)
        if not selected_user:
            tk.messagebox.showerror("Erro", "Selecione um usuário para editar.")
            return
        print(f"Editando o usuário: {selected_user}")

    def delete_user(self):
        selected_user = self.users_listbox.get(tk.ACTIVE)
        if not selected_user:
            tk.messagebox.showerror("Erro", "Selecione um usuário para excluir.")
            return
        confirmed = tk.messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o usuário: {selected_user}")
        if confirmed:
            print(f"Excluindo o usuário: {selected_user}")
            user_id = int(selected_user.split(" - ")[0])
            self.db_manager.connect()
            if self.db_manager.delete_user(user_id):
                tk.messagebox.showinfo("Sucesso", f"Usuário {user_id}, excluido com sucesso.")
                self.load_users()
                print("Usuário excluido com sucesso")
            else:
                tk.messagebox.showerror("Erro", "Erro ao excluir o usuário.")
        self.db_manager.close()


manage = ManagerWindow()
manage.window.mainloop()
