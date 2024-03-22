import pandas as pd
import numpy as np
import streamlit as st
import joblib
import seaborn as sns
import xgboost
import matplotlib.pyplot as plt
import os


# Load model and preprocessing artifacts
script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'stock_price_prediction.joblib')

# Load the file using the absolute path
artifact = joblib.load(file_path)

# Function to check missing inputs
def check_missing_inputs(data):
    return [key for key, value in data.items() if value == '']

# Function to make predictions
def predict(data):
    df = pd.DataFrame([data])
    X_data = pd.DataFrame(artifact['preprocessing'].transform(df), columns=artifact['preprocessing'].get_feature_names_out())

    # Display loading indicator
    with st.spinner("Predicting..."):
        prediction = artifact['model'].predict(X_data)

    predicted_close = prediction

    return X_data, predicted_close  # Return X_data along with the price


# Data Input Page
def input_page():
    st.markdown("<h1 style='text-align: center; font-size: 24px;'>Get A Prediction Of Tomorrow's Closing Price</h1>",
                 unsafe_allow_html=True)


    #User Inputs
    symbol = st.selectbox('Select Stock Symbol', options=['', 'INTC', 'AMD', 'TSLA', 'MARA', 'AMZN'])
    open_price = st.number_input('Open', value=0.0)
    high = st.number_input('High', value=0.0)
    low = st.number_input('Low', value=0.0)
    close_price = st.number_input("Today's Close", value=0.0)
    volume = st.number_input('Volume', value=0.0)
    hl = high - low  # High-Low
    oc = open_price - close_price  # Open-Close
    day_of_week = st.selectbox('Day Of Week', options=['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    month = st.selectbox('Month', options=['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    
    ##
    user_input = {
        'Symbol': symbol,
        'Open': open_price,
        'High': high,
        'Low': low,
        'Close': close_price,
        'Volume': volume,
        'H-L': hl,
        'O-C': oc,
        'DayOfWeek': day_of_week,
        'Month': month
    }

    # Button to make prediction
    if st.button('Predict'):
        missing_fields = check_missing_inputs(user_input)
        if missing_fields:
            st.error(f"Please fill in the following fields: {', '.join(missing_fields)}")
        else:
            X_data, result = predict(user_input)
            predicted_price = artifact["model"].predict(X_data)[0]
            st.success(f"Predicted Tomorrow's Close Price: {predicted_price:.2f}")
