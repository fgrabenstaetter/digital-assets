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

import urllib.request, urllib.error, threading, json, datetime, random, datetime
from DigitalAssets.data import currencies

class APIData ():
    def __init__ (self, mainWindow):
        self.mainWindow = mainWindow
        self.APIKey = '540cc835b097c5802c1d8ff21bc5731b'
        self.nbReloaded = 0
        self.askInterval = 10
        self.bigDataReloadModulo = 12
        self.currenciesSymbol = []
        for cur in currencies.getCurrencies():
            self.currenciesSymbol.append(cur[1])

        self.loop()

    def reloadData (self):
        # API calls and currencies data load

        # reload prices
        dataPrices = self.reloadPrices()
        if (dataPrices is not False):
            self.reloadCurrentView()

        if (((self.nbReloaded % self.bigDataReloadModulo) == 0) or (self.mainWindow.currencies['BTC'].dayVolume is None) or (self.mainWindow.currencies['BTC'].dayGraphData is None)):
            # reload currencies general data (dashboard)
            dataInfos = self.reloadInfos(dataPrices)
            if (dataInfos is not False):
                self.reloadCurrentView()

            # graph prices reload
            dataGraph = self.reloadGraphData()
            if (dataGraph is not False):
                self.reloadCurrentView()

        self.mainWindow.currencySwitcher.invalidate_sort()

    def loop (self):
        # start the api call loop

        def funcWrapper():
            self.nbReloaded += 1
            self.loop()
            self.reloadData()

        if (self.nbReloaded == 0):
            timeout = 0
        else:
            timeout = self.askInterval

        self.thread = threading.Timer(timeout, funcWrapper)
        self.thread.daemon = True
        self.thread.start()

    def reloadCurrentView (self):
        # reload actual currency view values

        actualCurrency = self.mainWindow.currencies[self.mainWindow.currencySwitcher.currentRow.curSymbol]
        self.mainWindow.currencyView.reload(actualCurrency)

    def datetimeToStr (self, dt):
        # datetime to str (YYYY-MM-DDTHH-MM-SSZ)

        dtStr = '{}-{}-{}T{}:{}:{}Z'.format(str(dt.year).zfill(4), str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2), str(dt.second).zfill(2))
        return dtStr

    def reloadPrices (self):
        # reload prices data

        try:
            res = urllib.request.urlopen('https://api.nomics.com/v1/prices?key=' + self.APIKey).read()
        except urllib.error.URLError:
            # show network error message
            if (self.mainWindow.networkErrorBarRevealer.get_child_revealed() is False):
                self.mainWindow.networkErrorBarRevealer.set_reveal_child(True)

            self.thread = threading.Timer(1, self.reloadData)
            return False

        # hide network error message if its visible
        if (self.mainWindow.networkErrorBarRevealer.get_child_revealed() is True):
            self.mainWindow.networkErrorBarRevealer.set_reveal_child(False)

        dataPrices = json.loads(res)

        for symbol in self.mainWindow.currencies.keys():
            for dataCur in dataPrices:
                if (dataCur['currency'] == symbol):
                    self.mainWindow.currencies[symbol].price = float(dataCur['price'])
                    break
        return dataPrices # it is necessary for reloadInfos to calculate the correct rank

    def reloadInfos (self, dataPrices):
        # reload general informations data (last day price, day volume, supply, etc.)

        try:
            res = urllib.request.urlopen('https://api.nomics.com/v1/dashboard?key=' + self.APIKey).read()
        except urllib.error.URLError:
            # show network error message
            if (self.mainWindow.networkErrorBarRevealer.get_child_revealed() is False):
                self.mainWindow.networkErrorBarRevealer.set_reveal_child(True)

            self.thread = threading.Timer(1, self.reloadData)
            return False

        # hide network error message if its visible
        if (self.mainWindow.networkErrorBarRevealer.get_child_revealed() is True):
            self.mainWindow.networkErrorBarRevealer.set_reveal_child(False)

        dataInfos = json.loads(res)

        for symbol in self.mainWindow.currencies.keys():
            for dataCur in dataInfos:
                if (dataCur['currency'] == symbol):
                    self.mainWindow.currencies[symbol].lastDayPrice = float(dataCur['dayOpen'])
                    self.mainWindow.currencies[symbol].dayVolume = float(dataCur['dayVolume'])
                    self.mainWindow.currencies[symbol].circulatingSupply = float(dataCur['availableSupply'])

                    if (dataCur['maxSupply'] is not None):
                        self.mainWindow.currencies[symbol].maxSupply = float(dataCur['maxSupply'])

                    if (dataCur['high'] is not None):
                        self.mainWindow.currencies[symbol].ath = float(dataCur['high'])

        # calcul rank and marketcap
        marketcapsSorted = [] # list of tuples (marketCap, symbol)
        for dataCur in dataInfos:
            for dp in dataPrices:
                if (dp['currency'] == dataCur['currency']):
                    price = dp['price']
                    break

            # Warning: its possible a coin has 'None' availableSupply -> skip it
            if ((dataCur['availableSupply'] is not None) and (price is not None)):
                marketcapsSorted.append((float(price) * float(dataCur['availableSupply']), dataCur['currency']))

        marketcapsSorted.sort(reverse = True)
        i = 1
        for marketCap, symbol in marketcapsSorted:
            if (symbol in self.mainWindow.currencies.keys()):
                self.mainWindow.currencies[symbol].marketCap = marketCap
                self.mainWindow.currencies[symbol].rank = i
            i += 1

    def reloadGraphData (self):
        # reload graphs data (timestamps and prices)

        toReload = []
        # always reload day graphs
        lastDayTime = datetime.datetime.today() - datetime.timedelta(days = 1)
        toReload.append(('day', self.datetimeToStr(lastDayTime)))

        # reload only once mont and year graphs (when the app start)
        if (self.mainWindow.currencies['BTC'].monthGraphData is None):
            lastMonthTime = datetime.datetime.today() - datetime.timedelta(days = 30)
            toReload.append(('month', self.datetimeToStr(lastMonthTime)))

        if (self.mainWindow.currencies['BTC'].yearGraphData is None):
            lastYearTime = datetime.datetime.today() - datetime.timedelta(days = 365)
            toReload.append(('year', self.datetimeToStr(lastYearTime)))

        for graphTime in toReload:
            try:
                res = urllib.request.urlopen('https://api.nomics.com/v1/currencies/sparkline?key=' + self.APIKey + '&start=' + graphTime[1]).read()
            except urllib.error.URLError:
                # show network error message
                if (self.mainWindow.networkErrorBarRevealer.get_child_revealed() is False):
                    self.mainWindow.networkErrorBarRevealer.set_reveal_child(True)

                self.thread = threading.Timer(1, self.reloadData)
                return False

            # hide network error message if its visible
            if (self.mainWindow.networkErrorBarRevealer.get_child_revealed() is True):
                self.mainWindow.networkErrorBarRevealer.set_reveal_child(False)

            dataGraphData = json.loads(res)

            def utcToLocal (dt):
                return dt.replace(tzinfo = datetime.timezone.utc).astimezone(tz = None)

            for symbol in self.mainWindow.currencies.keys():
                for dataCur in dataGraphData:
                    if (dataCur['currency'] == symbol):
                        GraphData = []

                        for index, value in enumerate(dataCur['timestamps']):
                            dateTime = utcToLocal(datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ'))
                            GraphData.append((dateTime, float(dataCur['prices'][index])))

                        setattr(self.mainWindow.currencies[symbol], graphTime[0] + 'GraphData', GraphData)
