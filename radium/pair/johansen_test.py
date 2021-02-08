import statsmodels.tsa.vector_ar.vecm as vm
import pandas as pd

def johansen_test(pair):
    """
    Conducts a Johansen test on a pair of equities and prints trace/eigenvalue statistic and critical values

    Args:
        pair: Pair of Equities to test

    Returns: Cointegration rations

    """

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
    print(f"Johansen Test for cointegration between {pair.equity1.symbol} and {pair.equity2.symbol} from"
          f" {pair.start_date} to {pair.end_date}")
    for i in [0,1]:
        print(f"\nr<={i} Trace Statistic = {trace_stat[i]}")
        print(f"r<={i} Trace Critical Values:")
        print(f"1%: {trace_crit[i][0]}\n5%: {trace_crit[i][1]}\n10% {trace_crit[i][2]}")

    for i in [0,1]:
        print(f"\nr<={i} Eigenvalue Statistic = {eigen_stat[i]}")
        print(f"r<={i} Eigenvalue Critical Values: ")
        print(f"1%: {eigen_crit[i][0]}\n5%: {eigen_crit[i][1]}\n10% {eigen_crit[i][2]}")

    print("\n")

    # Return cointegration ratios
    return result.evec[:, 0]