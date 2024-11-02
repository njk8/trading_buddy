import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

# Path to save images
IMAGE_PATH = '/opt/airflow/data/visualizations/'  # Ensure this folder is created and accessible

# Function to fetch stock data from the database
def fetch_stock_data(ticker):
    conn = sqlite3.connect('/opt/airflow/data/processed/stock_data.db')  # Adjust path if needed
    query = """
        SELECT date_time, close_price
        FROM stock_data
        WHERE ticker = ?
        ORDER BY date_time ASC
    """
    stock_data = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    return stock_data

# Function to save the stock data plot as an image
def save_stock_data_plot(ticker):
    # Fetch the latest stock data
    stock_data = fetch_stock_data(ticker)
    
    if not stock_data.empty:
        # Convert date_time column to datetime for plotting
        stock_data['date_time'] = pd.to_datetime(stock_data['date_time'])
        
        # Create and save the plot
        fig, ax = plt.subplots()
        ax.plot(stock_data['date_time'], stock_data['close_price'], label='Close Price')
        
        # Formatting
        ax.set_title(f'Real-time Stock Price of {ticker}')
        ax.set_xlabel('Date Time')
        ax.set_ylabel('Close Price')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"{IMAGE_PATH}{ticker}_stock_price_{timestamp}.png"
        plt.savefig(file_path)
        plt.close(fig)
        print(f"Plot saved: {file_path}")
    else:
        print(f"No data found for ticker {ticker}")

# Main function to save a plot for a specific stock ticker
if __name__ == "__main__":
    ticker = 'AAPL'  # Example: Apple stock
    save_stock_data_plot(ticker)
