import psycopg2

db_config = "dbname=automatizador user=postgres password=senha host=127.0.0.1"

conn = psycopg2.connect(db_config)
try:
    if conn:
        print("Conectado")
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM smtp')
            print("Deletado")
        except psycopg2.Error as e:
            print("Erro: ", e)
except psycopg2.Error as e:
    print("Erro: ", e)