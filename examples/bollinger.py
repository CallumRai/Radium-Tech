from src import Equity, Pair
from src.pair import johansen_test
from src.strategy import BollingerPair

# Alpha-vantage API Key
API_KEY = ''

# Creates equity, pair objects for visa and mastercard 2015-2021
visa = Equity('V', '2015-01-01', '2021-01-01', API_KEY)
mastercard = Equity('MA', '2015-01-01', '2021-01-01', API_KEY)
v_ma = Pair(visa, mastercard)

# Visualise data
v_ma.plot()

# Test for cointegration
johansen_test(v_ma)

# Backtest Bollinger band strategy on pair
entry_z = 1
exit_z = 0
lookback = 30
v_ma_bollinger = BollingerPair(v_ma, entry_z, exit_z, lookback)

# Evaluate strategy
sharpe = v_ma_bollinger.sharpe()
ann_returns = v_ma_bollinger.ann_returns()

print(f"Sharpe ratio: {sharpe}")
print(f"Annualised returns: {ann_returns}")