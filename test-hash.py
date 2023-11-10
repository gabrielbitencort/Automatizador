import psycopg2

db_config = "dbname=automatizador user=postgres password=mpti3562 host=127.0.0.1"

conn = psycopg2.connect(db_config)
try:
    if conn:
        print("Conectado")
except psycopg2.Error as e:
    print("Erro: ", e)