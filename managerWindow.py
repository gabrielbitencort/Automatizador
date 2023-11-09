import tkinter as tk
import tkinter.messagebox
import psycopg2

db_config = "dbname=automatizador user=postgres password=mpti3562 host=127.0.0.1"


class ManagerWindow():
    def __init__(self):
        users = self.load_users()
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("Gerenciador de Usuários")

        self.users_listbox = tk.Listbox(self.window)
        for user in users:
            self.users_listbox.insert(tk.END, user[0] + " - " + user[1])
        self.users_listbox.pack()

        self.edit_button = tk.Button(self.window, text="Editar Usuário", command=self.edit_user)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.window, text="Excluir Usuário", command=self.delete_user)
        self.delete_button.pack()

    @staticmethod
    def load_users():
        try:
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT name, email FROM users")
            users = cursor.fetchall()
            print(users)
            return users
        except psycopg2.Error as error:
            print("Erro ao carregar usuários: ", error)
            return []

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


manage = ManagerWindow()
manage.window.mainloop()
