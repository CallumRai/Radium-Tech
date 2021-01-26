
import statsmodels.tsa.stattools as ts
import statsmodels.tsa.vector_ar.vecm as vm
import pandas as pd
import data


def CADF_Test(symbol1, symbol2, start_date, end_date, key):
    """
    :param symbol1: First pair
    :param symbol2: Second pair
    :param start_date: First date
    :param end_date: Last date
    :param key: API Key
    :return: Resulting info from a cadf test
    """

    # Get closed prices in dataframe
    symbol1_df = data.adjusted_closed(symbol1, start_date, end_date, key)
    symbol2_df = data.adjusted_closed(symbol2, start_date, end_date, key)

    # Set column name as symbol
    symbol1_df = symbol1_df.rename(columns={"5. adjusted close": symbol1})
    symbol2_df = symbol2_df.rename(columns={"5. adjusted close": symbol2})

    # Augment dataframes, removing missing data
    df = pd.concat([symbol1_df, symbol2_df], axis=1, join="inner")

    # Get CADF result
    coint_t, pvalue, crit_value = ts.coint(df[symbol1], df[symbol2])

    # Round to make more interpretable
    coint_t = round(coint_t, 3)
    pvalue = round(pvalue, 3)
    crit_value = [round(x, 3) for x in crit_value]

    # Print results
    print(f"CADFTest for cointegration between {symbol1} and {symbol2} from {start_date} to {end_date}\n")
    print(f"t-statistic = {coint_t}")
    print(f"p-value = {pvalue}\n")
    print(f"1% Critical Value: {crit_value[0]}")
    print(f"5% Critical Value: {crit_value[1]}")
    print(f"10% Critical Value: {crit_value[2]}")


def johansen_test(symbol1, symbol2, start_date, end_date, key):
    """
    :param symbol1: First pair
    :param symbol2: Second pair
    :param start_date: First date
    :param end_date: Last date
    :param key: API Key
    :return: Resulting info from a cadf test
    """
    # Get closed prices in dataframe
    symbol1_df = data.adjusted_closed(symbol1, start_date, end_date, key)
    symbol2_df = data.adjusted_closed(symbol2, start_date, end_date, key)

    # Set column name as symbol
    symbol1_df = symbol1_df.rename(columns={"5. adjusted close": symbol1})
    symbol2_df = symbol2_df.rename(columns={"5. adjusted close": symbol2})

    # Augment dataframes, removing missing data
    df = pd.concat([symbol1_df, symbol2_df], axis=1, join="inner")

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
    print(f"Johansen Test for cointegration between {symbol1} and {symbol2} from {start_date} to {end_date}")
    for i in [0,1]:
        print(f"\nr<={i} Trace Statistic = {trace_stat[i]}")
        print(f"r<={i} Trace Critical Values:")
        print(f"1%: {trace_crit[i][0]}\n5%: {trace_crit[i][1]}\n10% {trace_crit[i][2]}")

    for i in [0,1]:
        print(f"\nr<={i} Eigenvalue Statistic = {eigen_stat[i]}")
        print(f"r<={i} Eigenvalue Critical Values: ")
        print(f"1%: {eigen_crit[i][0]}\n5%: {eigen_crit[i][1]}\n10% {eigen_crit[i][2]}")

    # Return cointegration ratios
    return result.evec[:, 0]
