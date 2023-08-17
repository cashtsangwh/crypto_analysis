import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def moving_average(time_series: pd.Series, window_size=10):
    """
    

    Parameters
    ----------
    time_series : pd.Series
        time series data
    window_size : int, optional
        the moving average size. The default is 10.

    Returns
    -------
    pd.Series
        Moving Average Series.

    """
    
    return time_series.rolling(window_size).mean()



def strategy_by_rsi(time_series:pd.Series, days=14, **kwargs):
    """

    Parameters
    ----------
    time_series : pd.Series
        The Closing Price Time series data.
    days : int, optional
        The number of days use to calculate the RSI. 
        The default is 14.

    Returns
    -------
    df : pd.DataFrame
        A dataframe with columns "Signal" that used to determine whether we should
        buy all sell the asset (buy: 1, sell: -1)
    fig : TYPE
        DESCRIPTION.

    """
    change = (time_series.shift(-1) - time_series).shift(1)
    gain = change.copy()
    loss = change.copy()
    gain.loc[change<=0] = 0
    loss.loc[change>=0] = 0
    
    avg_gain = gain.rolling(days).mean()
    avg_loss = -loss.rolling(days).mean()
    
    rsi = 100 - (100/(1+avg_gain/avg_loss))
    
    df = pd.DataFrame()
    df["Price"] = time_series
    df["Gain"] = gain
    df["Loss"] = loss
    df["Avg_Gain"] = avg_gain
    df["Avg_Loss"] = avg_loss
    df["RSI"] = rsi
    
    buy = rsi < 30
    sell = rsi > 70
    df["Signal"] = (buy.fillna(0).astype(np.int32) - sell.fillna(0).astype(np.int32))
    
    fig, ax = plt.subplots(3, figsize=(15,15))
    ax[0].plot(df["RSI"], label="RSI")
    ax[1].plot(df["Price"])
    ax[2].plot(df["Signal"] ,'-r')
    ax[0].legend()
    fig.tight_layout()
    
    return df, fig
    
    
    
