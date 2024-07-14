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
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

        self.tr = self.I(lambda: np.maximum(
            high - low,
            np.abs(high - np.roll(close, 1)),
            np.abs(low - np.roll(close, 1))
        ), name='TR')
        
        self.plus_dm = self.I(lambda: np.where(
            (high - np.roll(high, 1) > np.roll(low, 1) - low) &
            (high - np.roll(high, 1) > 0),
            high - np.roll(high, 1),
            0
        ), name='Plus_DM')
        
        self.minus_dm = self.I(lambda: np.where(
            (np.roll(low, 1) - low > high - np.roll(high, 1)) &
            (np.roll(low, 1) - low > 0),
            np.roll(low, 1) - low,
            0
        ), name='Minus_DM')
        
        self.smoothed_tr = self.I(lambda: self.smoothed(self.tr, self.window), name='Smoothed_TR')
        self.smoothed_plus_dm = self.I(lambda: self.smoothed(self.plus_dm, self.window), name='Smoothed_Plus_DM')
        self.smoothed_minus_dm = self.I(lambda: self.smoothed(self.minus_dm, self.window), name='Smoothed_Minus_DM')
        
        self.plus_di = self.I(lambda: np.where(self.smoothed_tr != 0, 100 * self.smoothed_plus_dm / self.smoothed_tr, 0), name='Plus_DI')
        self.minus_di = self.I(lambda: np.where(self.smoothed_tr != 0, 100 * self.smoothed_minus_dm / self.smoothed_tr, 0), name='Minus_DI')
        self.dx = self.I(lambda: np.where((self.plus_di + self.minus_di) != 0, 100 * np.abs(self.plus_di - self.minus_di) / (self.plus_di + self.minus_di), 0), name='DX')
        self.adx = self.I(lambda: self.smoothed(self.dx, self.window), name='ADX')

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
        alpha = 1 / window
        def smooth(x):
            if len(x) < 2:
                return x
            return x[0] if np.isnan(x[1]) else alpha * x[0] + (1 - alpha) * x[1]
        return self.I(smooth, series, name=f'EMA_{window}')
