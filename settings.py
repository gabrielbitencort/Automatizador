import os

scriptDir = os.path.dirname(os.path.abspath(__file__))
envPath = os.path.join(scriptDir, 'settings.env')

from dotenv import load_dotenv
load_dotenv(envPath)

DB_NAME = os.environ.get('DB_NAME', default='')
DB_USER = os.environ.get('DB_USER', default='')
DB_PASSWORD = os.environ.get("DB_PASSWORD", default='')
DB_HOST = os.environ.get("DB_HOST", default='localhost')

print(f"Nome: {DB_NAME}\nUsuário: {DB_USER}\nSenha: {DB_PASSWORD}\nHost: {DB_HOST}\n")

def getDatabaseUrl():
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
