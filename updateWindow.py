import tkinter as tk
import tkinter.messagebox
import requests
import json


# import subprocess


class UpdateSoftware:
    def __init__(self):
        # Create a update window
        self.window = tk.Tk()
        self.window.geometry('300x100')
        self.window.title("Verificar Atualizações")

        # Create update window widgets
        self.status_info = tk.Label(self.window, text="")
        self.btn_verify = tk.Button(self.window, text="VERIFICAR", command=self.verify_updates)

        # Widgtes positions
        self.status_info.place(x=10, y=30)
        self.btn_verify.place(x=110, y=50)

        self.center_window(300, 100)

    def verify_updates(self):
        # Verify updates
        latest_version = self.check_for_updates()
        if latest_version:
            current_version = 'v1.1.0-beta'
            if latest_version == current_version:
                tk.messagebox.showinfo("Atualização Disponivel", "Você já possui a versão mais recente.", parent=self.window)
            else:
                self.ask_for_update(latest_version)

    def check_for_updates(self):
        repo_owner = 'Gabriel-Bitencort'
        repo_name = 'Automatizador-V2.0'
        releases_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases'

        headers = {"Authorization": "token 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"}

        try:
            response = requests.get(releases_url, headers=headers)
            print("Procurando atualização...")
            print("Status da resposta: ", response.status_code)
            if response.status_code == 200:
                data = json.loads(response.text)
                # Verify if exists a pre-release
                if data and len(data) > 0:
                    # Acess the first release from list
                    latest_release = data[0]
                    if latest_release.get('prerelease'):
                        print("A versão mais recente é uma pre-release.")
                    else:
                        latest_version = latest_release.get('tag_name')
                        print(f"Atualização encontrada: {latest_version}")
                        return latest_version
            else:
                tk.messagebox.showinfo("Erro na atualização", "Não foi possivel se comunicar com o servidor", parent=self.window)
                self.close()
        except Exception as e:
            print("Erro ao verificar atualizações: ", str(e))
            self.close()

        return None

    def ask_for_update(self, latest_version):
        result = tk.messagebox.askquestion("Atualização Disponivel",
                                           f"Uma atualização ({latest_version}) está disponivel. Deseja atualizar?", parent=self.window)
        if result == 'yes':
            print("Atualizando...")

    def close(self):
        self.window.destroy()

    # Centralize the window
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
