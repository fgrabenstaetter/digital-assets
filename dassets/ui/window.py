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
from gi.repository import Gtk, Gdk, GLib
from dassets.ui.headerBar import HeaderBar
from dassets.ui.currencySwitcher import CurrencySwitcher
from dassets.ui.currencyView import CurrencyView
from dassets.sys.apiData import APIData
from dassets.sys.settings import Settings
from dassets.env import *

class Window ():

    def __init__ (self, application):
        """
            Init Window
        """
        self.__keysPressed = {'Ctrl': False, 'f': False}
        self.__application = application
        self.builder = self.__application.builder
        self.currencies = self.__application.currencies
        self.__uiObj = self.builder.get_object('mainWindow')
        self.__uiObj.set_application(self.__application)

        # Search for settings
        settings = Settings()
        quoteSymbol = settings.loadLastQuoteSymbol()
        if quoteSymbol not in self.currencies.keys():
            quoteSymbol = self.currencies.keys()[0]

        firstSymbol = 'BTC'
        lastCurrencySymbol = settings.loadLastCurrencySymbol()
        if lastCurrencySymbol in self.currencies.keys():
            firstSymbol = lastCurrencySymbol

        # load widgets
        self.headerBar = HeaderBar(self, self.currencies[quoteSymbol])
        self.currencySwitcher = CurrencySwitcher(self, firstSymbol)
        self.currencyView = CurrencyView(self)

        # load events
        def wantChangeAPIKey (obj = None, data = None):
            if data == 1:
                self.headerBar.showSettingsDialog()

        self.__errorBarUiObj = self.builder.get_object('errorBar')
        self.__errorBarTextUiObj = self.builder.get_object('errorBarText')
        self.__errorBarButtonUiObj = self.builder.get_object('errorBarButton')
        self.__errorBarButtonUiObj.connect('clicked', self.__application.actionSettingsEvent)

        controllerKey = Gtk.EventControllerKey()
        self.__uiObj.add_controller(controllerKey)
        controllerKey.connect('key-pressed', self.__keyPressEvent)

        self.__uiObj.connect('close-request', self.quit)
        self.__uiObj.show()

        # APIData requests (to avoid crash due to thread colision)
        self.apiDataRequests = {'reloadCurrencyView': False, 'resortCurrencySwitcher': False}
        self.__nextRequestsTimer()

        # load API Data
        self.__apiData = APIData(self)

    def quit (self, obj = None, data = None):
        """
            Quit event method handler, call quit method of the application
        """
        self.__application.quit()

    def close (self):
        """
            Close the window
        """
        self.__uiObj.close()

    def showError (self, text, settingsButton = False):
        self.__errorBarUiObj.set_revealed(True)
        self.__errorBarTextUiObj.set_text(text)
        self.__errorBarButtonUiObj.set_visible(settingsButton)

    def hideError (self):
        self.__errorBarUiObj.set_revealed(False)

    def getCurrencyBySymbol (self, symbol):
        """
            Return the currency which corresponds with symbol
        """
        return self.currencies[symbol]

    def getActualCurrency (self):
        """
            Return the actual currency
        """
        symbol = self.currencySwitcher.actualRow.currencySymbol
        return self.currencies[symbol]

    def getActualQuote (self):
        """
            Return the actual quote currency
        """
        symbol = self.headerBar.actualQuoteSymbol
        return self.currencies[symbol]

    def getActualSortMethodName (self):
        """
            Return the actual sort method name (rank, name, volume, day price
            variation, ath)
        """
        return self.headerBar.actualSortMethodName

    def changeTitle (self, title):
        """
            Change window title
        """
        self.__uiObj.set_title(title)

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
            self.currencySwitcher.sort()

        GLib.timeout_add(500, self.__nextRequestsTimer)

    def __keyPressEvent (self, ctrl, keyval, keycode, state):
        """
            A key has been pressed in the window
        """
        if keyval == Gdk.KEY_f and state & Gdk.ModifierType.CONTROL_MASK:
            self.headerBar.toggleSearch()
        elif (keyval >= Gdk.KEY_A and keyval <= Gdk.KEY_Z) or (keyval >= Gdk.KEY_a and keyval <= Gdk.KEY_z):
            self.headerBar.startSearch()
            self.currencySwitcher.searchInsertChar(keyval)
