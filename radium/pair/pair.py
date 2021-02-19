from datetime import datetime, date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statsmodels.formula.api as sm

from radium import Equity
from radium.helpers import _truncate


class Pair:
    """
    Initialise Pair class

    Parameters
    ----------
    equity1 : radium.Equity 
    equity2 : radium.Equity 

    Attributes
    ----------
    equity1 : radium.Equity
    equity2 : radium.Equity
    start_date : datetime.date
    end_date : datetime.date

    Raises
    ------
    TypeError
        If equity1 or equity2 is not of type radium.Equity.
    """

    def __init__(self, equity1, equity2):
        if not isinstance(equity1, Equity):
            raise TypeError('equity1 must of type radium.Equity')
        elif not isinstance(equity2, Equity):
            raise TypeError('equity2 must of type radium.Equity')

        self.equity1 = equity1
        self.equity2 = equity2
        self.start_date = equity1.start_date
        self.end_date = equity1.end_date

    @property
    def hedge_ratios(self):
        """
        np.float[][2]: ndarray of pairs of hedge ratios.
        
        Parameters
        ----------
        params : tuple of a string and an integer
            (method, lookback) where method is a string that determines the 
            method of calculating hedge_ratios and lookback is an integer that 
            determines the number of signals to lookback on.

        Raises
        ------
        TypeError
            If params isn't a tuple of length 2.
            If method isn't a string.
            If lookback isn't an integer.
        ValueError
            If lookback <= 0.
            If method isn't available.

        Notes
        -----
        Available method strings: 'OLS'.
        """

        return self._hedge_ratios

    @hedge_ratios.setter
    def hedge_ratios(self, params):

        # Exception handling of params
        if not isinstance(params, tuple):
            raise TypeError('params must be a tuple')
        elif len(params) != 2:
            raise TypeError('params must be a tuple of length 2')

        # Unpack params
        (method, lookback) = params

        # Exception handling of method
        if not isinstance(method, str):
            raise TypeError('method must be a string')
        
        # Exception handling of lookback
        if not isinstance(lookback, int):
            raise TypeError('lookback must be an integer.')
        elif lookback <= 0:
            raise ValueError('lookback must be > 0')

        # Calculate hedge ratios based on the method provided
        if method == 'OLS':
            self._hedge_ratios = self._hedge_ols(lookback)
        else:
            raise ValueError('Available method strings: "OLS"')


    @property
    def price_spread(self):
        """
        np.float[]: ndarray of price spread of equities for self.hedge_ratios.

        Raises
        ------
        TypeError
            If self.hedge_ratios isn't defined.

        Notes
        -----
        Spread calculated using y = h1*y1 + h2*y2.
        """

        if hasattr(self, '_hedge_ratios') == False:
            raise Exception('Pair.hedge_ratios is not defined.')

        # Calculate price_spread if undefined
        if hasattr(self, '_price_spread') == False:
            # Construct dataframe of closed prices
            prices = pd.concat([self.equity1.closed, self.equity2.closed],
                                axis=1)
            prices.columns = [self.equity1.symbol, self.equity2.symbol]

            # Multiply and add for each date
            self._price_spread = np.sum(self.hedge_ratios * prices, axis=1)

        return self._price_spread

    def budget(self, hedge_ratio, dec):
        """
        Returns budget needed to buy integer number of equities.

        Parameters
        ----------
        hedge_ratio : int[2]
            Equities hedge ratio
        dec : int
            Number of decimals to truncate to 

        Returns
        -------
        budget : float
            Budget needed rounded to 2 d.p.

        Raises
        -----
        TypeError
            If hedge_ratio isnt a list of floats, or dec isnt an integer.
        ValueError
            If hedge_ratio isn't length 2 or dec < 0.
        """

        if not isinstance(hedge_ratio, list):
            raise TypeError('hedge_ratio must be a list')
        elif not len(hedge_ratio) == 2:
            raise ValueError('hedge_ratio must have length 2')
        elif not isinstance(hedge_ratio[0], float):
            raise TypeError('hedge_ratio must be a list of floats')
        elif not isinstance(hedge_ratio[1], float):
            raise TypeError('hedge_ratio must be a list of floats')

        if not isinstance(dec, int):
            raise TypeError('Decimal places must be an integer.')
        elif dec < 0:
            raise ValueError('Decimal places has to be >= 0.')

        # Get the prices at end_date
        equity1_price = self.equity1.closed.iloc[0]
        equity2_price = self.equity2.closed.iloc[0]

        # Calculate truncated ratios to given number of decimals 
        truncated_ratios = np.array([_truncate(n, dec) for n in hedge_ratio])

        # Calculate budget to buy integer number of equites
        budget = equity1_price * abs(truncated_ratios[0]) * 10 ** dec \
                 + equity2_price * abs(truncated_ratios[1]) * 10 ** dec

        # Truncated budget to 2 decimals places
        budget = _truncate(budget, 2)

        return budget

    def plot_closed(self, start_date=None, end_date=None):
        """
        Plots closed prices of both equities between two dates.

        Parameters
        ----------
        start_date : datetime.date or 'YYYY-MM-DD', default=self.start_date 
        end_date : datetime.date or 'YYYY-MM-DD', default=self.end_date 

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If start_date/end_date isn't datetime.date or correctly formated
            string.
        ValueError
            If end_date <= start_date.

        """

        # Assign default values to start_date/end_date
        start_date = self.start_date if start_date == None else start_date
        end_date = self.end_date if end_date == None else end_date

        # Exception Handling
        if not isinstance(start_date, date):
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except:
                msg = 'start_date must be datetime.date or "YYYY-MM-DD"'
                raise TypeError(msg)

        if not isinstance(end_date, date):
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except:
                msg = 'end_date must be datetime.date or "YYYY-MM-DD"'
                raise TypeError(msg)

        # Raises error if date range invalid
        if end_date <= start_date:
            raise ValueError('end_date must be greater than start_date')
        elif start_date < self.start_date:
            raise ValueError('start_date cant be before pair.start_date')
        elif end_date > self.end_date:
            raise ValueError('end_date cant be before pair.end_date')

        # Gets required range only for both equities
        equity1_closed = self.equity1.closed
        mask = (equity1_closed.index >= start_date) \
               & (equity1_closed.index <= end_date)
        equity1_closed = equity1_closed.loc[mask]

        equity2_closed = self.equity2.closed
        mask = (equity2_closed.index >= start_date) \
               & (equity2_closed.index <= end_date)
        equity2_closed = equity2_closed.loc[mask]

        fig, ax = plt.subplots()
        plt.plot(equity1_closed, label=self.equity1.symbol)
        plt.plot(equity2_closed, label=self.equity2.symbol)

        title = (f'{self.equity1.symbol} and {self.equity2.symbol} '
                 f'from {start_date} to {end_date}')
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Adjusted closed prices ($)")

        # Put dollar marks infront of y axis
        formatter = ticker.FormatStrFormatter('$%1.2f')
        ax.yaxis.set_major_formatter(formatter)

        plt.legend()
        plt.grid()
        plt.show()

    def _hedge_ols(self, lookback):
        """
        Calculate pair hedge ratios by OLS regression. self.equity1 will be used
        as response variable when regressing.

        Parameters
        ----------
        lookback : int > 0 
            Number of signals to lookback on when regressing.

        Returns 
        -------
        hedge_ratios : np.float[][2] = [[1, -h], ...] 
            [1, -1*(OLS gradient)] as hedge ratios (y = y1 - h*y2).
        """

        # Construct dataframe of closed prices
        df = pd.concat([self.equity1.closed, self.equity2.closed], axis=1)
        df.columns = [self.equity1.symbol, self.equity2.symbol]

        # Get ols regression result for each date
        hedge_ratios = np.zeros(df.shape)
        for i in range(lookback, hedge_ratios.shape[0]):
            formula = f"{self.equity1.symbol} ~ {self.equity2.symbol}"
            df_lookback = df[(i - lookback):i]
            ols = sm.ols(formula, df_lookback).fit()

            # Hedge ratio for equity2 is -1*(OLS gradient)
            hedge_ratios[i - 1][0] = 1
            hedge_ratios[i - 1][1] = -1*ols.params[1]

        return hedge_ratios
