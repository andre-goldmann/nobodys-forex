# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 09:29:36 2020

@author: mingyu
"""

import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover

class AdxCrossover(Strategy):
    window = 20
    adx_threshold = 25

    def init(self):
        self.tr = self.I(lambda: np.maximum(
            self.data.High - self.data.Low,
            np.abs(self.data.High - self.data.Close.shift(1)),
            np.abs(self.data.Low - self.data.Close.shift(1))
        ))
        
        self.plus_dm = self.I(lambda: np.where(
            (self.data.High - self.data.High.shift(1) > self.data.Low.shift(1) - self.data.Low) &
            (self.data.High - self.data.High.shift(1) > 0),
            self.data.High - self.data.High.shift(1),
            0
        ))
        
        self.minus_dm = self.I(lambda: np.where(
            (self.data.Low.shift(1) - self.data.Low > self.data.High - self.data.High.shift(1)) &
            (self.data.Low.shift(1) - self.data.Low > 0),
            self.data.Low.shift(1) - self.data.Low,
            0
        ))
        
        self.smoothed_tr = self.I(self.smoothed, self.tr, self.window)
        self.smoothed_plus_dm = self.I(self.smoothed, self.plus_dm, self.window)
        self.smoothed_minus_dm = self.I(self.smoothed, self.minus_dm, self.window)
        
        self.plus_di = self.I(lambda: 100 * self.smoothed_plus_dm / self.smoothed_tr)
        self.minus_di = self.I(lambda: 100 * self.smoothed_minus_dm / self.smoothed_tr)
        self.dx = self.I(lambda: 100 * np.abs(self.plus_di - self.minus_di) / (self.plus_di + self.minus_di))
        self.adx = self.I(self.smoothed, self.dx, self.window)

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

    def smoothed(self, series, window):
        return series.ewm(span=window, adjust=False).mean()
