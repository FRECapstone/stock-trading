import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot(df, ticker):
    plt.figure()
    plt.plot(df['annDates_act'], df["strat_returns"],
             marker='o', label='Quarterly Returns')
    plt.plot(df['annDates_act'], df["cum_strat_returns"],
             marker='o', label='Cumulative Returns')
    plt.title(ticker + ' Quarterly Returns vs Cumulative Returns')
    plt.axhline(0, linestyle='--', color='red')
    plt.xlabel('Quarters')
    plt.ylabel('Returns')
    plt.legend()
    plt.show()
