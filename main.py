
# Import necessary libraries
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

# Initialize the Flask application
app = Flask(__name__)

# Load the trained ML model
model = pickle.load(open('ml_model.pkl', 'rb'))

# Define the home route
@app.route('/')
def home():
    """Renders the home page."""
    return '''<h1>Welcome to ML Day Trading US Stocks - Long Strategy</h1>
            <p>This application uses machine learning to make long trading decisions on US stocks.
            <a href="/dashboard">Go to Dashboard</a></p>'''

# Define the dashboard route
@app.route('/dashboard')
def dashboard():
    """Renders the dashboard page."""
    return '''<h1>Dashboard</h1>
            <form method="POST" action="/predict">
                <label for="stock_symbol">Stock Symbol:</label>
                <input type="text" name="stock_symbol" id="stock_symbol">
                <br>
                <label for="start_date">Start Date:</label>
                <input type="date" name="start_date" id="start_date">
                <br>
                <label for="end_date">End Date:</label>
                <input type="date" name="end_date" id="end_date">
                <br>
                <input type="submit" value="Predict">
            </form>'''

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    """Predicts the stock price using ML model."""

    # Get the stock symbol, start date, and end date from the request
    stock_symbol = request.form['stock_symbol']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Load the stock data
    stock_data = pd.read_csv(f'stock_data/{stock_symbol}.csv')

    # Filter the stock data by the start and end dates
    stock_data = stock_data[(stock_data['Date'] >= start_date) & (stock_data['Date'] <= end_date)]

    # Prepare the data for prediction
    features = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
    target = stock_data['Close']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train the ML model
    model.fit(X_train, y_train)

    # Make a prediction
    prediction = model.predict(X_test)

    # Evaluate the model
    score = model.score(X_test, y_test)

    # Return the prediction and score in JSON format
    return jsonify({'prediction': prediction.tolist(), 'score': score})

# Main function
if __name__ == '__main__':
    app.run(debug=True)
