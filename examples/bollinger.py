from radium import Equity, Pair
from radium.pair import cadf_test, johansen_test
from radium.strategy import BollingerPair


# Alpha-vantage API Key
API_KEY = ''

# Creates equity, pair objects for visa and mastercard 2015-2021
MRO = Equity('AXP', '2016-01-01', '2021-01-01', API_KEY)
NAVI = Equity('AAL', '2016-01-01', '2021-01-01', API_KEY)
MRO_NAVI = Pair(MRO, NAVI)

# Hedge the pair
MRO_NAVI.hedge('OLS', 30)

# Visualise data
#MRO_NAVI.plot_price_spread()

# Test for cointegration
#cadf_test(MRO_NAVI)
#johansen_test(MRO_NAVI)

# Backtest Bollinger band strategy on pair
entry_z = 1
exit_z = 0
lookback = 30
bollinger = BollingerPair(MRO_NAVI, entry_z, exit_z, lookback)

# Evaluate strategy
positions = bollinger.th_positions
sharpe = bollinger.sharpe()
ann_returns = bollinger.CAGR

print(f"Sharpe ratio: {sharpe}")
print(f"Annualised returns: {ann_returns}")
