import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from strategy.utils import moving_average

def strategy_by_cross(time_series:pd.Series, short:int=5, long:int=30, **kwargs):
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

    Returns
    -------
    df : pd.DataFrame
        A dataframe with columns "Signal" that used to determine whether we should
        buy all sell the asset (buy: 1, sell: -1)
    fig : TYPE
        DESCRIPTION.

    """

    short_MA = moving_average(time_series,short)
    long_MA = moving_average(time_series,long)
    df = pd.DataFrame()
    df["Price"] = time_series
    df["short"] = short_MA
    df["long"] = long_MA
    df = df.dropna()

    golden_cross = np.logical_and((df["short"].shift(-1) > df["short"]),
                                    np.logical_and((df["short"] < df["long"]),
                                    (df["short"].shift(-1) >  df["long"].shift(-1)))).shift(1)
    
    death_cross = np.logical_and((df["short"].shift(-1) < df["short"]),
                                    np.logical_and((df["short"] > df["long"]),
                                    (df["short"].shift(-1) <  df["long"].shift(-1)))).shift(1)
    

    df["Signal"] = (golden_cross.fillna(0).astype(np.int32) - death_cross.fillna(0).astype(np.int32))
    
    fig, ax = plt.subplots(3, figsize=(15,15))
    ax[0].plot(df["short"], label="Short MA")
    ax[0].plot(df["long"], label="Long MA")
    ax[1].plot(df["Price"])
    ax[2].plot(df["Signal"] ,'-r')
    ax[0].legend()
    fig.tight_layout()
    return df, fig
    