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


def moving_median(time_series: pd.Series, window_size=10):
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
    
    return time_series.rolling(window_size).median()

    
def moving_std(time_series: pd.Series, window_size=10):
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
    
    return time_series.rolling(window_size).std()