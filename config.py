from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

CHROMEDRIVER_PATH = Path(os.getenv("CHROMEDRIVER_PATH"))
EXCEL_PATH = Path(os.getenv("EXCEL_PATH"))
IMAGENS_PATH = Path(os.getenv("IMAGENS_PATH"))

WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_LOGIN_URL = os.getenv("WP_LOGIN_URL")
WP_NOVA_POSTAGEM_URL = os.getenv("WP_NOVA_POSTAGEM_URL")

LIMITE_PRODUTOS = 304