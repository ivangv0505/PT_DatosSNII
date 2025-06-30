import os
import psycopg2

def conexion():
    return psycopg2.connect(
        dbname   = os.getenv("DB_NAME", "datossnii"),
        user     = os.getenv("DB_USER", "postgres"),
        password = os.getenv("DB_PASS", "pt050505"),
        host     = os.getenv("DB_HOST", "localhost"),
        port     = os.getenv("DB_PORT", "5432"),
    )