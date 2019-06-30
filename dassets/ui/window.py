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
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GLib
from dassets.ui.headerBar import HeaderBar
from dassets.ui.currencySwitcher import CurrencySwitcher
from dassets.ui.currencyView import CurrencyView
from dassets.sys.apiData import APIData
from dassets.sys.settings import Settings
from dassets.env import *

class Window (Gtk.ApplicationWindow):

    def __init__ (self, application):
        """
            Init Window
        """
        Gtk.ApplicationWindow.__init__(self)
        self.set_default_size(1000, 600)
        icon = GdkPixbuf.Pixbuf().new_from_resource_at_scale(
                            PRGM_PATH + 'img/BTC.svg', 128, 128, True)
        self.set_default_icon(icon)
        self.__keysPressed = {'Ctrl': False, 'f': False}
        self.__application = application
        self.currencies = self.__application.currencies

        settings = Settings()

        # load widgets
        self.headerBar = HeaderBar(self, settings.loadLastBaseCurrencySymbol())
        self.set_titlebar(self.headerBar)

        self.currencyView = CurrencyView(self)
        self.currencySwitcher = CurrencySwitcher(self)
        self.currencySwitcherBox = Gtk.ScrolledWindow(vexpand = True)
        self.currencySwitcherBox.set_min_content_width(200)
        self.currencySwitcherBox.set_max_content_width(200)
        self.currencySwitcherBox.add(self.currencySwitcher)

        # activate the last currency
        lastCurrencySymbol = settings.loadLastCurrencySymbol()
        if self.currencies[lastCurrencySymbol] is not None:
            for row in self.currencySwitcher.get_children():
                if row.curSymbol == lastCurrencySymbol:
                   row.activate()
                   break

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

        networkErrorLabel = Gtk.Label.new(_('There is a network problem, please'
                                      ' verify your connection and try again'))
        networkErrorLabel.set_xalign(0)
        networkErrorLabel.set_name('infoBarText')

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
                                 self.__searchEntryKeyPressEvent)
        self.searchEntry.connect('search-changed', self.__searchEntrySearchEvent)
        self.connect('delete_event', self.quit)
        self.show_all()

        # some tweaks
        self.searchEntryRevealer.set_reveal_child(False)
        self.networkErrorBarRevealer.set_reveal_child(False)
        self.searchEntry.realize()

        # APIData requests (to avoid crash due to thread colision)
        self.apiDataRequests = {'reloadCurrencyView': False,
                                'resortCurrencySwitcher': False}
        self.__nextRequestsTimer()

        # load API Data
        self.__apiData = APIData(self)

    def quit (self, obj = None, data = None):
        """
            Quit event method handler, call quit method of the application
        """
        self.__application.quit()

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

        GLib.timeout_add(1000, self.__nextRequestsTimer)

    def __windowKeyPressEvent (self, obj, data):
        """
            A key has been pressed in the window
        """
        if data.get_keyval() == (True, Gdk.KEY_Control_L):
            self.__keysPressed['Ctrl'] = True
        elif data.get_keyval() == (True, Gdk.KEY_f):
            self.__keysPressed['f'] = True

        if self.__keysPressed['Ctrl'] is True \
                and self.__keysPressed['f'] is True:
            self.headerBar.searchButton.clicked()
        elif self.headerBar.searchButton.get_active() is False:
            self.searchEntry.grab_focus_without_selecting()
            GLib.timeout_add(0, self.__searchEntrySearchEvent)

    def __windowKeyReleaseEvent (self, obj, data):
        """
            A key has been released in the window
        """
        if data.get_keyval() == (True, Gdk.KEY_Control_L):
            self.__keysPressed['Ctrl'] = False
        elif data.get_keyval() == (True, Gdk.KEY_f):
            self.__keysPressed['f'] = False

    def __searchEntryKeyPressEvent (self, obj, data):
        """
            A button has been pressed in the search entry
        """
        if data.get_keyval() == (True, Gdk.KEY_Escape) \
                and self.headerBar.searchButton.get_active() is True:
            if len(self.searchEntry.get_text()) > 0:
                self.searchEntry.set_text('')
            else:
                self.headerBar.searchButton.clicked()

    def __searchEntrySearchEvent (self, obj = None, data = None):
        """
            Search entry input event
        """
        if (self.headerBar.searchButton.get_active() is False and len(self.searchEntry.get_text()) > 0) or (self.headerBar.searchButton.get_active() is True and len(self.searchEntry.get_text()) == 0):
            self.headerBar.searchButton.clicked()
        self.__reloadSearchResults()

    def __reloadSearchResults (self):
        """
            Reload the matching assets from the search pane
        """
        text = self.searchEntry.get_text().lower()
        for button in self.currencySwitcher.get_children():
            if text not in button.curName.lower() \
                    and text not in button.curSymbol.lower():
                button.hide()
            else:
                button.show()
