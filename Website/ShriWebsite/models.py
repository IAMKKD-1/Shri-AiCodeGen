import os
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

load_dotenv()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
port = os.environ.get("POSTGRES_PORT")  
database = os.environ.get("POSTGRES_DATABASE")

def create_table(table, columns):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        cur.execute(f'CREATE TABLE IF NOT EXISTS {table} {columns};')
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as err:
        print("Error:", err)
        return False

def insert_data(insert_query, data):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        cur.execute(insert_query, data)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as err:
        print("Error:", err)
        return False
    
def get_data(query):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except psycopg2.Error as err:
        print("Error:", err)
        return False
    
def update_data(update_query, data):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        cur.execute(update_query, data)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as err:
        print("Error:", err)
        return False
