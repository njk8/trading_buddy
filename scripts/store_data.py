import sqlite3

# Path to the SQLite database
DATABASE_PATH = '../data/stock_data.db'

def create_connection():
    """ Create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        print(f"Connected to the database at {DATABASE_PATH}")
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
    return conn

def create_tables(conn):
    """ Create tables using the SQL schema """
    try:
        with open('../models/create_tables.sql', 'r') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

if __name__ == '__main__':
    # Create a connection to the database
    conn = create_connection()

    # If connection is successful, create the tables
    if conn:
        create_tables(conn)
        conn.close()
