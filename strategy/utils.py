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

def lin_reg(time_dataframe, test_time_dataframe, train_time_len=10):
    from sklearn.linear_model import LinearRegression 
    
    variable = time_dataframe.values.shape[1]-1

    time_dataframe = time_dataframe.copy().dropna()
    
    matrix = []
    target = []
    
    for i in range(train_time_len, len(time_dataframe)):
        y = time_dataframe.iloc[i-train_time_len,variable]
        if not np.isnan(y):
            matrix.append(time_dataframe.iloc[i-train_time_len:i,:variable].values.reshape(-1))
            target.append(y)
        else:
            break
    
    lr = LinearRegression()
    lr.fit(matrix, target)

    pred = [np.nan]*train_time_len
    test_time_dataframe = test_time_dataframe.copy()
    test_time_dataframe.to_csv("Test.csv")
    for i in range(train_time_len, len(test_time_dataframe)):
        x = test_time_dataframe.iloc[i-train_time_len:i,:variable].values.reshape(-1)
        try:
            pred.append(lr.predict([x]))
        except:
            pred.append(0)
    
    return pd.Series(pred, index=test_time_dataframe.index)
    

def exponential_moving_average(time_series: pd.Series, window_size=5):
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
        Exponential Moving Average Series.

    """
    ts = time_series.copy()
    ts.dropna()
    start = ts.iloc[:window_size].mean()
    ts.iloc[window_size-1] = start
    ts.iloc[window_size-1:] = ts.iloc[window_size-1:].ewm(span=window_size, adjust=False).mean()
    ts.iloc[:window_size-1] = np.nan
    return ts

if __name__ == "__main__":

    test = pd.Series([106.54,106.74,106.67,106.97,107.96,108.36,108.36])
    ewm = exponential_moving_average(test, 5)
    
