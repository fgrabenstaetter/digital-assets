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
from gi.repository import Gtk, Gio, GLib, Gdk
from dassets.ui.window import Window
from dassets.env import *
from dassets.sys import currencies
from dassets.sys.currency import Currency
from dassets.sys.settings import Settings

class Application (Gtk.Application):

    def __init__ (self):
        """
            Init Application
        """
        Gtk.Application.__init__(self)
        self.new(APP_ID, Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_prgname(PRGM_NAME)
        GLib.set_application_name(PRGM_HNAME)

        # load CSS
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_resource(PRGM_PATH + 'css/style.css')
        Gtk.StyleContext().add_provider_for_screen(
            Gdk.Screen.get_default(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.currencies = {}
        # add USD currency
        self.currencies['USD'] = Currency('Dollars', 'USD', None)
        self.currencies['USD'].priceUSD = 1
        self.currencies['USD'].lastDayPriceUSD = 1
        self.currencies['USD'].athUSD = (1, None)
        self.currencies['USD'].rank = 0

        # add digital assets
        for cur in currencies.getCurrencies():
            currency = Currency(cur[0], cur[1], cur[2])
            self.currencies[currency.symbol] = currency

        self.__settings = Settings()
        self.__settings.loadLastCurrenciesRank(self.currencies)
        self.__settings.loadFavoriteCurrencies(self.currencies)
        self.__mainWindow = Window(self)

    def quit (self):
        """
            Quit the app and save some data
        """
        self.__settings.saveLastCurrenciesRank(self.currencies)
        self.__settings.saveFavoriteCurrencies(self.currencies)
        self.__settings.saveLastCurrencySymbol(self.__mainWindow.getActualCurrency().symbol)
        self.__settings.saveLastBaseCurrencySymbol(self.__mainWindow.getActualBaseCurrency().symbol)
        Gtk.main_quit()
