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

from dassets.sys import currencies, tools
from dassets.sys.settings import Settings
from collections.abc import Iterable
import urllib.request, urllib.error, threading, json, random, datetime

class APIData ():

    def __init__ (self, mainWindow):
        """
            Init APIData
        """
        self.__mainWindow = mainWindow
        self.__settings = Settings()
        self.__APIUrl = 'https://api.nomics.com/v1/'
        self.__APIKey = self.__settings.loadNomicsAPIKey()
        self.__thread = None

        self.__loopCounter = 0
        self.__loopInterval = 2 # each 2 seconds
        self.__loopAskInfosInterval = 5 # each 10 seconds
        self.__loopAskDayCandlesInterval = 30 # each 60 seconds
        self.__loopAskInfosLast = 0
        self.__loopAskDayCandlesLast = 0
        self.__tooManyRequestsCounter = 0
        self.__tooManyRequestsMaxAlert = 3

        self.__nomicsIDToSymbol = {}
        for cur in self.__mainWindow.currencies.values():
            self.__nomicsIDToSymbol[cur.nomicsID] = cur.symbol

        self.__loop()

    ###########
    # PRIVATE #
    ###########

    def __reloadData (self):
        """
            API calls and currencies data load
        """
        bitcoin = self.__mainWindow.currencies['BTC']
        # only one request per loop tick
        # reload only once month, year and all graphs (when the app start)

        if bitcoin.priceUSD is None or self.__loopCounter >= self.__loopAskInfosLast + self.__loopAskInfosInterval:
            if self.__reloadInfos() is not False:
                self.__loopAskInfosLast += self.__loopAskInfosInterval
        elif bitcoin.dayCandlesUSD is None or self.__loopCounter >= self.__loopAskDayCandlesLast + self.__loopAskDayCandlesInterval:
            if self.__reloadCandles('day') is not False:
                self.__loopAskDayCandlesLast += self.__loopAskDayCandlesInterval
        elif bitcoin.monthCandlesUSD is None:
            self.__reloadCandles('month')
        elif bitcoin.yearCandlesUSD is None:
            self.__reloadCandles('year')
        elif bitcoin.allCandlesUSD is None:
            self.__reloadCandles('all')

        self.__setRequest('resortCurrencySwitcher')
        self.__setRequest('reloadCurrencyView')
        self.__loopCounter += 1

    def __loop (self):
        """
            Start the API call loop
        """
        def funcWrapper():
            self.__reloadData()
            self.__loop()

        # Reload the Nomics API Key
        self.__APIKey = self.__settings.loadNomicsAPIKey()
        # Set a new timeout
        self.__thread = threading.Timer(self.__loopInterval, funcWrapper)
        self.__thread.daemon = True
        self.__thread.start()

    def __setRequest (self, str):
        """
            Reload actual currency view values
        """
        if str in self.__mainWindow.apiDataRequests.keys():
            self.__mainWindow.apiDataRequests[str] = True

    def __apiRequest (self, path):
        """
            Make an API request to Nomics
            path should contain args, ex: currencies/ticker?interval=1d&ids=BTC,ETH
        """
        try:
            res = urllib.request.urlopen(self.__APIUrl + path + '&key=' + self.__APIKey).read()
        except urllib.error.HTTPError as err:
            if err.code == 429:
                self.__tooManyRequestsCounter += 1

                if self.__tooManyRequestsCounter >= self.__tooManyRequestsMaxAlert:
                    errorText = _('Too many requests with current Nomics API key, please take a new one')
                    self.__mainWindow.showError(errorText, True)
                else:
                    self.__mainWindow.hideError()
            else:
                self.__tooManyRequestsCounter = 0

                if err.code == 401:
                    errorText = _('Unauthorized access to Nomics API, please verify your key')
                    self.__mainWindow.showError(errorText, True)
                else:
                    errorText = _('HTTP error occurred') + ' (' + str(err.code) + ' - ' + str(err.reason) + ')'
                    self.__mainWindow.showError(errorText)

            return False

        except urllib.error.URLError as err:
            errorText = _('There is a network problem, please verify your connection')
            self.__mainWindow.showError(errorText)
            return False

        # to show for 4sec minimum the too many requests error message
        if self.__tooManyRequestsCounter < self.__tooManyRequestsMaxAlert:
            self.__mainWindow.hideError()
        self.__tooManyRequestsCounter = 0

        try:
            data = json.loads(res)
        except json.JSONDecodeError:
            return False

        return data

    def __reloadInfos (self):
        """
            Reload general informations data
            (price, volume, price change, supply, ATH, etc.)
        """
        nomicsIDs = ','.join(self.__nomicsIDToSymbol.keys())
        dataInfos = self.__apiRequest('currencies/ticker?interval=1d&ids=' + nomicsIDs)
        if dataInfos is False or not isinstance(dataInfos, Iterable):
            return False

        for row in dataInfos:
            if 'currency' not in row:
                continue
            nomicsID = row['currency']
            if nomicsID not in self.__nomicsIDToSymbol:
                continue
            symbol = self.__nomicsIDToSymbol[nomicsID]
            currency = self.__mainWindow.currencies[symbol]

            if 'price' in row:
                price = float(row['price'])
                if price != 0:
                    if price != currency.priceUSD:
                        currency.lastPriceUSD = currency.priceUSD
                    currency.priceUSD = price

            if 'market_cap' in row:
                currency.marketcapUSD = float(row['market_cap'])

            if 'rank' in row:
                currency.rank = int(row['rank'])

            if 'circulating_supply' in row:
                currency.circulatingSupply = float(row['circulating_supply'])

            if 'max_supply' in row:
                currency.maxSupply = float(row['max_supply'])

            if 'high' in row and 'high_timestamp' in row:
                currency.athUSD = (float(row['high']), tools.utcToLocal(datetime.datetime.strptime(row['high_timestamp'], '%Y-%m-%dT%H:%M:%SZ')))

            # day infos
            if '1d' in row:
                if 'volume' in row['1d']:
                    currency.dayVolumeUSD = float(row['1d']['volume'])

                # last day
                if currency.priceUSD is not None and 'price_change' in row['1d']:
                    dayPriceChangeUSD = float(row['1d']['price_change'])
                    currency.lastDayPriceUSD = currency.priceUSD - dayPriceChangeUSD
                if currency.marketcapUSD is not None and 'market_cap_change' in row['1d']:
                    dayMarketcapChangeUSD = float(row['1d']['market_cap_change'])
                    currency.lastDayMarketcapUSD = currency.marketcapUSD - dayMarketcapChangeUSD

                if currency.dayVolumeUSD is not None and 'volume_change' in row['1d']:
                    dayVolumeChangeUSD = float(row['1d']['volume_change'])
                    currency.lastDayVolumeUSD = currency.dayVolumeUSD - dayVolumeChangeUSD

    def __reloadCandles (self, graphName):
        """
            Reload graphs data (timestamps and prices)
            graphName is one of 'day', 'month', 'year', 'all'
        """
        nomicsIDs = ','.join(self.__nomicsIDToSymbol.keys())
        candlesStartTime = None

        if graphName == 'day':
            candlesStartTime = datetime.datetime.today() - datetime.timedelta(days = 1)
        elif graphName == 'month':
            candlesStartTime = datetime.datetime.today() - datetime.timedelta(days = 30)
        elif graphName == 'year':
            candlesStartTime = datetime.datetime.today() - datetime.timedelta(days = 365)
        elif graphName == 'all':
            candlesStartTime = datetime.datetime(2010, 1, 1)

        candlesStartTimeStr = tools.datetimeToStr(candlesStartTime)
        candlesData = self.__apiRequest('currencies/sparkline?start=' + candlesStartTimeStr + '&ids=' + nomicsIDs)
        if candlesData is False or not isinstance(candlesData, Iterable):
            return False

        for row in candlesData:
            if 'currency' not in row:
                continue

            nomicsID = row['currency']
            if nomicsID not in self.__nomicsIDToSymbol:
                continue

            symbol = self.__nomicsIDToSymbol[nomicsID]
            currency = self.__mainWindow.currencies[symbol]

            if 'timestamps' not in row \
                    or 'prices' not in row \
                    or not isinstance(row['timestamps'], Iterable) \
                    or not isinstance(row['prices'], Iterable) \
                    or len(row['timestamps']) != len(row['prices']):
                continue

            candles = []
            for index, value in enumerate(row['timestamps']):
                dateTime = tools.utcToLocal(datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ'))
                candles.append((dateTime, float(row['prices'][index])))

            setattr(currency, graphName + 'CandlesUSD', candles)
