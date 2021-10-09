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

class Currency ():

    def __init__ (self, name, symbol, nomicsID, websiteURL):
        self.name = name
        self.symbol = symbol
        self.nomicsID = nomicsID
        self.websiteURL = websiteURL
        self.favorite = False

        self.priceUSD = None
        self.lastPriceUSD = None # to know if price has go up/down since last price

        self.rank = None
        self.marketcapUSD = None
        self.dayVolumeUSD = None

        self.lastDayPriceUSD = None
        self.lastDayMarketcapUSD = None
        self.lastDayVolumeUSD = None

        self.athUSD = None # None or (price, date)
        self.__lastCalculatedAth = None # None or (quote, price, date)

        self.circulatingSupply = None
        self.maxSupply = None

        self.candlesLastUpdate = 0
        # graph data is a list of (object datetime, float price)
        self.dayCandlesUSD = None
        self.monthCandlesUSD = None
        self.yearCandlesUSD = None
        self.allCandlesUSD = None

    def calculateAth (self, quote):
        """
            Calcululate the ATH price and date for this currency and quote
            @return tuple (ath, date)
        """
        if quote.symbol == 'USD' and self.athUSD is not None:
            return self.athUSD

        # function to calculate ATH only with USD quote currency
        def maxUSD ():
            max = None
            for (dt, price) in self.allCandlesUSD:
                if max is None or price > max[0]:
                    max = (price, dt)
            # convert max price to ratio and return
            return (max[0], max[1])

        if self.allCandlesUSD is not None and quote.symbol == 'USD':
            return maxUSD()
        elif self.allCandlesUSD is None or quote.allCandlesUSD is None or self.priceUSD is None or quote.priceUSD is None:
            return None

        actualPrice = self.priceUSD / quote.priceUSD
        athPrice = None
        athDate = None

        if self.__lastCalculatedAth is None or self.__lastCalculatedAth[0] != quote.symbol:
            i1, i2 = 0, 0
            l1 = len(self.allCandlesUSD)
            l2 = len(quote.allCandlesUSD)

            while i1 < l1 and i2 < l2:
                d1 = self.allCandlesUSD[i1][0]
                d2 = quote.allCandlesUSD[i2][0]
                tdelta = d1 - d2

                if tdelta.days == 0:
                    p1 = self.allCandlesUSD[i1][1]
                    p2 = quote.allCandlesUSD[i2][1]
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

            self.__lastCalculatedAth = (quote.symbol, athPrice, athDate)
        else:
            athPrice = self.__lastCalculatedAth[1]
            athDate = self.__lastCalculatedAth[2]

        return athPrice, athDate
