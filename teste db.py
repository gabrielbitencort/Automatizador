import psycopg2

try:
    conn = psycopg2.connect(database='automatizador',
                            user='postgres',
                            host='127.0.0.1',
                            password='mpti3562',
                            port=5432)
    if conn:
        print("Conectado no banco de dados.")
        try:
            print("Criando tabela.")
            cur = conn.cursor()
            cur.execute("""CREATE TABLE users(id SERIAL PRIMARY KEY, name VARCHAR(50) UNIQUE NOT NULL, email VARCHAR(50) UNIQUE NOT NULL);""")
            conn.commit()
            cur.close()
            conn.close()
            print("Tabela criada.")
        except psycopg2.Error as e:
            print("Não foi possivel criar tabela: ", e)


except psycopg2.Error as e:
    print("Não foi possivel conectar ao banco de dados: ", e)
