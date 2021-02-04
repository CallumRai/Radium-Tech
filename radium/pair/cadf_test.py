import statsmodels.tsa.stattools as ts
import pandas as pd

def CADF_Test(pair):
    """
    Args:
        pair: Pair

    Returns: Prints information from a CADF test

    """

    # Get closed prices in dataframe
    equity1_df = pair.equity1.closed
    equity2_df = pair.equity2.closed

    # Set column name as symbol
    equity1_df = equity1_df.rename(pair.equity1.symbol)
    equity2_df = equity2_df.rename(pair.equity2.symbol)

    # Augment dataframes, removing missing data
    df = pd.concat([equity1_df, equity2_df], axis=1, join="inner")

    # Get CADF result
    coint_t, pvalue, crit_value = ts.coint(df[pair.equity1.symbol], df[pair.equity2.symbol])

    # Round to make more interpretable
    coint_t = round(coint_t, 3)
    pvalue = round(pvalue, 3)
    crit_value = [round(x, 3) for x in crit_value]

    # Print results
    print(f"CADFTest for cointegration between {pair.equity1.symbol} and {pair.equity2.symbol} from {pair.start_date}"
          f" to {pair.end_date}\n")
    print(f"t-statistic = {coint_t}")
    print(f"p-value = {pvalue}\n")
    print(f"1% Critical Value: {crit_value[0]}")
    print(f"5% Critical Value: {crit_value[1]}")
    print(f"10% Critical Value: {crit_value[2]}")
