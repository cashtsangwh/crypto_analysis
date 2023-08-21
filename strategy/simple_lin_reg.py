import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from strategy.utils import lin_reg

def strategy_by_simple_lin_reg(time_series:pd.Series, volume_series, train_price_series, train_volume_series, train_time_len, test_time_len, **kwargs):
    """

    Parameters
    ----------
    time_series : pd.Series
        The Closing Price Time series data in test period.
    volume_series: pd.Series
        The Volume Data Time series data in test period.
    train_price_series:
        The Closing Price Time series data in train period.
    train_volume_series:
        The Volume Data Time series data in train period.
    train_time_len:
        Use how many days data for the explanatory variable
    test_time_len:
        The target will be the average return of a certan time length

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
    df["Return"] = time_series.pct_change(1)
    df["Volume"] = volume_series
    train_df = pd.DataFrame()
    
    train_df["Return"] = train_price_series.pct_change(1)
    train_df["Volume"] = train_volume_series
    train_df["Target"] = train_price_series.pct_change(test_time_len).shift(-test_time_len)
    pred = lin_reg(train_df, df.loc[:,["Return","Volume"]], train_time_len)
    
    df["Signal"] = 0
    df["Signal"][pred > 0] = 1
    df["Signal"][pred < 0] = -1
    
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