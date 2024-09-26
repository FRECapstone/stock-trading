import pandas as pd
import numpy as np


def strat(df):

    df['strat_returns'] = np.where(
        df['beat_est'], df['returns']*1, df['returns']*-1)
    df['cum_strat_returns'] = (1+df['strat_returns']).cumprod()-1

    print("Cumulative Return:", round(df['cum_strat_returns'].iloc[-1], 3))

    return df


def portfolio(list_df):

    temp = list_df[0].copy()
    temp = temp.rename(
        columns={'strat_returns': f"{temp['ticker'].dropna().iloc[0]}_strat_returns_p"})

    for df in list_df[1:]:
        temp = pd.merge(temp, df, on='annDates_act', how='outer')
        temp = temp.rename(
            columns={'strat_returns': f"{df['ticker'].dropna().iloc[0]}_strat_returns_p"})

    filter = temp.filter(regex='_strat_returns_p$').columns.tolist()
    temp = temp[['annDates_act']+filter]

    temp['strat_returns'] = temp.filter(regex='_strat_returns_p$').sum(axis=1)
    temp = temp.sort_values(by='annDates_act').reset_index(drop=True)

    temp['cum_strat_returns'] = temp['strat_returns'].cumsum()

    print("Cumulative Return:", temp['strat_returns'].sum())

    return temp
