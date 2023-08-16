from pycoingecko import CoinGeckoAPI
import pandas as pd
import datetime as dt
import numpy as np
from utils import *

class CryptoSimulator:
    def __init__(self, coin_list=['bitcoin', 'litecoin', 'ethereum']):
        self.cg = CoinGeckoAPI()
        self.currency = "usd"
        self.coin_list = coin_list
        self.histories = None
    
    def get_market_data(self):
        """
        Get Top 10 Coins in Market Data according to its market capacity 

        Returns
        -------
        market : list
            a list of coins

        """
        market = self.cg.get_coins_markets(vs_currency=self.currency, per_page=100, order='market_cap_desc')
        return market
        
    
    def get_historical_data(self):
        coin_list = self.coin_list
        histories = []
        for coin in coin_list:
            history = self.cg.get_coin_market_chart_by_id(id=coin, vs_currency=self.currency, days='max')
            df = pd.DataFrame()

            for key in history:
                history[key] = np.array(history[key])
            to_datetime = np.vectorize(lambda x:dt.datetime.fromtimestamp(x/1000))
            time_stamp = to_datetime(history["prices"][:,0])
            df.index= time_stamp
            df[f"{coin}_Price"] = history["prices"][:,1]
            df[f"{coin}_Market_Caps"] = history["market_caps"][:,1]
            df[f"{coin}_Volumes"] = history["total_volumes"][:,1]
            
            histories.append(df)
        
        self.histories = histories
            
        return histories    
        
    
    def get_current_data(self):
        coin_list = self.coin_list
        price_data = self.cg.get_price(coin_list, vs_currencies=self.currency)
        return price_data
    
        

    


    def simulation(self, strategy="cross", start_year=2020, end_year=2023, limit_loss=0.05, **kwargs):
        if self.histories is None :
            self.get_historical_data() 
        
        total_profit = []
        
        profit_histories = []
        
        figures = []
        
        for history in self.histories:
            price_ts = history.iloc[:,0]
            price_ts_require = price_ts[(price_ts.index.year >= start_year) & (price_ts.index.year <= end_year)]
            if strategy == "cross":
                strategy_df, fig = strategy_by_cross(price_ts_require, **kwargs)
            elif strategy == "crossRSI":
                strategy_df, fig = strategy_by_cross_rsi(price_ts_require, **kwargs)
            elif strategy == "simple_buy_hold":
                strategy_df, fig = strategy_by_simple_buy_and_hold(price_ts_require, **kwargs)
                
            figures.append(fig)               
            hold = False
            profit_rate = 1
            buy_price = 0
            profit_history = []
            last_price = 0
            for i, row in strategy_df.iterrows():
                if row["Signal"] == 1 and not hold:
                    buy_price = row["Price"]
                    hold = True
                    last_price = row["Price"]
                elif row["Signal"] == -1 and hold:
                    profit_rate *= row["Price"]/last_price
                    hold = False
                    last_price = row["Price"]
                elif hold and row["Price"]/buy_price < (1-limit_loss):
                    profit_rate *= row["Price"]/last_price
                    hold = False
                    last_price = row["Price"]
                elif hold:
                    profit_rate *= row["Price"]/last_price
                    last_price = row["Price"]

                
                profit_history.append(profit_rate)

            profit_history = pd.Series(profit_history, index=strategy_df.index)
            profit_histories.append(profit_history)
            total_profit.append(profit_rate)
        
        return total_profit, profit_histories, figures
        
                
                
        
        
    
    


if __name__ == "__main__":
    cs = CryptoSimulator()
    data = cs.get_current_data()
    market = cs.get_market_data()
    # historical = cs.get_historical_data()
    # total_profit, profit_histories = cs.simulation()
    # print(data)
