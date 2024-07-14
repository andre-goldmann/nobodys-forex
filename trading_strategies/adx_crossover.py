# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 09:29:36 2020

@author: mingyu
"""

import ta
from backtesting import Strategy
from backtesting.lib import crossover

class AdxCrossover(Strategy):
    window = 20
    adx_threshold = 25

    def init(self):
        self.adx = self.I(ta.trend.ADXIndicator, self.data.High, self.data.Low, self.data.Close, self.window)
        self.plus_di = self.I(ta.trend.ADXIndicator(high=self.data.High, low=self.data.Low, close=self.data.Close, window=self.window).adx_pos)
        self.minus_di = self.I(ta.trend.ADXIndicator(high=self.data.High, low=self.data.Low, close=self.data.Close, window=self.window).adx_neg)

    def next(self):
        if self.adx[-1] > self.adx_threshold:
            if crossover(self.plus_di, self.minus_di):
                self.buy()
            elif crossover(self.minus_di, self.plus_di):
                self.sell()

        if self.position.is_long and crossover(self.minus_di, self.plus_di):
            self.position.close()
        elif self.position.is_short and crossover(self.plus_di, self.minus_di):
            self.position.close()
