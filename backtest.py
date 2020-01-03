import pandas as pd
import numpy as np


def backtest(buy_condition, sell_condition, df):
    # df should minimally have a timestamp and close column
    # buy_condition & sell_condition should be dependent on the provided df
    df['signal'] = np.nan
    df.loc[df.eval(buy_condition), 'signal'] = 1
    df.loc[df.eval(sell_condition), 'signal'] = -1
    buy_df = df.loc[df['signal'] == 1]
    sell_df = df.loc[df['signal'] == -1]
    reduced_df = pd.concat([sell_df, buy_df], axis=0,
                           join='inner', ignore_index=False, copy=True)
    reduced_df.sort_values(by=['timestamp'], inplace=True)
    # Only take the state change
    reduced_df.loc[(reduced_df['signal'] == 1) & 
                   (reduced_df['signal'].shift() == 1)] = np.nan
    reduced_df.loc[(reduced_df['signal'] == -1) &
                   (reduced_df['signal'].shift() == -1)] = np.nan
    reduced_df.dropna(inplace=True)
    # Always start with buy
    first_buy = reduced_df.loc[reduced_df['signal'] == 1].index.min()
    reduced_df = reduced_df[first_buy:]
    reduced_df.reset_index(drop=True, inplace=True)
    reduced_df['delta'] = reduced_df['close']-reduced_df['close'].shift()
    #Only count profits when selling
    reduced_df.loc[reduced_df['signal']==1,'delta'] = np.nan
    result = reduced_df.delta.sum()
    return result
