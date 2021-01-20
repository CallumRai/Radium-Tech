import matplotlib.pyplot as plt
from helpers import data
import pandas as pd


def daily_two_close(symbol1, symbol2, start_date, end_date, key):
    # Get closed prices in dataframe
    symbol1_df = data.adjusted_closed(symbol1, start_date, end_date, key)
    symbol2_df = data.adjusted_closed(symbol2, start_date, end_date, key)

    # Set column name as symbol
    symbol1_df = symbol1_df.rename(columns={"5. adjusted close": symbol1})
    symbol2_df = symbol2_df.rename(columns={"5. adjusted close": symbol2})

    # Augment dataframes, removing missing data
    df = pd.concat([symbol1_df, symbol2_df], axis=1, join="inner")

    plt.plot(df.index, df[symbol1], label=symbol1)
    plt.plot(df.index, df[symbol2], label=symbol2)
    plt.xlabel("Date")
    plt.ylabel("Adjusted Closed Price")
    plt.ylim(bottom=0)
    plt.legend()
    plt.tight_layout()
    plt.show()

daily_two_close("IBM", "GLD", '2019-01-01', '2020-01-01', "R25C111BKODO8RHT")