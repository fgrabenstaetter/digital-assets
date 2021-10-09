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
from dassets import tools
import json

class Settings (Gio.Settings):

    def __init__ (self):
        Gio.Settings.__init__(self, schema_id = APP_ID)

    # methods to save settings

    def saveLastCurrenciesRank (self, currencies):
        if currencies['BTC'].rank is None:
            return False

        lastRanks = dict()
        for key in currencies.keys():
            if key != 'USD':
                lastRanks[key] = currencies[key].rank
        self.set_string('last-ranks', json.dumps(lastRanks))

    def saveFavoriteCurrencies (self, currencies):
        favorites = []
        for key in currencies.keys():
            if key != 'USD' and currencies[key].favorite:
                favorites.append(key)
        self.set_string('favorites', json.dumps(favorites))

    def saveNomicsAPIKey (self, apiKey):
        self.set_string('nomics-api-key', apiKey)

    def saveLastCurrencySymbol (self, currencySymbol):
        self.set_string('last-currency-symbol', currencySymbol)


    def saveLastQuoteSymbol (self, quoteSymbol):
        self.set_string('last-quote-symbol', quoteSymbol)

    # methods to load settings

    def loadFavoriteCurrencies (self, currencies):
        data = self.get_string('favorites')
        try:
            favorites = list(json.loads(data))
            for symbol in favorites:
                if symbol in currencies.keys():
                    currencies[symbol].favorite = True
        except json.JSONDecodeError:
            return False

    def loadLastCurrenciesRank (self, currencies):
        data = self.get_string('last-ranks')
        try:
            lastRanks = dict(json.loads(data))
            for symbol, rank in lastRanks.items():
                if symbol in currencies.keys():
                    currencies[symbol].rank = rank
        except json.JSONDecodeError:
            return False

    def loadNomicsAPIKey (self):
        return self.get_string('nomics-api-key')

    def loadLastCurrencySymbol (self):
        return self.get_string('last-currency-symbol')

    def loadLastQuoteSymbol (self):
        return self.get_string('last-quote-symbol')
