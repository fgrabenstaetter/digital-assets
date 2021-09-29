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
from dassets.sys import currencies
from dassets.env import *

@Gtk.Template(filename = DATA_DIR + '/ui/currencyRowTemplate.ui')
class CurrencyRowTemplate (Gtk.ListBoxRow):
    __gtype_name__ = 'CurrencyRowTemplate'
    logoUiObj = Gtk.Template.Child('currencyLogo')
    nameUiObj = Gtk.Template.Child('currencyName')
    symbolUiObj = Gtk.Template.Child('currencySymbol')
    favoriteRevealerUiObj = Gtk.Template.Child('currencyFavoriteRevealer')

class CurrencySwitcher ():

    def __init__ (self, mainWindow, firstSymbol):
        """
            Init CurrencySwitcher
        """
        self.__mainWindow = mainWindow
        self.__builder = self.__mainWindow.builder
        self.__uiObj = self.__builder.get_object('currencyList')
        self.__uiObj.set_sort_func(self.__currenciesSort)
        self.__uiObj.set_filter_func(self.__currenciesFilter)
        self.__uiObj.connect('row-activated', self.__rowActivatedEvent)
        self.__currencySearchRevealerUiObj = self.__builder.get_object('currencySearchRevealer')
        self.__currencySearchUiObj = self.__builder.get_object('currencySearch')
        self.actualRow = None

        for symbol in self.__mainWindow.currencies.keys():
            if symbol != 'USD':
                self.__addCurrency(self.__mainWindow.currencies[symbol], firstSymbol)
        self.__currencySearchUiObj.connect('search-changed', self.__searchChangedEvent)
        controllerKey = Gtk.EventControllerKey()
        self.__currencySearchUiObj.add_controller(controllerKey)
        controllerKey.connect('key-pressed', self.__searchKeyPressedEvent)

    def sort (self):
        """
            Sort again all currencies with the current sort method
        """
        self.__uiObj.invalidate_sort()

    def setCurrentFavorite (self, favorite):
        """
            Make the current row favorite or not
        """
        self.actualRow.favoriteRevealerUiObj.set_reveal_child(favorite)

    def changeSearchVisibility (self, visible):
        """
            Change search entry state to visible or hidden
        """
        self.__currencySearchUiObj.set_text('')
        self.__currencySearchRevealerUiObj.set_reveal_child(visible)
        self.__uiObj.invalidate_filter()

        if visible:
            self.__currencySearchUiObj.grab_focus()

    def searchInsertChar (self, char):
        self.__currencySearchUiObj.insert_text(chr(char), -1)
        self.__currencySearchUiObj.set_position(-1)

    ###########
    # PRIVATE #
    ###########

    def __searchKeyPressedEvent (self, ctrl, keyval, keycode, state):
        """
            An key has been pressed in the search entry
        """
        if keyval == Gdk.KEY_Escape:
            self.__mainWindow.headerBar.stopSearch()

    def __searchChangedEvent (self, obj, data = None):
        """
            Called when the text in currency search entry has changed
        """
        self.__uiObj.invalidate_filter()

    def __addCurrency (self, currency, firstSymbol):
        """
            Add a currency to the currency switcher and activate firstSymbol
            correponding row
        """
        row = CurrencyRowTemplate()
        row.nameUiObj.set_text(currency.name)
        row.symbolUiObj.set_text(currency.symbol)
        row.logoUiObj.set_from_resource(PRGM_PATH + 'img/' + currency.symbol + '.svg')

        if currency.favorite:
            row.favoriteRevealerUiObj.set_reveal_child(True)

        row.currencySymbol = currency.symbol
        row.currencyName = currency.name
        self.__uiObj.append(row)

        if currency.symbol == firstSymbol:
            row.activate()

    def __rowActivatedEvent (self, obj, row):
        """
            A currency row has been activated
        """
        lastRow = self.actualRow
        self.actualRow = row

        if lastRow is not row and hasattr(self.__mainWindow, 'currencyView'):
            self.__mainWindow.currencyView.reload(True)

        if self.__currencySearchRevealerUiObj.get_reveal_child() is True:
            self.__mainWindow.headerBar.stopSearch()

    def __currenciesFilter (self, row):
        """
            Tell if row should be visible or not in the list box
        """
        searchText = self.__currencySearchUiObj.get_text().lower()
        if searchText not in row.currencyName.lower() and searchText not in row.currencySymbol.lower():
            return False

        return True

    def __currenciesSort (self, row1, row2):
        """
            Sort between currencies row1 and row2
        """

        if self.__currencySearchUiObj.get_text():
            sortMethodName = 'rank'
        else:
            sortMethodName = self.__mainWindow.getActualSortMethodName()
        quote = self.__mainWindow.getActualQuote()
        cur1 = self.__mainWindow.currencies[row1.currencySymbol]
        cur2 = self.__mainWindow.currencies[row2.currencySymbol]

        if not cur1.favorite and cur2.favorite:
            return 1
        elif cur1.favorite and not cur2.favorite:
            return -1
        else:
            # avoid two rows with None value to be randomly ordered
            rankAndNone = sortMethodName == 'rank' and cur1.rank is None and cur2.rank is None
            volumeAndNone = sortMethodName == 'volume' and cur1.dayVolumeUSD is None and cur2.dayVolumeUSD is None
            dayPriceChangeAndNone = sortMethodName == 'change' and (cur1.lastDayPriceUSD is None or cur1.priceUSD is None) and (cur2.lastDayPriceUSD is None or cur2.priceUSD is None)
            athAndNone = sortMethodName == 'ath' and ((quote.symbol == 'USD' and cur1.athUSD is None and cur2.athUSD is None and cur1.allCandlesUSD is None and cur2.allCandlesUSD is None) or (quote.symbol != 'USD' and cur1.allCandlesUSD is None and cur2.allCandlesUSD is None))

            if rankAndNone or dayPriceChangeAndNone or volumeAndNone or athAndNone:
                sortMethodName = 'name'

            if sortMethodName == 'name':
                if cur1.name.lower() < cur2.name.lower():
                    return -1
                else:
                    return 1
            elif sortMethodName == 'rank':
                if cur1.rank is None:
                    return 1
                elif cur2.rank is None:
                    return -1
                elif cur1.rank < cur2.rank:
                    return -1
                else:
                    return 1
            elif sortMethodName == 'change':
                if quote.lastDayPriceUSD is None or quote.priceUSD is None:
                    return 0
                elif cur1.lastDayPriceUSD is None or cur1.priceUSD is None:
                    return 1
                elif cur2.lastDayPriceUSD is None or cur2.priceUSD is None:
                    return -1
                else:
                    cur1DayPriceChange = float(cur1.lastDayPriceUSD) / float(quote.lastDayPriceUSD)
                    cur1DayPriceChange = (float(cur1.priceUSD) / float(quote.priceUSD)) / cur1DayPriceChange
                    cur2DayPriceChange = float(cur2.lastDayPriceUSD) / float(quote.lastDayPriceUSD)
                    cur2DayPriceChange = (float(cur2.priceUSD) / float(quote.priceUSD)) / cur2DayPriceChange
                    if cur1DayPriceChange > cur2DayPriceChange:
                        return -1
                    else:
                        return 1
            elif sortMethodName == 'volume':
                if cur1.dayVolumeUSD is None:
                    return 1
                elif cur2.dayVolumeUSD is None:
                    return -1
                elif cur1.dayVolumeUSD > cur2.dayVolumeUSD:
                    return -1
                else:
                    return 1
            elif sortMethodName == 'ath':
                if quote.priceUSD is None:
                    return 0
                elif cur1.priceUSD is None:
                    return 1
                elif cur2.priceUSD is None:
                    return -1

                cur1Ath = cur1.calculateAth(quote)
                cur2Ath = cur2.calculateAth(quote)

                if cur1Ath is None:
                    return 1
                elif cur2Ath is None:
                    return -1

                cur1AthRatio = cur1.priceUSD / quote.priceUSD / cur1Ath[0]
                cur2AthRatio = cur2.priceUSD / quote.priceUSD / cur2Ath[0]

                if cur1AthRatio > cur2AthRatio:
                    return -1
                else:
                    return 1
