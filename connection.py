import sqlite3

def bd():
    conn = sqlite3.connect('meu_banco_de_dados.db')
    cursor = conn.cursor()

    return conn, cursor

def create_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        nome TEXT,
        code INTEGER
    )
    ''')

def select_data(conn, cursor, code):
    cursor.execute(f'SELECT id FROM users WHERE code = {code}')
    voucher_id = cursor.fetchone()  
    conn.close()

    if voucher_id:
        return voucher_id[0]  
    else:
        return None  
