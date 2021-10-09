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
from gi.repository import Gtk, Gio, GLib, Gdk
from dassets import currencies
from dassets.env import *
from dassets.currency import Currency
from dassets.settings import Settings
from dassets.nomicsAPI import NomicsAPI
from dassets.settingsWindow import SettingsWindow
from dassets.headerBar import HeaderBar
from dassets.currencySwitcher import CurrencySwitcher
from dassets.currencyView import CurrencyView
import signal

class Application (Gtk.Application):

    def __init__ (self):
        Gtk.Application.__init__(self)
        self.new(APP_ID, Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_prgname(PRGM_NAME)
        GLib.set_application_name(PRGM_HNAME)

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)

        self.connect('startup', self.__startup)
        self.connect('activate', self.__activate)
        self.register() # emit 'startup'

    # core methods

    def newBuilder (self, name):
        return Gtk.Builder.new_from_resource(UI_RPATH + name + '.ui')

    def addCssProvider (self, name):
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_resource(CSS_RPATH + name + '.css')
        Gtk.StyleContext().add_provider_for_display(Gdk.Display.get_default(), cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def quit (self, sig = None, frame = None):
        self.settings.saveLastCurrenciesRank(self.currencies)
        self.settings.saveFavoriteCurrencies(self.currencies)
        self.settings.saveLastCurrencySymbol(self.getActualCurrency().symbol)
        self.settings.saveLastQuoteSymbol(self.getActualQuote().symbol)
        self.__windowNode.close()

    # utility methods

    def changeTitle (self, title):
        self.__windowNode.set_title(title)

    def showError (self, text, settingsButton = False):
        self.__errorBarNode.set_revealed(True)
        self.__errorBarTextNode.set_text(text)
        self.__errorBarButtonNode.set_visible(settingsButton)

    def hideError (self):
        self.__errorBarNode.set_revealed(False)

    def getActualCurrency (self):
        symbol = self.currencySwitcher.actualRow.currencySymbol
        return self.currencies[symbol]

    def getActualQuote (self):
        symbol = self.headerBar.actualQuoteSymbol
        return self.currencies[symbol]

    def getActualSortMethodName (self):
        """
            Return one of 'rank', 'name', 'change', 'volume', 'ath'
        """
        return self.headerBar.actualSortMethodName

    ###########
    # PRIVATE #
    ###########

    def __startup (self, app = None):
        self.builder = self.newBuilder('application')
        self.settings = Settings()
        self.run() # emit 'activate'

    def __activate (self, app = None):
        self.__initCurrencies()
        self.__initActions()
        self.__initWindows()
        self.__initWidgets()

        self.addCssProvider('global')
        self.__nomicsAPI = NomicsAPI(self)

    def __initWindows (self):
        self.__windowNode = self.builder.get_object('window')
        self.__windowNode.show()
        self.__windowNode.connect('close-request', self.quit)
        self.add_window(self.__windowNode)

        controllerKey = Gtk.EventControllerKey()
        self.__windowNode.add_controller(controllerKey)
        controllerKey.connect('key-pressed', self.__windowKeyPressed)

        self.__settingsWindow = SettingsWindow(self)
        self.__aboutDialogNode = self.builder.get_object('aboutDialog')
        self.__aboutDialogNode.set_transient_for(self.__windowNode)

    def __initActions (self):
        def actionSettingsEvent (action = None, data = None):
            self.__settingsWindow.show()

        def actionAboutEvent (action = None, data = None):
            self.__aboutDialogNode.show()

        self.actionSettings = Gio.SimpleAction.new('settings')
        self.actionSettings.connect('activate', actionSettingsEvent)
        self.add_action(self.actionSettings)

        self.actionAbout = Gio.SimpleAction.new('about')
        self.actionAbout.connect('activate', actionAboutEvent)
        self.add_action(self.actionAbout)

    def __initWidgets (self):
        # load widgets
        self.headerBar = HeaderBar(self)
        self.currencySwitcher = CurrencySwitcher(self)
        self.currencyView = CurrencyView(self)

        # error bar
        self.__errorBarNode = self.builder.get_object('errorBar')
        self.__errorBarTextNode = self.builder.get_object('errorBarText')
        self.__errorBarButtonNode = self.builder.get_object('errorBarButton')

        def errorBarButtonClicked (obj = None, data = None):
            self.actionSettings.activate()

        self.__errorBarButtonNode.connect('clicked', errorBarButtonClicked)

    def __initCurrencies (self):
        self.currencies = {}

        # add USD currency
        self.currencies['USD'] = Currency('Dollars', 'USD', 'USD', None)
        usd = self.currencies['USD']
        usd.priceUSD = 1
        usd.lastPriceUSD = 1
        usd.marketcapUSD = 1
        usd.dayVolumeUSD = 1
        usd.lastDayPriceUSD = 1
        usd.lastDayMarketcapUSD = 1
        usd.lastDayVolumeUSD = 1
        usd.athUSD = (1, None)
        usd.rank = 0

        # add crypto currencies
        for cur in currencies.getCurrencies():
            currency = Currency(cur[0], cur[1], cur[2], cur[3])
            self.currencies[currency.symbol] = currency

        self.settings.loadLastCurrenciesRank(self.currencies)
        self.settings.loadFavoriteCurrencies(self.currencies)

    def __windowKeyPressed (self, ctrl, keyval, keycode, state):
        if keyval == Gdk.KEY_f and state & Gdk.ModifierType.CONTROL_MASK:
            self.headerBar.toggleSearch()
        elif (keyval >= Gdk.KEY_A and keyval <= Gdk.KEY_Z) or (keyval >= Gdk.KEY_a and keyval <= Gdk.KEY_z):
            self.headerBar.setSearch(True)
            self.currencySwitcher.searchInsertChar(keyval)
