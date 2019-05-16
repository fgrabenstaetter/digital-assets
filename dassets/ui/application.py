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
from gi.repository import Gtk, Gio, GLib
from dassets.ui.window import Window
from dassets.env import *
from dassets.sys import currencies
from dassets.sys.currency import Currency
import pickle

class Application (Gtk.Application):

    def __init__ (self):
        """
            Init Application
        """
        Gtk.Application.__init__(self)
        self.new(PRGM_NAME, Gio.ApplicationFlags.FLAGS_NONE)
        self.register_session = True
        GLib.set_prgname(PRGM_NAME)
        GLib.set_application_name(PRGM_HNAME)

        self.currencies = {}
        # add USD currency
        self.currencies['USD'] = Currency('Dollars', 'USD', None)
        self.currencies['USD'].price = 1
        self.currencies['USD'].lastDayPrice = 1
        self.currencies['USD'].ath = 1
        self.currencies['USD'].rank = 0

        # add digital assets
        for cur in currencies.getCurrencies():
            currency = Currency(cur[0], cur[1], cur[2])
            self.currencies[currency.symbol] = currency

        # gsettings
        self.__gsettings = Gio.Settings(PRGM_NAME)

        self.__loadFavoriteCurrencies()
        self.__loadLastCurrenciesRank()
        self.__mainWindow = Window(self)

    def quit (self):
        """
            Quit the app and save some data
        """
        Gtk.main_quit()
        self.__saveFavoriteCurrencies()
        self.__saveLastCurrenciesRank()

    ###########
    # PRIVATE #
    ###########

    def __saveFavoriteCurrencies (self):
        """
            Save favorites currencies in a file to load them in the next app
            launch
        """
        dic = dict()
        for key in self.currencies.keys():
            if key != 'USD':
                dic[key] = self.currencies[key].favorite
        with open(CONFIG_DIR + '/favorites', 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dic)

    def __loadFavoriteCurrencies (self):
        """
            Load favorites currencies from a file
        """
        try:
            with open(CONFIG_DIR + '/favorites', 'rb') as file:
                unpickler = pickle.Unpickler(file)
                dic = unpickler.load()
                for key in dic.keys():
                    if key in self.currencies.keys() and dic[key] == True:
                        self.currencies[key].favorite = True
        except OSError:
            # not created now, skip
            pass

    def __saveLastCurrenciesRank (self):
        """
            Save currencies rank in a file to load them in the next app launch
        """
        if self.currencies['BTC'].rank is None:
            return

        dic = dict()
        for key in self.currencies.keys():
            if key != 'USD':
                dic[key] = self.currencies[key].rank

        with open(CONFIG_DIR + '/lastRanks', 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dic)

    def __loadLastCurrenciesRank (self):
        """
            Load last currencies rank (sorted by marketcap) to avoid the delay
            before currencies are sorted by rank after their data is downloaded
        """
        try:
            with open(CONFIG_DIR + '/lastRanks', 'rb') as file:
                unpickler = pickle.Unpickler(file)
                dic = unpickler.load()
                for key in dic.keys():
                    if key in self.currencies.keys():
                        self.currencies[key].rank = dic[key]
        except OSError:
            # not created now, skip
            pass
