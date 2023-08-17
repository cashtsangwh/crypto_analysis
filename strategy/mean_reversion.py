import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from strategy.utils import moving_average, moving_std, moving_std

def strategy_by_mean_reversion(time_series:pd.Series, short=20, long=80, **kwargs):
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
    df = pd.DataFrame()
    df["Price"] = time_series

    df["short_mean"] = moving_average(time_series,short)
    df["long_mean"] = moving_average(time_series,long)
    
    df["short_std"] = moving_std(time_series,short)
    df["long_std"] = moving_std(time_series,long)
    
    df = df.dropna()
    signal = pd.Series(np.zeros_like(df["short_mean"].values), index=df["Price"].index)
    signal[(df["Price"] < df["short_mean"] - df["short_std"]) & (df["Price"] < df["long_mean"] - df["long_std"])] = 1
    signal[(df["Price"] > df["short_mean"])] = -1
    df["Signal"] = signal

    
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