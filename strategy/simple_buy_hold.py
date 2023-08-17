import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def strategy_by_simple_buy_and_hold(time_series:pd.Series, **kwargs):
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
        buy or sell the asset (buy: 1, sell: -1)
    fig : TYPE
        DESCRIPTION.

    """
    df = pd.DataFrame()
    df["Price"] = time_series
    df["Signal"] = 0
    df["Signal"].iloc[0] = 1
    df["Signal"].iloc[-1] = -1
    
    fig, ax = plt.subplots(2, figsize=(15,15))
    ax[-2].plot(df["Price"])
    ax[-2].set_title(f"Price in Testing Period")
    ax[-2].grid()
    ax[-1].bar(df["Signal"].index, df["Signal"], color='red')
    ax[-1].axhline(y=0, color='k')
    ax[-1].grid()
    ax[-1].set_title(f"Buy/Sell Signal")

    
    fig.tight_layout()
    return df, fig