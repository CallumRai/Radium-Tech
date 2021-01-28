import unittest
from radium.equity import *

# AV Key
key = "A6O7S12U02K5YZO7"

from radium.pair import *
from radium.strategy import *
from radium.backtest import *

gld = Equity("GLD", "2020-01-01", "2021-01-01", key)
gdx = Equity("GDX", "2020-01-01", "2021-01-01", key)
gld_gdx = Pair(gld, gdx)
boll_gld_gdx = BollingerPair(gld_gdx, 1, 0, 30)
print(boll_gld_gdx)

#class TestEquity(unittest.TestCase):
