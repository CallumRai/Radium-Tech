# Radium

**Radium-Tech** is a Python package providing an intuitive backtesting and visualisation platform for quantitative trading strategies.

## Main Features

In current version Radium-Tech can:
- Plot price data for multiple equities.
- Regress hedge ratios and price spread for a pair of equities.
- Conduct tests for cointegration on pairs of equities.
- Backtest a Bollinger Band strategy.

Future versions aim to add additonal mean-reversing strategies.

## Where to get it

The latest public version of Radium-Tech is avaliable on [Python Package Index (PyPI)](https://pypi.org/project/Radium-Tech/)

```sh
pip install Radium-Tech
```

## Dependencies

Radium-Tech requires:
- `numpy`
- `pandas`
- `matplotlib`
- `statsmodels`
- `requests`

An [Alpha-Vantage](https://www.alphavantage.co/) free API key is also required for equity data.

## Documentation

Official documentation for Radium-Tech is hosted on readthedocs.io: https://radium-tech.readthedocs.io/en/latest/

They can be downloaded in PDF form: https://radium-tech.readthedocs.io/_/downloads/en/latest/pdf/

## Example 

An example full backtest cycle can be found in `Radium-Tech/Examples/bollinger.py`

```sh
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
```

## Authors

Radium-Tech is developed by [Ivan Erlic](https://linkedin.com/in/ivan-e-665420122) and [Callum Rai](https://linkedin.com/in/callumrai) of University College London.

Please submit any bugs/suggestions/questions to the [issues forum](https://github.com/CallumRai/Radium-Tech/issues)
