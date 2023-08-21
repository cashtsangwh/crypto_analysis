import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from strategy.utils import moving_average

def strategy_by_RSI(time_series:pd.Series, short:int=5, long:int=30, **kwargs):
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
    
    change = (time_series.shift(-1) - time_series).shift(1)
    gain = change.copy()
    loss = change.copy()
    gain.loc[change<=0] = 0
    loss.loc[change>=0] = 0
    
    short_avg_gain = gain.rolling(short).mean()
    short_avg_loss = -loss.rolling(short).mean()
    long_avg_gain = gain.rolling(long).mean()
    long_avg_loss = -loss.rolling(long).mean()
    
    short_rsi = 100 - (100/(1+short_avg_gain/short_avg_loss))
    long_rsi = 100 - (100/(1+long_avg_gain/long_avg_loss))
    
    df = pd.DataFrame()
    df["Price"] = time_series
    df["Gain"] = gain
    df["Loss"] = loss
    df["Short_Avg_Gain"] = short_avg_gain
    df["Short_Avg_Loss"] = short_avg_loss
    df["Long_Avg_Gain"] = long_avg_gain
    df["Long_Avg_Loss"] = long_avg_loss
    
    df["short_RSI"] = short_rsi
    df["long_RSI"] = long_rsi


    
    

    golden_cross = np.logical_and((df["short_RSI"].shift(-1) > df["short_RSI"]),
                                    np.logical_and((df["short_RSI"] < df["long_RSI"]),
                                    (df["short_RSI"].shift(-1) >  df["long_RSI"].shift(-1)))).shift(1)
    
    death_cross = np.logical_and((df["short_RSI"].shift(-1) < df["short_RSI"]),
                                    np.logical_and((df["short_RSI"] > df["long_RSI"]),
                                    (df["short_RSI"].shift(-1) <  df["long_RSI"].shift(-1)))).shift(1)
    

    df["Signal"]= (golden_cross.fillna(0).astype(np.int32) - death_cross.fillna(0).astype(np.int32))


    fig, ax = plt.subplots(3, figsize=(15,15))
    ax[0].plot(df["short_RSI"], label="Short RSI")
    ax[0].plot(df["long_RSI"], label="Long RSI")
    ax[0].set_title(f"{short} and {long} Days RSI Line")
    ax[0].legend()
    ax[-2].plot(df["Price"])
    ax[-2].set_title(f"Price in Testing Period")
    ax[-2].grid()
    ax[-1].bar(df["Signal"].index, df["Signal"], color='red')
    ax[-1].axhline(y=0, color='k')
    ax[-1].grid()
    ax[-1].set_title(f"Buy/Sell Signal")

    
    fig.tight_layout()
    return df, fig
