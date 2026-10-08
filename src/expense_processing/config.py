import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "expenses"),
    "user": os.getenv("POSTGRES_USER", "expense_user"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}
DATA_FOLDER = os.getenv("DATA_FOLDER", "data")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()