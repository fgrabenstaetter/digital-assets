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
import urllib.request, urllib.error, threading, json, datetime, random, datetime

class APIData ():

    def __init__ (self, mainWindow):
        """
            Init APIData
        """
        self.__mainWindow = mainWindow
        self.__settings = Settings()
        # default API key
        self.__APIKey = self.__settings.loadNomicsAPIKey()
        self.__nbReloadedloaded = 0
        self.__askInterval = 10
        self.__bigDataReloadModulo = 12
        self.__thread = None
        self.__currenciesSymbol = []
        for cur in currencies.getCurrencies():
            self.__currenciesSymbol.append(cur[1])
        self.__loop()

    ###########
    # PRIVATE #
    ###########

    def __reloadData (self):
        """
            API calls and currencies data load
        """
        # reload prices
        dataPrices = self.__reloadPrices()
        if dataPrices is not False:
            self.__setRequest('reloadCurrencyView')
            self.__setRequest('resortCurrencySwitcher')

        if (self.__nbReloadedloaded % self.__bigDataReloadModulo) == 0 \
                or self.__mainWindow.currencies['BTC'].dayVolume is None \
                or self.__mainWindow.currencies['BTC'].dayGraphData is None:
            # reload currencies general data (dashboard)
            dataInfos = self.__reloadInfos(dataPrices)
            self.__setRequest('resortCurrencySwitcher')
            if dataInfos is not False:
                self.__setRequest('reloadCurrencyView')

            # graph prices reload
            dataGraph = self.__reloadGraphData()
            if dataGraph is not False:
                self.__setRequest('reloadCurrencyView')

    def __loop (self):
        """
            Start the API call loop
        """
        def funcWrapper():
            self.__nbReloadedloaded += 1
            self.__loop()
            self.__reloadData()

        if self.__nbReloadedloaded == 0:
            timeout = 0
        else:
            timeout = self.__askInterval

        # Reload the Nomics API Key
        self.__APIKey = self.__settings.loadNomicsAPIKey()
        # Set a new timeout
        self.__thread = threading.Timer(timeout, funcWrapper)
        self.__thread.daemon = True
        self.__thread.start()

    def __setRequest (self, str):
        """
            Reload actual currency view values
        """
        if str in self.__mainWindow.apiDataRequests.keys():
            self.__mainWindow.apiDataRequests[str] = True

    def __reloadPrices (self):
        """
            Reload prices data
        """
        try:
            res = urllib.request.urlopen(
                'https://api.nomics.com/v1/prices?key=' + self.__APIKey).read()
        except urllib.error.URLError:
            # show network error message
            if self.__mainWindow.networkErrorBarRevealer.get_child_revealed() \
                                                                    is False:
                self.__mainWindow.networkErrorBarRevealer.set_reveal_child(True)

            self.__thread = threading.Timer(1, self.__reloadData)
            return False

        # hide network error message if its visible
        if self.__mainWindow.networkErrorBarRevealer.get_child_revealed() is True:
            self.__mainWindow.networkErrorBarRevealer.set_reveal_child(False)

        dataPrices = json.loads(res)
        for symbol in self.__mainWindow.currencies.keys():
            for dataCur in dataPrices:
                if dataCur['currency'] == symbol:
                    self.__mainWindow.currencies[symbol].price = \
                                                        float(dataCur['price'])
                    break
        # it is necessary for __reloadInfos to calculate the correct rank
        return dataPrices

    def __reloadInfos (self, dataPrices):
        """
            Reload general informations data (last day price, day volume,
            supply, etc.)
        """
        try:
            res = urllib.request.urlopen(
                'https://api.nomics.com/v1/dashboard?key=' + self.__APIKey).read()
        except urllib.error.URLError:
            # show network error message
            if self.__mainWindow.networkErrorBarRevealer.get_child_revealed() \
                                                                    is False:
                self.__mainWindow.networkErrorBarRevealer.set_reveal_child(True)

            self.__thread = threading.Timer(1, self.__reloadData)
            return False

        # hide network error message if its visible
        if (self.__mainWindow.networkErrorBarRevealer.get_child_revealed() \
                                                                    is True):
            self.__mainWindow.networkErrorBarRevealer.set_reveal_child(False)

        dataInfos = json.loads(res)
        for symbol in self.__mainWindow.currencies.keys():
            for dataCur in dataInfos:
                if dataCur['currency'] == symbol:
                    if dataCur['dayOpen'] is not None:
                        self.__mainWindow.currencies[symbol].lastDayPrice = \
                                                    float(dataCur['dayOpen'])
                    if dataCur['dayVolume'] is not None:
                        self.__mainWindow.currencies[symbol].dayVolume = \
                                                    float(dataCur['dayVolume'])
                    if dataCur['availableSupply'] is not None:
                        self.__mainWindow.currencies[symbol].circulatingSupply = \
                                            float(dataCur['availableSupply'])
                    if dataCur['maxSupply'] is not None:
                        self.__mainWindow.currencies[symbol].maxSupply = \
                                                    float(dataCur['maxSupply'])
                    if dataCur['high'] is not None:
                        self.__mainWindow.currencies[symbol].ath = \
                                                        float(dataCur['high'])
        # calcul rank and marketcap
        marketcapsSorted = [] # list of tuples (marketCap, symbol)
        for dataCur in dataInfos:
            for dp in dataPrices:
                if dp['currency'] == dataCur['currency']:
                    price = dp['price']
                    break

            # Warning: its possible that a coin has 'None' availableSupply, skip
            if dataCur['availableSupply'] is not None and price is not None:
                marketcapsSorted.append(
                            (float(price) * float(dataCur['availableSupply']),
                            dataCur['currency']))

        marketcapsSorted.sort(reverse = True)
        i = 1
        for marketCap, symbol in marketcapsSorted:
            if symbol in self.__mainWindow.currencies.keys():
                self.__mainWindow.currencies[symbol].marketCap = marketCap
                self.__mainWindow.currencies[symbol].rank = i
            i += 1

    def __reloadGraphData (self):
        """
            Reload graphs data (timestamps and prices)
        """
        toReload = []
        # always reload day graphs
        lastDayTime = datetime.datetime.today() - datetime.timedelta(days = 1)
        toReload.append(('day', tools.datetimeToStr(lastDayTime)))

        # reload only once month and year graphs (when the app start)
        if self.__mainWindow.currencies['BTC'].monthGraphData is None:
            lastMonthTime = datetime.datetime.today() \
                            - datetime.timedelta(days = 30)
            toReload.append(('month', tools.datetimeToStr(lastMonthTime)))

        if self.__mainWindow.currencies['BTC'].yearGraphData is None:
            lastYearTime = datetime.datetime.today() \
                           - datetime.timedelta(days = 365)
            toReload.append(('year', tools.datetimeToStr(lastYearTime)))

        if self.__mainWindow.currencies['BTC'].allGraphData is None:
            allTime = datetime.datetime(2010, 1, 1)
            toReload.append(('all', tools.datetimeToStr(allTime)))

        for graphTime in toReload:
            try:
                res = urllib.request.urlopen(
                    'https://api.nomics.com/v1/currencies/sparkline?key=' \
                    + self.__APIKey + '&start=' + graphTime[1]).read()
            except urllib.error.URLError:
                # show network error message
                if self.__mainWindow.networkErrorBarRevealer \
                                                .get_child_revealed() is False:
                    self.__mainWindow.networkErrorBarRevealer.set_reveal_child(
                                                                        True)
                self.__thread = threading.Timer(1, self.__reloadData)
                return False

            # hide network error message if its visible
            if self.__mainWindow.networkErrorBarRevealer.get_child_revealed() \
                                                                        is True:
                self.__mainWindow.networkErrorBarRevealer.set_reveal_child(False)

            dataGraphData = json.loads(res)
            def utcToLocal (dt):
                return dt.replace(tzinfo = datetime.timezone.utc) \
                         .astimezone(tz = None)

            for symbol in self.__mainWindow.currencies.keys():
                for dataCur in dataGraphData:
                    if dataCur['currency'] == symbol:
                        GraphData = []
                        for index, value in enumerate(dataCur['timestamps']):
                            dateTime = utcToLocal(datetime.datetime.strptime(
                                                value, '%Y-%m-%dT%H:%M:%SZ'))
                            GraphData.append((dateTime,
                                              float(dataCur['prices'][index])))
                        setattr(self.__mainWindow.currencies[symbol],
                                graphTime[0] + 'GraphData',
                                GraphData)
