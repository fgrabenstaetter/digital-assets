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
from gi.repository import Gtk, Gdk
from dassets.env import *

@Gtk.Template(filename = DATA_DIR + '/ui/quoteRowTemplate.ui')
class QuoteRowTemplate (Gtk.ListBoxRow):
    __gtype_name__ = 'QuoteRowTemplate'
    logoNode = Gtk.Template.Child('quoteLogo')
    nameNode = Gtk.Template.Child('quoteName')
    symbolNode = Gtk.Template.Child('quoteSymbol')

class HeaderBar ():

    def __init__ (self, app):
        self.__app = app
        self.__app.addCssProvider('headerBar')
        self.__builder = self.__app.newBuilder('headerBar')
        self.__node = self.__builder.get_object('headerBar')
        self.__app.builder.get_object('window').set_titlebar(self.__node)

        firstSymbol = 'USD'
        lastQuoteSymbol = self.__app.settings.loadLastQuoteSymbol()
        if lastQuoteSymbol in self.__app.currencies.keys():
            firstSymbol = lastQuoteSymbol

        self.actualQuoteSymbol = firstSymbol
        self.actualSortMethodName = 'rank'

        self.__searchButtonNode = self.__builder.get_object('searchButton')
        self.__quoteButtonLogoNode = self.__builder.get_object('quoteButtonLogo')
        self.__quoteButtonNameNode = self.__builder.get_object('quoteButtonName')
        self.__quoteButtonSymbolNode = self.__builder.get_object('quoteButtonSymbol')

        self.__initSearch()
        self.__initSort()
        self.__initMenu()
        self.__initQuotes()

        self.__changeQuoteButtonText(self.__app.currencies[self.actualQuoteSymbol])

    def setSearch (self, active):
        self.__searchButtonNode.set_active(active)

    def toggleSearch (self):
        active = self.__searchButtonNode.get_active()
        self.__searchButtonNode.set_active(not active)

    ###########
    # PRIVATE #
    ###########

    def __changeQuoteButtonText (self, quote):
        self.__quoteButtonLogoNode.set_from_resource(IMG_RPATH + quote.symbol + '.png')
        self.__quoteButtonNameNode.set_text(quote.name)
        self.__quoteButtonSymbolNode.set_text(quote.symbol)

    def __sortedQuotes (self):
        """
            Return a list of quote currencies sorted by rank
        """
        if self.__app.currencies['BTC'].rank is not None:
            # sort by rank
            return sorted(list(self.__app.currencies.values()), key = lambda cur: cur.rank if cur.rank is not None else 9999)
        else:
            # sort by name
            return sorted(list(self.__app.currencies.values()), key = lambda cur: cur.name)

    def __initSearch (self):
        def searchButtonToggled (obj = None, data = None):
            self.__app.currencySwitcher.changeSearchVisibility(self.__searchButtonNode.get_active())

        self.__searchButtonNode.connect('toggled', searchButtonToggled)

    def __initSort (self):
        sortPopoverNode = self.__builder.get_object('sortPopover')
        sortButtonNode = self.__builder.get_object('sortButton')

        def sortButtonClicked (obj = None, data = None):
            sortPopoverNode.popup()

        def sortPopoverClosed (obj = None, data = None):
            sortButtonNode.set_active(False)

        def sortMethodToggled (obj, data = None):
            if not obj.get_active():
                return
            self.actualSortMethodName = obj.methodName
            sortPopoverNode.popdown()
            self.__app.currencySwitcher.sort()

        sortButtonNode.connect('clicked', sortButtonClicked)
        sortPopoverNode.connect('closed', sortPopoverClosed)

        methods = ['rank', 'name', 'change', 'volume', 'ath']
        for method in methods:
            checkButtonNode = self.__builder.get_object(method + 'Button')
            checkButtonNode.methodName = method
            checkButtonNode.connect('toggled', sortMethodToggled)

    def __initMenu (self):
        menuButtonNode = self.__builder.get_object('menuButton')
        menuPopoverNode = self.__builder.get_object('menuPopover')

        def menuButtonClicked (obj = None, data = None):
            menuPopoverNode.popup()

        def menuPopoverClosed (obj = None, data = None):
            menuButtonNode.set_active(False)

        menuButtonNode.connect('clicked', menuButtonClicked)
        menuPopoverNode.connect('closed', menuPopoverClosed)

    def __initQuotes (self):
        quoteButtonNode = self.__builder.get_object('quoteButton')
        quotePopoverNode = self.__builder.get_object('quotePopover')
        quoteSearchNode = self.__builder.get_object('quoteSearch')
        quoteListNode = self.__builder.get_object('quoteList')

        for quote in self.__sortedQuotes():
            row = QuoteRowTemplate()
            row.logoNode.set_from_resource(IMG_RPATH + quote.symbol + '.png')
            row.nameNode.set_text(quote.name)
            row.symbolNode.set_text(quote.symbol)
            row.quote = quote
            quoteListNode.append(row)

        def filterFunc (row):
            """
                Tell if row should be visible or not in the list box
            """
            searchText = quoteSearchNode.get_text().lower()
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

        quoteListNode.set_filter_func(filterFunc)
        quoteListNode.set_sort_func(sortFunc)

        def quotePopoverClosed (obj = None, data = None):
            quoteButtonNode.set_active(False)

        def quoteButtonToggled (obj = None, data = None):
            if not quoteButtonNode.get_active():
                return
            quotePopoverNode.popup()
            quoteSearchNode.set_text('')
            quoteListNode.invalidate_sort()
            quoteListNode.invalidate_filter()

        def quoteSearchChanged (obj, data = None):
            quoteListNode.invalidate_filter()

        def quoteListRowActivated (obj, row):
            self.actualQuoteSymbol = row.quote.symbol
            quoteButtonNode.set_active(False)
            self.__changeQuoteButtonText(row.quote)

            self.__app.currencySwitcher.sort()
            self.__app.currencyView.reload()
            quotePopoverNode.popdown()

        quotePopoverNode.connect('closed', quotePopoverClosed)
        quoteButtonNode.connect('toggled', quoteButtonToggled)
        quoteSearchNode.connect('search-changed', quoteSearchChanged)
        quoteListNode.connect('row-activated', quoteListRowActivated)

        def quoteSearchKeyPressed (ctrl, keyval, keycode, state):
            if keyval == Gdk.KEY_Escape:
                quotePopoverNode.popdown()

        controllerKey = Gtk.EventControllerKey()
        quoteSearchNode.add_controller(controllerKey)
        controllerKey.connect('key-pressed', quoteSearchKeyPressed)
