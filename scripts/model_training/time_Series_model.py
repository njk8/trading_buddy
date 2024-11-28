import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error,mean_absolute_error
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv


# Construct the path to the database
BASE_DIR = r'C:\Users\91940\Documents\Trade_buddy\scripts'
DB_PATH = os.path.join(BASE_DIR, 'C:/Users/91940/Documents/Trade_buddy/data/processed/stock_data.db')

# Normalize the path to handle '..'
DB_PATH = os.path.normpath(DB_PATH)

TICKER = 'AAPL'
PLOT_PATH = 'C:/Users/91940/Documents/Trade_buddy/data/model_outputs/'

# Fetch stock data
def fetch_stock_data(ticker):
    # Print to confirm the correct path
    print("Database Path:", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT date_time, close_price
        FROM stock_data_transformed
        WHERE ticker = ?
        ORDER BY date_time ASC
    """
    data = pd.read_sql(query, conn, params=(ticker,))
    conn.close()
    
    # Convert date_time to datetime and set as index
    data['date_time'] = pd.to_datetime(data['date_time'])
    data.set_index('date_time', inplace=True)
    
    data = data[~data.index.duplicated(keep='first')]
    data = data.asfreq('min', method='ffill')  # 'T' for minute-level frequency

    return data

# Train-test split
def train_test_split(data, test_size=0.2):
    split_idx = int(len(data) * (1 - test_size))
    train, test = data.iloc[:split_idx], data.iloc[split_idx:]
    print(len(data),len(test))
    #plot_acf(train)
    #plot_pacf(train)
    #plt.show()
    return train, test

# Model training and prediction
def train_and_predict(train, test, p=2, d=1, q=10):
    # Train ARIMA model
    model = ARIMA(train, order=(p, d, q))
    fitted_model = model.fit()
    print(f"ARIMA model fitted with order ({p}, {d}, {q})")

    # Predict on test data
    test_pred = fitted_model.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)
    
    # Calculate performance metrics
    mse = mean_squared_error(test, test_pred)
    mae = mean_absolute_error(test, test_pred)
    mape = np.mean(np.abs((test - test_pred) / test)) * 100  # Mean Absolute Percentage Error
    rmspe = np.sqrt(np.mean(np.square((test - test_pred) / test))) * 100  # Root Mean Squared Percentage Error

    # Print performance metrics
    print(f"Test Mean Squared Error (MSE): {mse:.2f}")
    print(f"Test Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Test Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    print(f"Test Root Mean Squared Percentage Error (RMSPE): {rmspe:.2f}%")

    # Future forecast
    future_steps = 2  # Define steps for future prediction
    future_pred = fitted_model.forecast(steps=future_steps)

    return test_pred, future_pred, mse, mae, mape, rmspe

def train_and_predict_sarimax(train, test, p=1, d=1, q=1, P=1, D=1, Q=1, s=1440):
    """
    Train SARIMA model on the given train data and predict test and future values.
    
    Args:
        train (pd.Series): Training time series data.
        test (pd.Series): Test time series data.
        p, d, q (int): Non-seasonal ARIMA parameters.
        P, D, Q, s (int): Seasonal parameters and seasonal period.
    
    Returns:
        tuple: Test predictions, future predictions, test MSE.
    """
    # Train the SARIMAX model
    model = SARIMAX(train, order=(p, d, q), seasonal_order=(P, D, Q, s))
    fitted_model = model.fit(disp=False)
    print(f"SARIMA model fitted with order ({p}, {d}, {q}) and seasonal order ({P}, {D}, {Q}, {s})")
    
    # Predict on test data
    test_pred = fitted_model.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)
    mse = mean_squared_error(test, test_pred)
    print(f"Test Mean Squared Error: {mse:.2f}")
    
    # Future forecast
    future_steps = 5  # Define steps for future prediction
    future_pred = fitted_model.forecast(steps=future_steps)
    
    return test_pred, future_pred, mse

# Visualization
def plot_predictions(train, test, test_pred, future_pred):
    plt.figure(figsize=(10, 6))
    plt.plot(train.index, train, label='Train Data', color='blue')
    plt.plot(test.index, test, label='Test Data', color='green')
    plt.plot(test.index, test_pred, label='Test Predictions', color='orange')
    future_index = pd.date_range(test.index[-1] + pd.Timedelta(days=1), periods=len(future_pred), freq='min')
    plt.plot(future_index, future_pred, label='Future Forecast', color='red')

    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f"{TICKER} Stock Price Prediction")
    plt.legend()
    plt.tight_layout()
    file_path = f"{PLOT_PATH}{TICKER}_stock_prediction_{datetime.now().strftime('%Y%m%d')}.png"
    plt.savefig(file_path)
    plt.show()
    print(f"Plot saved at {file_path}")

# Module for RAG invocation
def invoke_rag_prompt(context: str, question: str):
    # Load variables from the .env file
    load_dotenv()

    # Get the API key
    api_key = os.getenv("GROQ_API_KEY")
    if api_key is None:
        raise EnvironmentError("GROQ_API_KEY not found in the environment.")
    os.environ["GROQ_API_KEY"] = api_key

    chat_model = ChatGroq(model="llama3-8b-8192") #CHOOSING THE CHAT MODEL

    """Invokes the RAG prompt with a given context and question."""
    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a world-class stock analyst and a helpful assistant. Make it in two paragraphs and Use the following context when responding:\n\n{context}."),
        ("human", "{question}")
    ])
    rag_chain = rag_prompt | chat_model | StrOutputParser()
    return rag_chain.invoke({"context": context, "question": question})

def generate_context(mse, mae, mape, rmspe):
    """Generates the context string for the RAG model based on metrics."""
    return f"""
    Stock Analysis Report:
    - Model: ARIMA
    - MSE: {mse:.2f}
    - MAE: {mae:.2f}
    - MAPE: {mape:.2f}%
    - RMSPE: {rmspe:.2f}%
    """


# Main execution
if __name__ == "__main__":
    stock_data = fetch_stock_data(TICKER)

    # Ensure there are enough data points
    if len(stock_data) < 20:  # Arbitrary threshold to ensure meaningful analysis
        print("Not enough data points for training and testing,",{len(stock_data)})
    else:
        train, test = train_test_split(stock_data['close_price'])
        test_pred, future_pred, mse, mae, mape, rmspe = train_and_predict(train, test)
        #test_pred, future_pred, mse = train_and_predict_sarimax(train, test, p=2, d=1, q=1, P=1, D=1, Q=1, s=1440)
        print('Predictions computed')
        plot_predictions(train, test, test_pred, future_pred)

        # Generate RAG context and invoke prompt
        SOURCE = generate_context(mse, mae, mape, rmspe)
        rag_response = invoke_rag_prompt(SOURCE, "What do you think about the ARIMA model performance for this stock and whether you recommend buying?")
        
        print("\nRAG Response:")
        print(rag_response)


