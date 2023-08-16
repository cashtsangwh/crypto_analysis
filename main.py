import streamlit as st
from simulator import CryptoSimulator
from matplotlib import pyplot as plt
import numpy as np
import json


sidebar = st.sidebar
st.set_page_config(page_title="Cryptocurrecny Investment Analysis App", layout="wide")
st.markdown("# Cryptocurrecny Investment Analysis App")
number = sidebar.selectbox("Number of Cryptocurrency",options= list(range(1,16)), index=0)
strategy = sidebar.selectbox("Choose Strategy",options= ["cross", "crossRSI", "simple_buy_hold"], index=0)

short = 0
long = 0
days = 0

if strategy == "cross":
    short=sidebar.selectbox("Choose Days Short Moving Average",options= list(range(5,155,5)), index=0)
    long=sidebar.selectbox("Choose Days Long Moving Average",options= list(range(5,155,5)), index=0)
elif strategy == "crossRSI":
    short=sidebar.selectbox("Choose Days Short Moving Average",options= list(range(5,155,5)), index=0)
    long=sidebar.selectbox("Choose Days Long Moving Average",options= list(range(5,155,5)), index=0)
    days =sidebar.selectbox("Choose Days for RSI",options= list(range(5,40,1)), index=0)


with open("./coins.json", 'r') as f:
    top_100_coin_list = json.load(f)

coin_list = top_100_coin_list[:number].copy()
for i in range(number):
    coin_list[i] = sidebar.selectbox(f"Choose Cryptocurrency {i+1}",options=top_100_coin_list, index=i)

test_start = sidebar.selectbox("Back Testing Start Year",options= list(range(2015,2024)), index=len(list(range(2015,2024)))-4)
test_end = sidebar.selectbox("Back Testing End Year",list(range(2015,2024)), index=len(list(range(2015,2024)))-1)
submit = sidebar.button("Start Back Testing")

if test_end < test_start:
    test_end = test_start + 1



if submit:
    
    cs = CryptoSimulator(coin_list=coin_list)
    ## Get historical Data
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
    
    ## 
    st.markdown("### Strategy Information")
    total_profit, profit_histories, figures = cs.simulation(strategy=strategy,
                                                            start_year=test_start, 
                                                            end_year=test_end, 
                                                            short=short, 
                                                            long=long, 
                                                            days=days)
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
            st.write(f"Accumulate Return: {total_profit[j]*100-100}%")
    

