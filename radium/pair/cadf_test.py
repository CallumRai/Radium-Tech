import statsmodels.tsa.stattools as ts
import pandas as pd


def CADF_Test(self):
    """
    Args:
        self: Pair

    Returns: Prints information from a CADF test

    """

    # Get closed prices in dataframe
    equity1_df = self.equity1.closed
    equity2_df = self.equity2.closed

    # Set column name as symbol
    equity1_df = equity1_df.rename(columns={"5. adjusted close": self.equity1.symbol})
    equity2_df = equity2_df.rename(columns={"5. adjusted close": self.equity2.symbol})

    # Augment dataframes, removing missing data
    df = pd.concat([equity1_df, equity2_df], axis=1, join="inner")

    # Get CADF result
    coint_t, pvalue, crit_value = ts.coint(df[self.equity1.symbol], df[self.equity2.symbol])

    # Round to make more interpretable
    coint_t = round(coint_t, 3)
    pvalue = round(pvalue, 3)
    crit_value = [round(x, 3) for x in crit_value]

    # Print results
    print(f"CADFTest for cointegration between {self.equity1.symbol} and {self.equity2.symbol} from {self.start_date}"
          f" to {self.end_date}\n")
    print(f"t-statistic = {coint_t}")
    print(f"p-value = {pvalue}\n")
    print(f"1% Critical Value: {crit_value[0]}")
    print(f"5% Critical Value: {crit_value[1]}")
    print(f"10% Critical Value: {crit_value[2]}")
