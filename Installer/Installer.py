import os
import zipfile
import ctypes
import sys
from win32com.client import Dispatch
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


# Verifica se o programa está sendo executado com privilégios de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except OSError:
        return False


# Define o diretório de instalação
install_dir = os.path.join(os.environ['ProgramFiles'], 'Automatizador')

# Nome do arquivo ZIP
zip_file = 'Automatizador-v1.2.0-beta.zip'

# Nome do atalho na área de trabalho
shortcut_name = 'Automatizador.lnk'

# Caminho para o executável após a instalação
executable_path = os.path.join(install_dir, 'Automatizador.exe')


class NoTabsNotebook(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        ttk.Notebook.__init__(self, *args, **kwargs)
        style = ttk.Style()
        style.layout("TNotebook", [])


class Installer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x350")
        self.window.resizable(False, False)
        self.window.iconbitmap('installation.ico')
        self.window.title("Automatizador - Programa de Instalação")

        # Criar um notebook para abas
        self.notebook = NoTabsNotebook(self.window)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        # Criar e adicionar a aba de introdução
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1)

        self.create_introduction_tab()

        # Frame com botões
        self.frame_btn = tk.Frame(self.window, background='#CCCCCC')
        self.frame_btn.grid(row=1, column=0, sticky='ew')

        self.btn_cancel = tk.Button(self.frame_btn, text="Cancelar", width=10, command=self.cancel)
        self.btn_cancel.pack(side='right', padx=10, pady=6)
        self.btn_next = tk.Button(self.frame_btn, text="Avançar >", width=10, command=self.next_tab)
        self.btn_next.pack(side='right', padx=10, pady=6)
        self.btn_back = tk.Button(self.frame_btn, text="< Voltar", width=10, command=self.go_back)
        self.btn_back.pack(side='right', padx=1, pady=6)
        self.btn_back.grid_remove()

        # Configurar grid para expandir conforme a janela é redimensionada
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Centraliza a janela
        self.center_window(500, 350)

    def create_introduction_tab(self):
        # Frame com titulo
        self.frame_title = tk.Frame(self.tab1)
        self.frame_title.grid(row=0, column=0, sticky='nsew')

        # Frame com texto
        self.frame_text = tk.Frame(self.tab1)
        self.frame_text.grid(row=1, column=0, sticky='nsew')

        self.title = tk.Label(self.frame_title, text="Bem-vindo ao Assistente de Instalação do Automatizador")
        self.title.pack(side='top', fill='both', padx=10, pady=20)

        self.text = tk.Label(self.frame_text, text="Este Assistente vai instalar o Automatizador no seu computador.\n\n"
                                                   "Recomenda-se fechar todos os outros programas antes de continuar.\n\n"
                                                   "Clique Avançar para continuar, ou Cancelar para sair do Programa de Instalação.",
                             justify=tk.LEFT)
        self.text.pack(side='top', padx=10, pady=10, anchor='w')

    def create_license_agreement(self):
        pass

    def next_tab(self):
        # Lógica para mudar de aba
        current_tab_index = self.notebook.index(self.notebook.select())
        next_tab_index = current_tab_index + 1

        if next_tab_index < self.notebook.index("end"):
            self.notebook.select(next_tab_index)
            self.btn_back.grid()
        else:
            print("Não há mais abas disponíveis.")
            self.btn_back.grid_remove()

    def go_back(self):
        # Lógica para voltar à aba anterior
        current_tab_index = self.notebook.index(self.notebook.select())
        previous_tab_index = current_tab_index - 1

        if previous_tab_index >= 0:
            self.notebook.select(previous_tab_index)
            if previous_tab_index == 0:
                self.btn_back.grid_remove()
        else:
            print("Não há aba anterior.")

    # Cancela a instalação
    def cancel(self):
        confirm = tk.messagebox.askyesno("Cancelar Instalação", "Tem certeza que deseja cancelar a instalação?",
                                         parent=self.window)
        if confirm:
            self.window.destroy()

    # Centraliza a janela
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")


def main():
    # Verifica os privilégios de administrador
    if is_admin():
        try:
            # Extrai o arquivo ZIP
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(install_dir)

            # Cria um atalho na área de trabalho
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            shortcut_target = executable_path
            shortcut_path = os.path.join(desktop, shortcut_name)
            create_shortcut(shortcut_target, shortcut_path)
            tk.messagebox.showinfo("Instalador", "Instalação concluída")
            print('Instalação concluída.')
        except FileNotFoundError as e:
            print(f"Arquivo zip não encontrado: {e}")
    else:
        # Se não estiver executando como administrador, solicita elevação de privilégios
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


# Função para criar um atalho na área de trabalho
def create_shortcut(target, shortcut):
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut)
    shortcut.TargetPath = target
    shortcut.save()


if __name__ == '__main__':
    installer = Installer()
    installer.window.mainloop()
