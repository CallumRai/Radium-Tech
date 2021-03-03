from radium import Equity, Pair
from radium.pair import cadf_test, johansen_test
from radium.strategy import BollingerPair


# Alpha-vantage API Key
API_KEY = ''

# Creates equity, pair objects for visa and mastercard 2015-2021
equity1 = Equity('KO', '2016-01-01', '2021-01-01', API_KEY)
equity2 = Equity('SBUX', '2016-01-01', '2021-01-01', API_KEY)
pair = Pair(equity1, equity2)

# Visualise data
pair.plot_closed()

# Test for cointegration
cadf_test(pair)
johansen_test(pair)

# Hedge the pair
pair.hedge('OLS', 30)

# Backtest Bollinger band strategy on pair
entry_z = 1
exit_z = 0
lookback = 30
bollinger = BollingerPair(pair, entry_z, exit_z, lookback)

# Evaluate strategy
CAGR = bollinger.CAGR
sharpe = bollinger.sharpe

print(f"Compound Annual Growth Rate: {CAGR}")
print(f"Sharpe ratio: {sharpe}")
