import pandas as pd
import statsmodels.tsa.stattools as ts

from .pair import Pair


def cadf_test(pair):
    """
    Conducts a Cointegrated Augmented Dickey Fuller Test on a pair of equities 
    and prints t-statistic, p-value and critical values.

    Parameters
    ----------
    pair : radium.Pair

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If pair is not of type radium.Pair.
    """

    if not isinstance(pair, Pair):
        raise TypeError('Pair must be of type radium.Pair')

    # Get closed prices in dataframe
    equity1_df = pair.equity1.closed
    equity2_df = pair.equity2.closed

    # Set column name as symbol
    equity1_df = equity1_df.rename(pair.equity1.symbol)
    equity2_df = equity2_df.rename(pair.equity2.symbol)

    # Augment dataframes, removing missing data
    df = pd.concat([equity1_df, equity2_df], axis=1, join="inner")

    # Get CADF result
    coint_t, pvalue, crit_value = ts.coint(df[pair.equity1.symbol],
                                           df[pair.equity2.symbol])

    # Round to make more interpretable
    coint_t = round(coint_t, 3)
    pvalue = round(pvalue, 3)
    crit_value = [round(x, 3) for x in crit_value]

    # Print results
    results = (f'CADF Test for cointegration between {pair.equity1.symbol} '
               f'and {pair.equity2.symbol} from {pair.start_date} to '
               f'{pair.end_date}\n\n'
               f't-statistic = {coint_t}\n'
               f'p-value = {pvalue}\n\n'
               f'1% Critical Value: {crit_value[0]}\n'
               f'5% Critical Value: {crit_value[1]}\n'
               f'10% Critical Value: {crit_value[2]}\n\n')

    print(results)
