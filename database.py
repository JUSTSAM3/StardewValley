import psycopg2
from psycopg2 import sql
import os

DB_NAME = "stardew"
DB_USER = "postgres"
DB_PASSWORD = "sistemas2024"
DB_HOST = "192.168.56.101"
DB_PORT = "5432"


# Crea la base de datos si no existe
def create_database_if_not_exists():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        exists = cur.fetchone()

        if not exists:
            print(f"[INFO] La base '{DB_NAME}' no existe. Creándola...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        else:
            print(f"[OK] Base '{DB_NAME}' ya existe.")

        cur.close()
        conn.close()

    except Exception as e:
        print("[ERROR] No fue posible verificar/crear la base:", e)


# Obtiene conexión normal a la BD
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# Crea tablas a partir del schema.sql
def initialize_tables():
    try:
        conn = get_connection()
        cur = conn.cursor()

        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

        with open(schema_path, "r", encoding="utf8") as f:
            sql_commands = f.read()

        cur.execute(sql_commands)
        conn.commit()

        print("[OK] Tablas creadas o ya existentes.")
        cur.close()
        conn.close()

    except Exception as e:
        print("[ERROR] No se pudieron crear las tablas:", e)
