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
        self.favorite = False

        self.priceUSD = None
        self.lastDayPriceUSD = None
        self.dayVolumeUSD = None
        self.marketCapUSD = None
        self.athUSD = None # None or (price, date)
        self.__lastCalculatedAth = None # None or (baseCurrency, price, date)

        self.circulatingSupply = None
        self.maxSupply = None
        self.rank = None

        # graph data is a list of (object datetime, float price)
        self.dayGraphDataUSD = None
        self.monthGraphDataUSD = None
        self.yearGraphDataUSD = None
        self.alltimeGraphDataUSD = None

    def calculateAth (self, baseCurrency):
        """
            Calcululate the ATH ratio (between 0 and 1) and the ATH date for the self currency
            compared to the baseCurrency
            @return tuple (ratio, date)
        """

        # function to calculate ATH only with USD base currency
        def maxUSD ():
            max = None
            for (dt, price) in self.alltimeGraphDataUSD:
                if max is None or price > max[0]:
                    max = (price, dt)
            # convert max price to ratio and return
            return (max[0], max[1])

        if self.alltimeGraphDataUSD is not None and baseCurrency.symbol == 'USD':
            return maxUSD()
        elif self.alltimeGraphDataUSD is None \
                or baseCurrency.alltimeGraphDataUSD is None \
                or self.priceUSD is None or baseCurrency.priceUSD is None:
            return 0, None

        actualPrice = self.priceUSD / baseCurrency.priceUSD
        athPrice = None
        athDate = None
        if self.__lastCalculatedAth is None \
                or self.__lastCalculatedAth[0] != baseCurrency.symbol:
            i1, i2 = 0, 0
            l1 = len(self.alltimeGraphDataUSD)
            l2 = len(baseCurrency.alltimeGraphDataUSD)
            while i1 < l1 and i2 < l2:
                d1 = self.alltimeGraphDataUSD[i1][0]
                d2 = baseCurrency.alltimeGraphDataUSD[i2][0]
                tdelta = d1 - d2
                if tdelta.days == 0:
                    p1 = self.alltimeGraphDataUSD[i1][1]
                    p2 = baseCurrency.alltimeGraphDataUSD[i2][1]
                    price = p1 / p2
                    if athPrice is None or price > athPrice:
                        athPrice = price
                        athDate = d1
                    i1 += 1
                    i2 += 1
                elif tdelta.days < 0:
                    i1 += 1
                else:
                    i2 += 1
            self.__lastCalculatedAth = (baseCurrency.symbol, athPrice, athDate)
        else:
            athPrice = self.__lastCalculatedAth[1]
            athDate = self.__lastCalculatedAth[2]
        return (actualPrice / athPrice), athDate
