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
gi.require_version('Gtk', '4.0')
from gi.repository import Gio
from dassets.env import *
from dassets.sys import tools
import json

class Settings (Gio.Settings):

    def __init__ (self):
        """
            Init Settings
        """
        Gio.Settings.__init__(self, schema_id = APP_ID)

    def saveLastCurrenciesRank (self, currencies):
        """
            Save last currencies ranks in GSettings
        """
        if currencies['BTC'].rank is not None:
            lastRanks = dict()
            for key in currencies.keys():
                if key != 'USD':
                    lastRanks[key] = currencies[key].rank
            self.set_string('last-ranks', json.dumps(lastRanks))

    def saveFavoriteCurrencies (self, currencies):
        """
            Save favorites currencies in GSettings
        """
        favorites = []
        for key in currencies.keys():
            if key != 'USD' and currencies[key].favorite is True:
                favorites.append(key)
        self.set_string('favorites', json.dumps(favorites))

    def saveNomicsAPIKey (self, apiKey):
        """
            Save Nomics API key in GSettings
        """
        self.set_string('nomics-api-key', apiKey)

    def saveLastCurrencySymbol (self, currencySymbol):
        """
            Save last currency symbol in GSettings
        """
        self.set_string('last-currency-symbol', currencySymbol)


    def saveLastQuoteSymbol (self, quoteSymbol):
        """
            Save last quote symbol in GSettings
        """
        self.set_string('last-quote-symbol', quoteSymbol)

    def loadFavoriteCurrencies (self, currencies):
        """
            Load favorites currencies from GSettings
        """
        data = self.get_string('favorites')
        try:
            favorites = list(json.loads(data))
            for symbol in favorites:
                if symbol in currencies.keys():
                    currencies[symbol].favorite = True
        except json.JSONDecodeError:
            tools.print_warning('GSettings \'favorites\' value is invalid')

    def loadLastCurrenciesRank (self, currencies):
        """
            Load last currencies ranks from GSettings
        """
        data = self.get_string('last-ranks')
        try:
            lastRanks = dict(json.loads(data))
            for symbol, rank in lastRanks.items():
                if symbol in currencies.keys():
                    currencies[symbol].rank = rank
        except json.JSONDecodeError:
            tools.print_warning('GSettings \'last-ranks\' value is invalid')

    def loadNomicsAPIKey (self):
        """
            Load Nomics API key from GSettings and return it
        """
        return self.get_string('nomics-api-key')

    def loadLastCurrencySymbol (self):
        """
            Load last currency symbol from GSettings and return it
        """
        return self.get_string('last-currency-symbol')

    def loadLastQuoteSymbol (self):
        """
            Load last quote symbol from GSettings and return it
        """
        return self.get_string('last-quote-symbol')
