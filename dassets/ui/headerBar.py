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
from gi.repository import Gtk, Gio
from dassets.env import *
from dassets.ui.settingsWindow import SettingsWindow

@Gtk.Template(filename = DATA_DIR + '/ui/quoteRowTemplate.ui')
class QuoteRowTemplate (Gtk.ListBoxRow):
    __gtype_name__ = 'QuoteRowTemplate'
    nameUiObj = Gtk.Template.Child('quoteName')
    symbolUiObj = Gtk.Template.Child('quoteSymbol')

class HeaderBar ():

    def __init__ (self, mainWindow, defaultQuote):
        """
            Init HeaderBar
        """
        self.__mainWindow = mainWindow
        self.__builder = self.__mainWindow.builder
        self.__quotes =  self.__mainWindow.currencies
        self.__uiObj = self.__builder.get_object('mainHeaderBar')
        self.actualQuoteSymbol = defaultQuote.symbol
        self.actualSortMethodName = 'rank'

        self.__searchButtonUiObj = self.__builder.get_object('searchButton')
        self.__quoteButtonNameUiObj = self.__builder.get_object('quoteButtonName')
        self.__quoteButtonSymbolUiObj = self.__builder.get_object('quoteButtonSymbol')

        self.__initSearch()
        self.__initSort()
        self.__initMenu()
        self.__initQuotes()
        self.__changeQuoteButtonText(defaultQuote)

    def startSearch (self):
        self.__searchButtonUiObj.set_active(True)

    def stopSearch (self):
        self.__searchButtonUiObj.set_active(False)

    def toggleSearch (self):
        active = self.__searchButtonUiObj.get_active()
        self.__searchButtonUiObj.set_active(not active)

    ###########
    # PRIVATE #
    ###########

    def __changeQuoteButtonText (self, quote):
        """
            Change quote button name and symbol labels
        """
        self.__quoteButtonNameUiObj.set_text(quote.name)
        self.__quoteButtonSymbolUiObj.set_text(quote.symbol)

    def __sortedQuotes (self):
        """
            Return a sorted list of quote currencies
        """
        if self.__quotes['BTC'].rank is not None:
            # sort by rank
            return sorted(list(self.__quotes.values()), key = lambda cur: cur.rank if cur.rank is not None else 9999)
        else:
            # sort by name
            return sorted(list(self.__quotes.values()), key = lambda cur: cur.name)

    def __initSearch (self):
        """
            Init search button
        """
        def searchButtonToggledEvent (obj = None, data = None):
            self.__mainWindow.currencySwitcher.changeSearchVisibility(self.__searchButtonUiObj.get_active())

        self.__searchButtonUiObj.connect('toggled', searchButtonToggledEvent)

    def __initSort (self):
        """
            Init sort button and popover
        """
        sortPopoverUiObj = self.__builder.get_object('sortPopover')
        sortButtonUiObj = self.__builder.get_object('sortButton')

        def sortButtonClicked (obj = None, data = None):
            sortPopoverUiObj.popup()
        def sortPopoverClosedEvent (obj = None, data = None):
            sortButtonUiObj.set_active(False)

        def sortMethodClicked (obj, data = None):
            if obj.get_active() is False:
                return
            self.actualSortMethodName = obj.methodName
            sortPopoverUiObj.popdown()
            self.__mainWindow.currencySwitcher.sort()

        sortButtonUiObj.connect('clicked', sortButtonClicked)
        sortPopoverUiObj.connect('closed', sortPopoverClosedEvent)

        methods = ['rank', 'name', 'change', 'volume', 'ath']
        for method in methods:
            checkButtonUiObj = self.__builder.get_object(method + 'Button')
            checkButtonUiObj.methodName = method
            checkButtonUiObj.connect('toggled', sortMethodClicked)

    def __initMenu (self):
        """
            Init menu button and popover
        """
        menuButtonUiObj = self.__builder.get_object('menuButton')
        menuPopoverUiObj = self.__builder.get_object('menuPopover')

        def menuButtonClicked (obj = None, data = None):
            menuPopoverUiObj.popup()
        def menuPopoverClosedEvent (obj = None, data = None):
            menuButtonUiObj.set_active(False)

        menuButtonUiObj.connect('clicked', menuButtonClicked)
        menuPopoverUiObj.connect('closed', menuPopoverClosedEvent)

    def __initQuotes (self):
        """
            Init quote button and popover
        """

        quoteButtonUiObj = self.__builder.get_object('quoteButton')
        quotePopoverUiObj = self.__builder.get_object('quotePopover')
        quoteSearchUiObj = self.__builder.get_object('quoteSearch')
        quoteListUiObj = self.__builder.get_object('quoteList')

        for quote in self.__sortedQuotes():
            row = QuoteRowTemplate()
            row.nameUiObj.set_text(quote.name)
            row.symbolUiObj.set_text(quote.symbol)
            row.quote = quote
            quoteListUiObj.append(row)

        def filterFunc (row):
            """
                Tell if row should be visible or not in the list box
            """
            searchText = quoteSearchUiObj.get_text().lower()
            if (searchText not in row.quote.name.lower() and searchText not in row.quote.symbol.lower()) or row.quote.symbol == self.actualQuoteSymbol:
                return False

            return True

        def sortFunc (row1, row2):
            """
                Sort between quotes row1 and row2
            """
            quote1 = row1.quote
            quote2 = row2.quote

            if quote1.rank is None:
                return 1
            elif quote2.rank is None:
                return -1
            elif quote1.rank < quote2.rank:
                return -1
            else:
                return 1

        quoteListUiObj.set_filter_func(filterFunc)
        quoteListUiObj.set_sort_func(sortFunc)

        def quotePopoverClosedEvent (obj = None, data = None):
            quoteButtonUiObj.set_active(False)

        def quoteButtonToggledEvent (obj = None, data = None):
            if quoteButtonUiObj.get_active() is False:
                return
            quotePopoverUiObj.popup()
            quoteSearchUiObj.set_text('')
            quoteListUiObj.invalidate_sort()
            quoteListUiObj.invalidate_filter()

        def quoteSearchEvent (obj, data = None):
            text = obj.get_text().lower()
            quoteListUiObj.invalidate_filter()

        def quoteSearchKeyPressEvent (ctrl, keyval, keycode, state):
            if keyval == Gdk.KEY_Escape:
                quotePopoverUiObj.popdown()

        def quoteListRowActivatedEvent (obj, row):
            self.actualQuoteSymbol = row.quote.symbol
            quoteButtonUiObj.set_active(False)
            self.__changeQuoteButtonText(row.quote)

            self.__mainWindow.currencySwitcher.sort()
            self.__mainWindow.currencyView.reload()
            quotePopoverUiObj.popdown()

        quotePopoverUiObj.connect('closed', quotePopoverClosedEvent)
        quoteButtonUiObj.connect('toggled', quoteButtonToggledEvent)
        quoteSearchUiObj.connect('search-changed', quoteSearchEvent)
        quoteListUiObj.connect('row-activated', quoteListRowActivatedEvent)

        controllerKey = Gtk.EventControllerKey()
        quoteSearchUiObj.add_controller(controllerKey)
        controllerKey.connect('key-pressed', quoteSearchKeyPressEvent)
