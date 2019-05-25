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
        self.athUSD = None
        self.__lastCalculatedAthPrice = None

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
            Calcululate the ATH ratio (between 0 and 1) for the self currency
            compared to the baseCurrency
        """
        if self.alltimeGraphDataUSD is None \
                or baseCurrency.alltimeGraphDataUSD is None:
            return 0
        actualPrice = self.priceUSD / baseCurrency.priceUSD
        athPrice = None
        if self.__lastCalculatedAthPrice is None \
                or self.__lastCalculatedAthPrice[0] != baseCurrency.symbol:
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
                    i1 += 1
                    i2 += 1
                elif tdelta.days < 0:
                    i1 += 1
                else:
                    i2 += 1
            self.__lastCalculatedAthPrice = (baseCurrency.symbol, athPrice)
        else:
            athPrice = self.__lastCalculatedAthPrice[1]
        return actualPrice / athPrice
