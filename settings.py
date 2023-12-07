import logging
import sys
import os

if getattr(sys, 'frozen', False):
    scriptDir = os.path.dirname(sys.executable)
else:
    scriptDir = os.path.dirname(__file__)
envPath = os.path.join(scriptDir, 'settings.env')

from dotenv import load_dotenv

load_dotenv(envPath)

DB_NAME = os.environ.get('DB_NAME', default='')
DB_USER = os.environ.get('DB_USER', default='')
DB_PASSWORD = os.environ.get("DB_PASSWORD", default='')
DB_HOST = os.environ.get("DB_HOST", default='localhost')


def getDatabaseUrl():
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

def createDefaultLogging(scriptDir):
    logFile = os.path.join(scriptDir, 'logs', f"{os.path.basename(sys.executable)}.log")

    os.makedirs(os.path.join(scriptDir, 'logs'), exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logFile),
            logging.StreamHandler()
        ]
    )
