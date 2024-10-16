import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import time

# Function to fetch stock data from the database
def fetch_stock_data(ticker):
    conn = sqlite3.connect('../data/stock_data.db')  # Adjust path as necessary
    query = f"""
        SELECT date_time, close_price
        FROM stock_data
        WHERE ticker = ?
        ORDER BY date_time ASC
    """
    stock_data = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    return stock_data

# Function to plot the stock data in real-time
def plot_stock_data(ticker):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    ax.set_title(f'Real-time Stock Price of {ticker}')
    ax.set_xlabel('Date Time')
    ax.set_ylabel('Close Price')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    try:
        while True:
            # Fetch the latest stock data
            stock_data = fetch_stock_data(ticker)
            
            if not stock_data.empty:
                # Convert date_time column to datetime for plotting
                stock_data['date_time'] = pd.to_datetime(stock_data['date_time'])

                # Clear the previous plot
                ax.clear()

                # Plot the new data
                ax.plot(stock_data['date_time'], stock_data['close_price'], label='Close Price')

                # Formatting
                ax.set_title(f'Real-time Stock Price of {ticker}')
                ax.set_xlabel('Date Time')
                ax.set_ylabel('Close Price')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.draw()  # Update the plot

            else:
                print(f"No data found for ticker {ticker}")
            
            plt.pause(60)  # Pause for 60 seconds before updating the plot
            
            # Check if the figure is closed, and break the loop
            if not plt.fignum_exists(fig.number):
                print("Plot window closed. Exiting.")
                break

            time.sleep(60)  # Fetch new data every 60 seconds

    except KeyboardInterrupt:
        print("Script interrupted. Exiting.")

    finally:
        plt.ioff()  # Turn off interactive mode
        plt.close()  # Close the plot

# Main function to visualize data for a specific stock ticker
if __name__ == "__main__":
    ticker = 'AAPL'  # Example: Apple stock (replace with your desired stock ticker)
    plot_stock_data(ticker)
