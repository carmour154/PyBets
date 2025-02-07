import streamlit as st
import pandas as pd

def dashboard():  
    st.title('Todays Best Bets')
    df = pd.read_csv('best_bets.csv')

    # Function to apply background color
    def highlight(x):
        return 'background-color: lightgreen' if x > 0 else 'background-color: #FFCCCC'

    # Apply the function to the 'expected_value' column
    df = df.style.applymap(highlight, subset=['expected_value'])

    st.write(df)