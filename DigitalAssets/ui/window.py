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
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
from DigitalAssets.ui.headerBar import HeaderBar
from DigitalAssets.ui.currencySwitcher import CurrencySwitcher
from DigitalAssets.ui.currencyView import CurrencyView
from DigitalAssets.data.apiData import APIData
from DigitalAssets.data import currencies
from DigitalAssets.data.currency import Currency
import pickle, pathlib, os, gettext

# general paths
sharePath = '/usr/share/digital-assets/'
configPath = str(pathlib.Path.home()) + '/.config/digital-assets/'

# init translations
try:
    tr = gettext.translation('locale', localedir = sharePath + 'locale/')
    tr.install()
except OSError:
    # translation loading error
    pass

# create config path if not exists
os.makedirs(os.path.dirname(configPath), exist_ok = True)

class Window (Gtk.Window):
    def __init__ (self):
        Gtk.Window.__init__(self)
        self.set_default_size(1000, 600)

        # dirs path
        self.sharePath = sharePath
        self.configPath = configPath

        icon = GdkPixbuf.Pixbuf().new_from_file_at_scale(self.sharePath + 'img/BTC.svg', 128, 128, True)
        self.set_default_icon(icon)

        # keys
        self.keysPressed = {'Ctrl': False, 'f': False}

        # data
        self.currencies = {}
        for cur in currencies.getCurrencies():
            currency = Currency(cur[0], cur[1], cur[2])
            self.currencies[currency.symbol] = currency

        self.loadFavoriteCurrencies()
        self.loadLastCurrenciesRank()

        # USD
        self.currencies['USD'] = Currency('Dollars', 'USD', None)
        self.currencies['USD'].price = 1
        self.currencies['USD'].lastDayPrice = 1
        self.currencies['USD'].ath = 1

        # load CSS
        with open(self.sharePath + 'css/style.css', 'r') as file:
            css = file.read()

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_data(css.encode())
        Gtk.StyleContext().add_provider_for_screen(
            Gdk.Screen.get_default(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

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
        self.searchEntryBox = Gtk.Box(halign = Gtk.Align.CENTER, border_width = 10)
        self.searchEntryBox.add(self.searchEntry)
        self.searchEntryRevealer = Gtk.Revealer()
        self.searchEntryRevealer.add(self.searchEntryBox)

        leftBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        leftBox.pack_start(self.searchEntryRevealer, False, False, 0)
        leftBox.pack_end(self.currencySwitcherBox, True, True, 0)

        currencyViewBox = Gtk.ScrolledWindow()
        currencyViewBox.add(self.currencyView)

        networkErrorLabel = Gtk.Label(_('There is a network problem, please verify your connection and try again'), xalign = 0, name = 'infoBarText')
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
        self.connect('key_press_event', self.windowKeyPressEvent)
        self.connect('key_release_event', self.windowKeyReleaseEvent)
        self.searchEntry.connect('key_press_event', self.searchEntryKeyPressEvent)
        self.searchEntry.connect('search-changed', self.searchEntrySearchEvent)
        self.connect('delete_event', self.quit)
        self.show_all()

        # some tweaks
        self.searchEntryRevealer.set_reveal_child(False)
        self.networkErrorBarRevealer.set_reveal_child(False)

        # load API Data
        self.apiData = APIData(self)

    def quit (self, obj = None, data = None):
        # quit the app and save some data

        Gtk.main_quit()
        self.saveFavoriteCurrencies()
        self.saveLastCurrenciesRank()

    def windowKeyPressEvent (self, obj, data):
        # a key has been pressed in the window

        if (data.get_keyval() == (True, Gdk.KEY_Control_L)):
            self.keysPressed['Ctrl'] = True
        elif (data.get_keyval() == (True, Gdk.KEY_f)):
            self.keysPressed['f'] = True

        if ((self.keysPressed['Ctrl']) is True and (self.keysPressed['f'] is True)):
            self.headerBar.searchButton.clicked()

    def windowKeyReleaseEvent (self, obj, data):
        # a key has been released in the window

        if (data.get_keyval() == (True, Gdk.KEY_Control_L)):
            self.keysPressed['Ctrl'] = False
        elif (data.get_keyval() == (True, Gdk.KEY_f)):
            self.keysPressed['f'] = False

    def searchEntryKeyPressEvent (self, obj, data):
        # a button has been pressed in the search entry

        if (data.get_keyval() == (True, Gdk.KEY_Escape)):
            self.headerBar.searchButton.clicked()

    def searchEntrySearchEvent (self, obj, data = None):
        text = obj.get_text().lower()
        for button in self.currencySwitcher.get_children():
            if ((text not in button.curName.lower()) and (text not in button.curSymbol.lower())):
                button.hide()
            else:
                button.show()

    def saveFavoriteCurrencies (self):
        # save favorites currencies in a file to load them in the next app launch

        dic = dict()
        for key in self.currencies.keys():
            if (key != 'USD'):
                dic[key] = self.currencies[key].favorite

        with open(self.configPath + 'favorites', 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dic)

    def loadFavoriteCurrencies (self):
        # load favorites currencies name in a file

        try:
            with open(self.configPath + 'favorites', 'rb') as file:
                unpickler = pickle.Unpickler(file)
                dic = unpickler.load()

                for key in dic.keys():
                    if ((key in self.currencies.keys()) and (dic[key] == True)):
                        self.currencies[key].favorite = True
        except OSError:
            # not created now, skip
            pass

    def saveLastCurrenciesRank (self):
        # save currencies rank in a file to load them in the next app launch

        if (self.currencies['BTC'].rank is None):
            return
        dic = dict()
        for key in self.currencies.keys():
            if (key != 'USD'):
                dic[key] = self.currencies[key].rank

        with open(self.configPath + 'lastRanks', 'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dic)

    def loadLastCurrenciesRank (self):
        # load last currencies rank (sorted by marketcap) to avoid the delay before currencies are sorted by rank (default sort setting)

        try:
            with open(self.configPath + 'lastRanks', 'rb') as file:
                unpickler = pickle.Unpickler(file)
                dic = unpickler.load()

                for key in dic.keys():
                    if (key in self.currencies.keys()):
                        self.currencies[key].rank = dic[key]
        except OSError:
            # not created now, skip
            pass

    def getCurrencyBySymbol (self, symbol):
        return self.currencies[symbol]

    def getActualCurrency (self):
        symbol = self.currencySwitcher.actualRow.curSymbol
        return self.currencies[symbol]

    def getActualBaseCurrency (self):
        symbol = self.headerBar.actualBaseCurrencySymbol
        return self.currencies[symbol]

    def getActualSortMethodName (self):
        return self.headerBar.actualSortMethodName
