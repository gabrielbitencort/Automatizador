from settings import getDatabaseUrl
import psycopg2

db_config = getDatabaseUrl()

def testConection():
    try:
        # conecta ao banco de dados
        conn = psycopg2.connect(db_config)

        # criar um cursor
        cursor = conn.cursor()

        # fecha o cursor e a conexão
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Erro: {e}")


testConection()
