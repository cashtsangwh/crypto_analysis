import streamlit as st
from simulator import CryptoSimulator
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import json


sidebar = st.sidebar
st.set_page_config(page_title="Cryptocurrecny Investment Analysis App", layout="wide")
st.markdown("# Cryptocurrecny Investment Analysis App")
number = sidebar.selectbox("Number of Cryptocurrency",options= list(range(1,16)), index=0)
strategy = sidebar.selectbox("Choose Strategy",options= ["MA", "RSI", "Mean_Reversion", "Linear_Regression", "MACD", "Simple_Buy_Hold"], index=0)
limit_fall = sidebar.selectbox("Limit Fall(%)",options= list(range(1,50)), index=0)
short = 0
long = 0
days = 0
explan_time_len = 0
test_time_len = 0
dea_day = 0
if strategy == "MA" or strategy == "Mean_Reversion" or strategy == "MACD":
    short=sidebar.selectbox("Choose Days for Short Moving Average",options= list(range(2,201,1)), index=5)
    long=sidebar.selectbox("Choose Days for Long Moving Average",options= list(range(2,201,1)), index=28)
    if strategy == "MACD":
        dea_day = sidebar.selectbox("Choose Days for DEA",options= list(range(2,155,1)), index=7)

elif strategy == "RSI":
    short=sidebar.selectbox("Choose Days for Short RSI",options= list(range(2,201,1)), index=4)
    long=sidebar.selectbox("Choose Days for Long RSI",options= list(range(2,201,1)), index=14)
elif strategy == "Linear_Regression":
    explan_time_len=sidebar.selectbox("Choose Time Length for Explanatory Variable",options= list(range(3,50,1)), index=6)
    test_time_len=sidebar.selectbox("Choose Time Length for Target",options= list(range(1,50,1)), index=0)


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

if not submit:
    st.markdown("## Parameter Explanation")
    st.markdown("### Number of Cryptocurrency")
    st.write("This app can capture the top 100 cryptocurrency with the highest market capital")
    st.write("Choose the number of cryptocurrency you want, the limit is 15")
    st.markdown("### Choose strategy")
    st.markdown("#### MA")
    st.write("This strategy implement the Golden Cross and Death Cross strategy by finding the interception Short Moving Average Line and Long Moving Average Line")
    st.write("You need to set the number of days for calculating Short/Long Moving Average")
    st.markdown("#### RSI")
    st.write("Similar to MA Strategy but using the Relative Strength Index (RSI) instead of MA to find the Golden Cross and Death Cross")
    st.write("You need to set the number of days for calculating Short/Long RSI")
    st.markdown("#### MACD")
    st.write("This strategy need to calculate a short and long term Exponential Moving Average(EMA) of Price and calculate their difference (Fast Line)")
    st.write("Then it need to calculate the EMA of the resulted Fast Line")
    st.write("You need to set the number of days for calculating Short/Long term EMA and the number of day for calculate the EMA of the Fast Line")
    st.markdown("#### Mean_Reversion")
    st.write("This is a buy low sell high strategy. It will calculate 'Mean' price for reference. The idea is to buy it when the price is lower than the 'Mean' and sell it when the price is higher than the 'Mean'")
    st.write("You need to set the number of days for calculating Short/Long Moving Average")
    st.markdown("#### Linear Regression")
    st.write("This strategy use the past m days daily return and volume to predict the accumulated return of the next n days")
    st.write("You need to set the number of days for m(Time length for Explanatory Variable) and n(Time length for Target)")
    st.write("It will automatically use the data before the backtesting period for training")
    st.markdown("#### Simple_Buy_Hold")
    st.write("This is just a buy and hold strategy. Just buy it at the start of the testing period wait until the end of it")
    st.markdown("#### Limit Fall(%)")
    st.write("This is a protective mechanism. When the price of the cryptocurrency drop by this percentage comparing to the last day, it will immediately sell it. (No use in Simple Buy Hold Strategy)")

if submit:
    
    cs = CryptoSimulator(coin_list=coin_list)
    ## Get historical Data
    histories = cs.get_historical_data()
    
    summary = histories[0].iloc[:,:2].copy()
    for history in histories[1:]:
        summary = pd.merge(summary, history.iloc[:,:2].copy(), right_index=True, left_index=True, how="outer")

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
            ax.grid()
            st.pyplot(fig)
    st.markdown("### Summary Information")
    st.write(summary.describe(percentiles=[0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99]))
    ## 
    st.markdown("### Strategy Information")
    total_profit, profit_histories, figures = cs.simulation(strategy=strategy,
                                                            limit_loss=limit_fall/100,
                                                            start_year=test_start, 
                                                            end_year=test_end, 
                                                            short=short, 
                                                            long=long, 
                                                            days=days,
                                                            explan_time_len=explan_time_len,
                                                            test_time_len=test_time_len,
                                                            dea_day=dea_day,)
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
            ax.grid()
            st.pyplot(fig)
            st.write(f"Accumulate Return: {total_profit[j]*100-100}%")
    

