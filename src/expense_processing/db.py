import psycopg

from expense_processing.config import DB_CONFIG

def get_connection():
    return psycopg.connect(**DB_CONFIG)