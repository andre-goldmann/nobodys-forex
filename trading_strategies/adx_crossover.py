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
        self.tr = self.I(self.true_range)
        self.plus_dm = self.I(self.plus_directional_movement)
        self.minus_dm = self.I(self.minus_directional_movement)
        
        self.smoothed_tr = self.I(self.smoothed, self.tr, self.window)
        self.smoothed_plus_dm = self.I(self.smoothed, self.plus_dm, self.window)
        self.smoothed_minus_dm = self.I(self.smoothed, self.minus_dm, self.window)
        
        self.plus_di = self.I(self.di, self.smoothed_plus_dm, self.smoothed_tr)
        self.minus_di = self.I(self.di, self.smoothed_minus_dm, self.smoothed_tr)
        self.dx = self.I(self.directional_index, self.plus_di, self.minus_di)
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

    def true_range(self):
        return np.maximum(self.data.High - self.data.Low,
                          np.abs(self.data.High - self.data.Close.shift(1)),
                          np.abs(self.data.Low - self.data.Close.shift(1)))

    def plus_directional_movement(self):
        up_move = self.data.High - self.data.High.shift(1)
        down_move = self.data.Low.shift(1) - self.data.Low
        return np.where((up_move > down_move) & (up_move > 0), up_move, 0)

    def minus_directional_movement(self):
        up_move = self.data.High - self.data.High.shift(1)
        down_move = self.data.Low.shift(1) - self.data.Low
        return np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    def smoothed(self, series, window):
        return series.ewm(span=window, adjust=False).mean()

    def di(self, smoothed_dm, smoothed_tr):
        return 100 * smoothed_dm / smoothed_tr

    def directional_index(self, plus_di, minus_di):
        return 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
