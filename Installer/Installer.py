import os
import requests
# import zipfile
import py7zr
import platform

# GitHub latest release URL
github_repo = 'Gabriel-Bitencort/Automatizador-V2.0'
github_api_url = f'https://api.github.com/repos/{github_repo}/releases/latest'
headers = {"Authorization": "token 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"}

# Instalation directory
install_dir = os.path.join(os.environ['PROGRAMFILES'], 'Automatizador')

try:
    # Get the latest release information
    response = requests.get(github_api_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    latest_release_url = data['assets'][0]['browser_download_url']
    print(latest_release_url)

    # .7z file name
    compressed_file = 'Automatizador-v1.1.0-beta.7z'

    # Download .7z file
    with open(compressed_file, 'wb') as file:
        file.write(response.content)

    # unzip file
    with py7zr.SevenZipFile(compressed_file, 'r') as z:
        z.extractall(install_dir)

    # Verify OS to create a shortcut
    if platform.system() == 'Windows':
        import winshell
        from win32com.client import Dispatch

        # Create a shortcut
        desktop = winshell.desktop()
        shortcut = os.path.join(desktop, "Automatizador.ink")
        target = os.path.join(install_dir, 'dist', 'Automatizador', 'Automatizador.exe')
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut)
        shortcut.Targetpath = target
        shortcut.WorkngDirectory = os.path.dirname(target)
        shortcut.save()

    print("Instalação concluida.")
except requests.exceptions.RequestException as e:
    print(f"Erro na solicitação HTTP: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
