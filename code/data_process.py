import pandas as pd
import numpy as np


def find_mean_estimate(df):
    temp = df.copy()
    temp['FPEDATS'] = pd.to_datetime(temp['FPEDATS'])
    temp['ANNDATS_ACT'] = pd.to_datetime(temp['ANNDATS_ACT'])
    temp['ANNDATS'] = pd.to_datetime(temp['ANNDATS'])

    temp = temp.sort_values(by=['FPEDATS', 'ANNDATS'], ascending=[True, True])

    result = temp.groupby(['TICKER', 'FPEDATS', 'ANNDATS']).agg({
        'VALUE': 'mean',
        'ACTUAL': 'first',
        'ANNDATS_ACT': 'first'
    }).rename(columns={
        'VALUE': 'Mean_Est_EPS',
        'ACTUAL': 'EPS_ACT'
    })

    result = result.reset_index()
    return result


def select_timeDiff(df, day_diff):

    temp = df.copy()
    temp['day_diff'] = (temp['ANNDATS_ACT'] - temp['ANNDATS']).dt.days

    mask = temp['day_diff'] >= day_diff
    result = temp[mask].copy()

    result['diff_from_target'] = result['day_diff'] - day_diff
    idx = result.groupby('FPEDATS')['diff_from_target'].idxmin()
    result = result.loc[idx]

    result = result.reset_index(drop=True)
    result = result.drop(['day_diff', 'diff_from_target'], axis=1)
    return result


def beat_estimate(df):

    temp = df.copy()
    temp['beat_est'] = temp['EPS_ACT'] >= temp['Mean_Est_EPS']

    result = temp[['TICKER', 'ANNDATS', 'ANNDATS_ACT',
                   'Mean_Est_EPS', 'EPS_ACT', 'beat_est']]
    result = result.rename(columns={
        'TICKER': 'ticker',
        'ANNDATS': 'annDates_est',
        'ANNDATS_ACT': 'annDates_act',
        'Mean_Est_EPS': 'eps_est',
        'EPS_ACT': 'eps_act'
    })

    return result


def calc_returns(df, ticker, day_diff):

    result = df.copy()

    stock_price = yf.download(ticker, start='2019-07-01', end='2024-09-23')
    all_dates = pd.date_range(start='2019-07-01', end='2024-09-23')

    stock_price = stock_price.reindex(all_dates)['Close'].pct_change(
        periods=day_diff, fill_method='bfill')
    result = pd.merge(result, stock_price, left_on='annDates_act',
                      right_index=True, how='left').rename(columns={'Close': 'returns'})
    # alternative (to show buy and sell prices):
    # stock_price = stock_price.reindex(all_dates).fillna(method='bfill')
    # stock_price["close_shift"] = stock_price["Close"].shift(day_diff)
    # stock_price["returns"] = (stock_price["Close"] - stock_price["close_shift"])/stock_price["close_shift"]
    # stock_price = stock_price[['Close', 'close_shift', 'returns']].rename(columns={'Close': 'close'})
    # result = pd.merge(df, stock_price, left_on='annDates_act', right_index=True, how='left')

    return result
