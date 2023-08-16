import streamlit as st
from simulator import CryptoSimulator
from matplotlib import pyplot as plt
import numpy as np
## Get historical Data



sidebar = st.sidebar
st.set_page_config(page_title="Cryptocurrecny Investment Analysis App", layout="wide")
test_start = sidebar.selectbox("Back Testing Start Year",options= list(range(2015,2024)), index=len(list(range(2015,2024)))-4)
test_end = sidebar.selectbox("Back Testing End Year",list(range(2015,2024)), index=len(list(range(2015,2024)))-1)
submit = sidebar.button("Start Back Testing")

if test_end < test_start:
    test_end = test_start + 1



if submit:
    coin_list = ['bitcoin', 'litecoin', 'ethereum']
    cs = CryptoSimulator(coin_list=coin_list)
    histories = cs.get_historical_data()
    num_row = len(coin_list) // 3
    last_col = len(coin_list) % 3
    st.markdown("### Historical Price Data")
    for j, coin in enumerate(coin_list):
        if j % 3 == 0:
            cols = st.columns(3)
        with cols[j%3]:
            fig, ax = plt.subplots()
            ax.plot(histories[j].iloc[:,0])
            ax.set_title(f"{coin.title()} Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            st.pyplot(fig)
    
    st.markdown("### Strategy By Golden Cross and Death Cross")
    total_profit, profit_histories, figures = cs.simulation(start_year=test_start, end_year=test_end)
    for j, coin in enumerate(coin_list):
        if j % 3 == 0:
            cols = st.columns(3)
        with cols[j%3]:
            st.pyplot(figures[j])
    
    st.markdown("### Accumulated Return")
    for j, coin in enumerate(coin_list):
        if j % 3 == 0:
            cols = st.columns(3)
        with cols[j%3]:
            fig, ax = plt.subplots()
            ax.set_title(f"{coin.title()} Accumulated Return")
            ax.plot(profit_histories[j]-1)
            ax.set_xlabel("Date")
            ax.set_ylabel("Return")
            st.pyplot(fig)
            st.write(f"Accumulate Return: {total_profit[j]*100}%")
    

