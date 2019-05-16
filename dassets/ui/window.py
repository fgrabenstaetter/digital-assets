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
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GObject
from dassets.ui.headerBar import HeaderBar
from dassets.ui.currencySwitcher import CurrencySwitcher
from dassets.ui.currencyView import CurrencyView
from dassets.sys.apiData import APIData
from dassets.sys import currencies
from dassets.sys.currency import Currency
from dassets.env import *
import pickle

class Window (Gtk.Window):

    def __init__ (self):
        """
            Init Window
        """
        Gtk.Window.__init__(self)
        self.set_default_size(1000, 600)
        icon = GdkPixbuf.Pixbuf().new_from_file_at_scale(
                                    DATA_DIR + '/img/BTC.svg', 128, 128, True)
        self.set_default_icon(icon)
        self.__keysPressed = {'Ctrl': False, 'f': False}
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

        self.__loadFavoriteCurrencies()
        self.__loadLastCurrenciesRank()

        # load CSS
        with open(DATA_DIR + '/css/style.css', 'r') as file:
            css = file.read()

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_data(css.encode())
        Gtk.StyleContext().add_provider_for_screen(
            Gdk.Screen.get_default(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # load widgets
        self.headerBar = HeaderBar(self)
        self.set_titlebar(self.headerBar)

        self.currencyView = CurrencyView(self)
        self.currencySwitcher = CurrencySwitcher(self)

        self.currencySwitcherBox = Gtk.ScrolledWindow(vexpand = True)
        self.currencySwitcherBox.set_min_content_width(200)
        self.currencySwitcherBox.set_max_content_width(200)
        self.currencySwitcherBox.add(self.currencySwitcher)

        self.searchEntry = Gtk.SearchEntry()
        self.searchEntryBox = Gtk.Box(halign = Gtk.Align.CENTER,
                                      border_width = 10)
        self.searchEntryBox.add(self.searchEntry)
        self.searchEntryRevealer = Gtk.Revealer()
        self.searchEntryRevealer.add(self.searchEntryBox)

        leftBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        leftBox.pack_start(self.searchEntryRevealer, False, False, 0)
        leftBox.pack_end(self.currencySwitcherBox, True, True, 0)

        currencyViewBox = Gtk.ScrolledWindow()
        currencyViewBox.add(self.currencyView)

        networkErrorLabel = Gtk.Label(_('There is a network problem, please' \
            + ' verify your connection and try again'),
                                      xalign = 0,
                                      name = 'infoBarText')
        networkErrorBar = Gtk.InfoBar(message_type = Gtk.MessageType.ERROR)
        networkErrorBar.pack_start(networkErrorLabel, True, True, 0)
        self.networkErrorBarRevealer = Gtk.Revealer(border_width = 10)
        self.networkErrorBarRevealer.add(networkErrorBar)

        rightBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        rightBox.pack_start(self.networkErrorBarRevealer, False, False, 0)
        rightBox.pack_end(currencyViewBox, True, True, 0)

        mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        mainBox.add(leftBox)
        mainBox.add(rightBox)
        self.add(mainBox)

        # load events
        self.connect('key_press_event', self.__windowKeyPressEvent)
        self.connect('key_release_event', self.__windowKeyReleaseEvent)
        self.searchEntry.connect('key_press_event',
                                 self.searchEntryKeyPressEvent)
        self.searchEntry.connect('search-changed', self.searchEntrySearchEvent)
        self.connect('delete_event', self.quit)
        self.show_all()

        # some tweaks
        self.searchEntryRevealer.set_reveal_child(False)
        self.networkErrorBarRevealer.set_reveal_child(False)

        # APIData requests (to avoid crash due to thread colision)
        self.apiDataRequests = {'reloadCurrencyView': False,
                                'resortCurrencySwitcher': False}
        self.__nextRequestsTimer()

        # load API Data
        self.__apiData = APIData(self)

    def quit (self, obj = None, data = None):
        """
            Quit the app and save some data
        """
        Gtk.main_quit()
        self.__saveFavoriteCurrencies()
        self.__saveLastCurrenciesRank()

    def searchEntryKeyPressEvent (self, obj, data):
        """
            A button has been pressed in the search entry
        """
        if data.get_keyval() == (True, Gdk.KEY_Escape) \
                and self.headerBar.searchButton.get_active() is True:
            self.headerBar.searchButton.clicked()

    def searchEntrySearchEvent (self, obj, data = None):
        """
            Search entry input event
        """
        text = obj.get_text().lower()
        for button in self.currencySwitcher.get_children():
            if text not in button.curName.lower() \
                    and text not in button.curSymbol.lower():
                button.hide()
            else:
                button.show()

    def getCurrencyBySymbol (self, symbol):
        """
            Return the currency which corresponds with symbol
        """
        return self.currencies[symbol]

    def getActualCurrency (self):
        """
            Return the actual currency
        """
        symbol = self.currencySwitcher.actualRow.curSymbol
        return self.currencies[symbol]

    def getActualBaseCurrency (self):
        """
            Return the actual base currency
        """
        symbol = self.headerBar.actualBaseCurrencySymbol
        return self.currencies[symbol]

    def getActualSortMethodName (self):
        """
            Return the actual sort method name (rank, name, volume, day price
            variation, ath)
        """
        return self.headerBar.actualSortMethodName

    ###########
    # PRIVATE #
    ###########

    def __nextRequestsTimer (self):
        """
            Add next timeout and execute APIData requests if there are some
            waiting
        """
        if self.apiDataRequests['reloadCurrencyView'] is True:
            self.apiDataRequests['reloadCurrencyView'] = False
            self.currencyView.reload()

        if self.apiDataRequests['resortCurrencySwitcher'] is True:
            self.apiDataRequests['resortCurrencySwitcher'] = False
            self.currencySwitcher.invalidate_sort()

        GObject.timeout_add(1000, self.__nextRequestsTimer)

    def __windowKeyPressEvent (self, obj, data):
        """
            A key has been pressed in the window
        """
        if data.get_keyval() == (True, Gdk.KEY_Control_L):
            self.__keysPressed['Ctrl'] = True
        elif data.get_keyval() == (True, Gdk.KEY_f):
            self.__keysPressed['f'] = True

        if self.__keysPressed['Ctrl'] is True and self.__keysPressed['f'] is True:
            self.headerBar.searchButton.clicked()

    def __windowKeyReleaseEvent (self, obj, data):
        """
            A key has been released in the window
        """
        if data.get_keyval() == (True, Gdk.KEY_Control_L):
            self.__keysPressed['Ctrl'] = False
        elif data.get_keyval() == (True, Gdk.KEY_f):
            self.__keysPressed['f'] = False

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
