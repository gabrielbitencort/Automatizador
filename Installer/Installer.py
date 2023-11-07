import os
import zipfile
import ctypes
import sys
from win32com.client import Dispatch


# Verifica se o programa está sendo executado com privilégios de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# Define o diretório de instalação
install_dir = os.path.join(os.environ['ProgramFiles'], 'Automatizador')

# Nome do arquivo ZIP
zip_file = 'Automatizador-v1.1.0-beta.zip'

# Nome do atalho na área de trabalho
shortcut_name = 'Automatizador.lnk'

# Caminho para o executável após a instalação
executable_path = os.path.join(install_dir, 'dist', 'Automatizador', 'Automatizador.exe')


def main():
    # Verifica os privilégios de administrador
    if is_admin():
        # Extrai o arquivo ZIP
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(install_dir)

        # Cria um atalho na área de trabalho
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shortcut_target = executable_path
        shortcut_path = os.path.join(desktop, shortcut_name)
        create_shortcut(shortcut_target, shortcut_path)

        print('Instalação concluída.')
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
    main()
