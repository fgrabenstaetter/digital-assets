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
from dassets.env import *
from dassets.sys import currencies
from dassets.sys.currency import Currency
from dassets.sys.settings import Settings
from dassets.ui.window import Window
from dassets.ui.settingsWindow import SettingsWindow
import signal

class Application (Gtk.Application):

    def __init__ (self):
        """
            Init Application
        """
        Gtk.Application.__init__(self)
        self.new(APP_ID, Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(PRGM_HNAME)

        self.currencies = {}
        # add USD currency
        self.currencies['USD'] = Currency('Dollars', 'USD', 'USD', None)
        self.currencies['USD'].priceUSD = 1
        self.currencies['USD'].lastPriceUSD = 1
        self.currencies['USD'].marketcapUSD = 1
        self.currencies['USD'].dayVolumeUSD = 1
        self.currencies['USD'].lastDayPriceUSD = 1
        self.currencies['USD'].lastDayMarketcapUSD = 1
        self.currencies['USD'].lastDayVolumeUSD = 1
        self.currencies['USD'].athUSD = (1, None)
        self.currencies['USD'].rank = 0

        # add digital assets
        for cur in currencies.getCurrencies():
            currency = Currency(cur[0], cur[1], cur[2], cur[3])
            self.currencies[currency.symbol] = currency

        self.__settings = Settings()
        self.__settings.loadLastCurrenciesRank(self.currencies)
        self.__settings.loadFavoriteCurrencies(self.currencies)

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)

        self.connect('startup', self.__startup)
        self.connect('activate', self.__activate)
        self.register() # emit 'startup'

    def __startup (self, app = None):
        # load CSS
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_resource(PRGM_PATH + 'css/mainWindow.css')
        Gtk.StyleContext().add_provider_for_display(Gdk.Display.get_default(), cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # load UI
        self.builder = Gtk.Builder.new_from_resource(PRGM_PATH + 'ui/mainWindow.ui')
        self.run() # emit 'activate'

    def __activate (self, app = None):
        self.__initWindows()
        self.__initActions()

    def __initWindows (self):
        self.__mainWindow = Window(self)
        self.__settingsWindow = SettingsWindow(self.builder)

        self.__aboutDialogUiObj = self.builder.get_object('aboutDialog')
        self.__settingsWindowUiObj = self.builder.get_object('settingsWindow')

        def settingsWindowKeyPressedEvent (ctrl, keyval, keycode, state):
            if keyval == Gdk.KEY_Escape: # Escape
                self.__settingsWindowUiObj.hide()

        controllerKey = Gtk.EventControllerKey()
        self.__settingsWindowUiObj.add_controller(controllerKey)
        controllerKey.connect('key-pressed', settingsWindowKeyPressedEvent)

    def actionSettingsEvent (self, action = None, data = None):
        self.__settingsWindowUiObj.show()

    def actionAboutEvent (self, action = None, data = None):
        self.__aboutDialogUiObj.show()

    def __initActions (self):
        actionSettings = Gio.SimpleAction.new('settings')
        actionSettings.connect('activate', self.actionSettingsEvent)
        self.add_action(actionSettings)

        actionAbout = Gio.SimpleAction.new('about')
        actionAbout.connect('activate', self.actionAboutEvent)
        self.add_action(actionAbout)

    def quit (self, sig = None, frame = None):
        """
            Quit the app and save some data
        """
        self.__settings.saveLastCurrenciesRank(self.currencies)
        self.__settings.saveFavoriteCurrencies(self.currencies)
        self.__settings.saveLastCurrencySymbol(self.__mainWindow.getActualCurrency().symbol)
        self.__settings.saveLastQuoteSymbol(self.__mainWindow.getActualQuote().symbol)
        self.__mainWindow.close()
