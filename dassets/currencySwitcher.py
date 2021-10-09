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
from dassets import currencies
from dassets.env import *

@Gtk.Template(filename = DATA_DIR + '/ui/currencyRowTemplate.ui')
class CurrencyRowTemplate (Gtk.ListBoxRow):
    __gtype_name__ = 'CurrencyRowTemplate'
    logoNode = Gtk.Template.Child('currencyLogo')
    nameNode = Gtk.Template.Child('currencyName')
    symbolNode = Gtk.Template.Child('currencySymbol')
    favoriteRevealerNode = Gtk.Template.Child('currencyFavoriteRevealer')

class CurrencySwitcher ():

    def __init__ (self, app):
        self.__app = app
        self.__app.addCssProvider('currencySwitcher')
        self.__node = self.__app.builder.get_object('currencyList')
        self.__node.set_sort_func(self.__currenciesSort)
        self.__node.set_filter_func(self.__currenciesFilter)
        self.__node.connect('row-activated', self.__rowActivated)
        self.actualRow = None

        self.__currencySearchRevealerNode = self.__app.builder.get_object('currencySearchRevealer')
        self.__currencySearchNode = self.__app.builder.get_object('currencySearch')
        self.__currencySearchNode.connect('search-changed', self.__searchChanged)

        controllerKey = Gtk.EventControllerKey()
        self.__currencySearchNode.add_controller(controllerKey)
        controllerKey.connect('key-pressed', self.__searchKeyPressed)

        # determinate the first currency
        firstSymbol = 'BTC'
        lastCurrencySymbol = self.__app.settings.loadLastCurrencySymbol()
        if lastCurrencySymbol in self.__app.currencies.keys():
            firstSymbol = lastCurrencySymbol

        for symbol in self.__app.currencies.keys():
            if symbol != 'USD':
                self.__addCurrency(self.__app.currencies[symbol], firstSymbol)

    def sort (self):
        """
            Sort again all currencies with the current sort method
        """
        self.__node.invalidate_sort()

    def setCurrentFavorite (self, favorite):
        """
            Make the current row favorite or not
        """
        self.actualRow.favoriteRevealerNode.set_reveal_child(favorite)

    def changeSearchVisibility (self, visible):
        """
            Change search entry state to visible or hidden
        """
        self.__currencySearchNode.set_text('')
        self.__currencySearchRevealerNode.set_reveal_child(visible)
        self.__node.invalidate_filter()

        if visible:
            self.__currencySearchNode.grab_focus()

    def searchInsertChar (self, char):
        self.__currencySearchNode.insert_text(chr(char), -1)
        self.__currencySearchNode.set_position(-1)

    ###########
    # PRIVATE #
    ###########

    def __searchKeyPressed (self, ctrl, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.__app.headerBar.setSearch(False)

    def __searchChanged (self, obj, data = None):
        self.__node.invalidate_filter()

    def __addCurrency (self, currency, firstSymbol):
        row = CurrencyRowTemplate()
        row.nameNode.set_text(currency.name)
        row.symbolNode.set_text(currency.symbol)
        row.logoNode.set_from_resource(IMG_RPATH + currency.symbol + '.png')

        if currency.favorite:
            row.favoriteRevealerNode.set_reveal_child(True)

        row.currencySymbol = currency.symbol
        row.currencyName = currency.name
        self.__node.append(row)

        if currency.symbol == firstSymbol:
            row.activate()

    def __rowActivated (self, obj, row):
        lastRow = self.actualRow
        self.actualRow = row

        if lastRow is not row and hasattr(self.__app, 'currencyView'):
            self.__app.currencyView.reload()

        if self.__currencySearchRevealerNode.get_reveal_child() is True:
            self.__app.headerBar.setSearch(False)

    def __currenciesFilter (self, row):
        """
            Tell if row should be visible or not in the list box
        """
        searchText = self.__currencySearchNode.get_text().lower()
        if searchText not in row.currencyName.lower() and searchText not in row.currencySymbol.lower():
            return False

        return True

    def __currenciesSort (self, row1, row2):
        """
            Sort between currencies row1 and row2
        """
        if self.__currencySearchNode.get_text():
            sortMethodName = 'rank'
        else:
            sortMethodName = self.__app.getActualSortMethodName()
        quote = self.__app.getActualQuote()
        cur1 = self.__app.currencies[row1.currencySymbol]
        cur2 = self.__app.currencies[row2.currencySymbol]

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
