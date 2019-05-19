"""
 Copyright © François Grabenstaetter <francoisgrabenstaetter@gmail.com>

 This file is part of Digital Assets.

 Digital Assets is free software: you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published
 by the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Digital Assets is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Digital Assets. If not, see <http://www.gnu.org/licenses/>.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Currency ():

    def __init__ (self, name, symbol, websiteURL):
        """
            Init Currency
        """
        self.name = name
        self.symbol = symbol
        self.websiteURL = websiteURL

        self.price = None # in USD
        self.lastDayPrice = None # in USD
        self.dayVolume = None # in USD
        self.circulatingSupply = None
        self.maxSupply = None
        self.marketCap = None # in USD
        self.rank = None
        self.ath = None # in USD
        self.dayGraphData = None
        self.monthGraphData = None
        self.yearGraphData = None
        self.allGraphData = None
        self.favorite = False

    def calculateAth (self, baseCurrency):
        """
            Calcululate the ATH ratio (between 0 and 1) for the self currency
            against the baseCurrency
        """
        if self.allGraphData is None or baseCurrency.allGraphData is None:
            return 0
        actualPrice = self.price / baseCurrency.price
        athPrice = None
        for index1, (dateTime1, price1) in enumerate(self.allGraphData):
            for index2, (dateTime2, price2) in enumerate(baseCurrency.allGraphData):
                if dateTime1 == dateTime2:
                    price = price1 / price2
                    if athPrice is None or price > athPrice:
                        athPrice = price
        return actualPrice / athPrice
