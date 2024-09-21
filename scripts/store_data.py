import sqlite3
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# Use absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '../data/stock_data.db')
SQL_PATH = os.path.join(BASE_DIR, '../models/create_tables.sql')


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
        with open(SQL_PATH, 'r') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def insert_stock_data(conn, stock_data):
    """ Insert stock data into the stock_data table """
    sql = ''' INSERT INTO stock_data(ticker, date_time, open_price, high_price, low_price, close_price, volume)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, stock_data)
    conn.commit()

def fetch_and_store_data(ticker):
    """ Fetch stock data from Yahoo Finance and store it in the database """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d", interval="1m")  # Fetch real-time minute-by-minute data
    
    # Prepare data for insertion into the database
    stock_data = [
        (ticker, row.name.strftime('%Y-%m-%d %H:%M:%S'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
        for index, row in hist.iterrows()
    ]
    
    # Create a connection and insert data
    conn = create_connection()
    if conn:
        insert_stock_data(conn, stock_data)
        conn.close()

def visualize_stock_data(ticker):
    """ Visualize stock prices from the database """
    conn = create_connection()
    if conn:
        query = f"SELECT date_time, close_price FROM stock_data WHERE ticker='{ticker}'"
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Convert date_time to datetime for plotting
        df['date_time'] = pd.to_datetime(df['date_time'])

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(df['date_time'], df['close_price'], marker='o', linestyle='-', color='b')
        plt.title(f'Stock Prices for {ticker}')
        plt.xlabel('Date and Time')
        plt.ylabel('Close Price')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    ticker = 'AAPL'  # Example: Fetch and store Apple's stock data
    fetch_and_store_data(ticker)
    visualize_stock_data(ticker)