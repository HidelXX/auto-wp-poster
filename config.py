from dotenv import load_dotenv
import os

load_dotenv()

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
EXCEL_PATH = os.getenv("EXCEL_PATH")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
LIMITE_PRODUTOS = 250