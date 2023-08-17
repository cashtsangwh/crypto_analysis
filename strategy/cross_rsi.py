import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from strategy.utils import moving_average

def strategy_by_cross_rsi(time_series:pd.Series, short:int=5, long:int=30, days=14, **kwargs):
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
    
    short_MA = moving_average(time_series,short)
    long_MA = moving_average(time_series,long)
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
    df["short"] = short_MA
    df["long"] = long_MA
    df["Gain"] = gain
    df["Loss"] = loss
    df["Avg_Gain"] = avg_gain
    df["Avg_Loss"] = avg_loss
    df["RSI"] = rsi
    buy = rsi < 30
    sell = rsi > 70
    df = df.dropna()
    df["rsi_Signal"] = (buy.astype(np.int32) - sell.astype(np.int32))
    
    
    

    golden_cross = np.logical_and((df["short"].shift(-1) > df["short"]),
                                    np.logical_and((df["short"] < df["long"]),
                                    (df["short"].shift(-1) >  df["long"].shift(-1)))).shift(1)
    
    death_cross = np.logical_and((df["short"].shift(-1) < df["short"]),
                                    np.logical_and((df["short"] > df["long"]),
                                    (df["short"].shift(-1) <  df["long"].shift(-1)))).shift(1)
    

    df["cross_Signal"] = (golden_cross.fillna(0).astype(np.int32) - death_cross.fillna(0).astype(np.int32))
    df["Signal"] = df["rsi_Signal"] + 1.5*df["cross_Signal"]
    
    df["Signal"].loc[df["Signal"]==1] = 0
    df["Signal"].loc[df["Signal"]<0] = -1
    df["Signal"].loc[df["Signal"]>1] = 1
    
    fig, ax = plt.subplots(4, figsize=(15,15))
    ax[0].plot(df["RSI"], label="RSI")
    ax[0].set_title("RSI")
    ax[1].plot(df["short"], label="Short MA")
    ax[1].plot(df["long"], label="Long MA")
    ax[1].set_title(f"{short} and {long} Days Moving Average Line")
    ax[1].legend()
    ax[-2].plot(df["Price"])
    ax[-2].set_title(f"Price in Testing Period")
    ax[-2].grid()
    ax[-1].bar(df["Signal"].index, df["Signal"], color='red')
    ax[-1].axhline(y=0, color='k')
    ax[-1].grid()
    ax[-1].set_title(f"Buy/Sell Signal")

    
    fig.tight_layout()
    return df, fig
