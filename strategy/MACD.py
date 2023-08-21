import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from strategy.utils import exponential_moving_average

def strategy_by_MACD(time_series:pd.Series, short:int=5, long:int=30, dea_day:int=9, **kwargs):
    """

    Parameters
    ----------
    time_series : pd.Series
        The Closing Price Time series data.
    short : int, optional
        The number of days use to calculate the shorter day moving average line. 
        The default is 5.
    long : int, optional
        The number of days use to calculate the shorter day moving average line. 
        The default is 30.
    dea_dat: int, optional
        The number of days use to calculate the DEA line.

    Returns
    -------
    df : pd.DataFrame
        A dataframe with columns "Signal" that used to determine whether we should
        buy or sell the asset (buy: 1, sell: -1)
    fig : TYPE
        DESCRIPTION.

    """

    short_EMA = exponential_moving_average(time_series,short)
    long_EMA = exponential_moving_average(time_series,long)
    diff = short_EMA - long_EMA
    dea = exponential_moving_average(diff,dea_day)
    df = pd.DataFrame()
    df["Price"] = time_series
    df["short"] = short_EMA
    df["long"] = long_EMA
    df["diff"] = diff
    df["dea"] = dea
    df = df.dropna()

    golden_cross = np.logical_and((df["diff"].shift(-1) > df["diff"]),
                                    np.logical_and((df["diff"] < df["dea"]),
                                    (df["diff"].shift(-1) >  df["dea"].shift(-1)))).shift(1)
    
    death_cross = np.logical_and((df["diff"].shift(-1) < df["diff"]),
                                    np.logical_and((df["diff"] > df["dea"]),
                                    (df["diff"].shift(-1) <  df["dea"].shift(-1)))).shift(1)
    

    df["Signal"] = (golden_cross.fillna(0).astype(np.int32) - death_cross.fillna(0).astype(np.int32))
    
    fig, ax = plt.subplots(4, figsize=(15,15))
    ax[0].plot(df["diff"], label="DIFF")
    ax[0].plot(df["dea"], label="DEA")
    ax[0].grid()
    ax[0].legend()
    ax[0].set_title(f"DIFF and DEA")
    ax[1].plot(2*(df["diff"] - df["dea"]), color='orange')
    ax[1].bar(df["Signal"].index,2*(df["diff"] - df["dea"]), color='green')
    ax[1].grid()
    ax[1].set_title(f"MACD")
    ax[-2].plot(df["Price"])
    ax[-2].set_title(f"Price in Testing Period")
    ax[-2].grid()
    ax[-1].bar(df["Signal"].index, df["Signal"], color='red')
    ax[-1].axhline(y=0, color='k')
    ax[-1].grid()
    ax[-1].set_title(f"Buy/Sell Signal")

    fig.tight_layout()
    return df, fig
    