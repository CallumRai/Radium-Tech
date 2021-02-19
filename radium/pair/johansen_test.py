import statsmodels.tsa.vector_ar.vecm as vm
import pandas as pd

from .pair import Pair

def johansen_test(pair):
    """
    Conducts a Johansen Test on a pair of equities and prints 
    trace/eigenvalue statistics and critical values.

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

    # Get Johansen results
    result = vm.coint_johansen(df.values, det_order=0, k_ar_diff=1)
    trace_stat = result.lr1
    trace_crit = result.cvt
    eigen_stat = result.lr2
    eigen_crit = result.cvm

    # Round to make more interpretable
    trace_stat = [round(x, 3) for x in trace_stat]
    trace_crit = [[round(x, 3) for x in y] for y in trace_crit]
    eigen_stat = [round(x, 3) for x in eigen_stat]
    eigen_crit = [[round(x, 3) for x in y] for y in eigen_crit]

    # Print results
    print(f'Johansen Test for cointegration between {pair.equity1.symbol} and ' 
          f'{pair.equity2.symbol} from {pair.start_date} to {pair.end_date}\n')

    for i in [0,1]:
        print(f'r<={i} Trace Statistic = {trace_stat[i]}\n'
              f'r<={i} Trace Critical Values:\n'
              f'1%: {trace_crit[i][0]}\n'
              f'5%: {trace_crit[i][1]}\n'
              f'10% {trace_crit[i][2]}')

    print('\n')

    for i in [0,1]:
        print(f'r<={i} Eigenvalue Statistic = {eigen_stat[i]}\n'
              f'r<={i} Eigenvalue Critical Values:\n'
              f'1%: {eigen_crit[i][0]}\n'
              f'5%: {eigen_crit[i][1]}\n'
              f'10% {eigen_crit[i][2]}')

    print('\n')
