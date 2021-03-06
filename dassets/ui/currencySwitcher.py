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
from gi.repository import Gtk, GdkPixbuf
from dassets.sys import currencies
from dassets.env import *

class CurrencySwitcher (Gtk.ListBox):

    def __init__ (self, mainWindow):
        """
            Init CurrencySwitcher
        """
        Gtk.ListBox.__init__(self, name = 'currencySwitcher')
        self.__mainWindow = mainWindow
        self.actualRow = None
        self.set_sort_func(self.__currenciesSort)
        self.connect('row-activated', self.__rowActivatedEvent)

        for symbol in self.__mainWindow.currencies.keys():
            if symbol != 'USD':
                self.__addCurrency(self.__mainWindow.currencies[symbol])

        self.actualRow = self.get_children()[0]
        self.show_all()

    def scrollToActualChild (self):
        """
            Scroll the Gtk.ScrolledWindow
            (self.__mainWindow.currencySwitcherBox) to the current ListBoxRow
        """
        sumHeightBeforeChild = 0
        sumChildrenHeight = 0
        childIndex = self.actualRow.get_index()
        for key, child in enumerate(self.get_children()):
            if key < childIndex:
                sumHeightBeforeChild += child.get_allocated_height()
            sumChildrenHeight += child.get_allocated_height()

        value = sumHeightBeforeChild
        upper = sumChildrenHeight
        boxVadj = self.__mainWindow.currencySwitcherBox.get_vadjustment()
        stepIncrement = boxVadj.get_step_increment()
        pageIncrement = boxVadj.get_page_increment()
        pageSize = boxVadj.get_page_size()
        self.__mainWindow.currencySwitcherBox.set_vadjustment(Gtk.Adjustment \
                .new(value, 0, upper, stepIncrement, pageIncrement, pageSize))

    ###########
    # PRIVATE #
    ###########

    def __addCurrency (self, currency):
        # add a currency to the currency switcher
        """
            Add a currency to the currency switcher
        """
        row = Gtk.ListBoxRow()
        row.curName = currency.name
        row.curSymbol = currency.symbol

        pixbuf = GdkPixbuf.Pixbuf.new_from_resource_at_scale(
                PRGM_PATH + 'img/' + currency.symbol + '.svg', 32, 32, True)
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        nameBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                          spacing = 2)
        nameLabel = Gtk.Label(xalign = 0)
        nameLabel.set_line_wrap(True)
        nameLabel.set_markup('<b>' + currency.name + '</b>')

        favoriteImage = Gtk.Image(xalign = 1)
        favoriteImage.set_from_icon_name('starred-symbolic', 1)
        row.favoriteImageRevealer = Gtk.Revealer(
            transition_type = Gtk.RevealerTransitionType.CROSSFADE,
            transition_duration = 1000)
        row.favoriteImageRevealer.add(favoriteImage)

        if currency.favorite:
            row.favoriteImageRevealer.set_reveal_child(True)

        nameTopBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL,
                             hexpand = True)
        nameTopBox.pack_start(nameLabel, False, False, 0)
        nameTopBox.pack_end(row.favoriteImageRevealer, True, True, 0)

        symbolLabel = Gtk.Label(label = currency.symbol, xalign = 0)

        nameBox.add(nameTopBox)
        nameBox.add(symbolLabel)

        box = Gtk.Box(hexpand = False)
        box.set_spacing(16)
        box.set_border_width(10)
        box.add(icon)
        box.add(nameBox)

        row.add(box)
        self.add(row)

    def __rowActivatedEvent (self, obj, row):
        """
            A currency row has been activated
        """
        lastRow = self.actualRow
        self.actualRow = row

        if lastRow is not row:
            # load stack
            self.__mainWindow.currencyView.reload(True)

        # if search entry showed, hide it
        if self.__mainWindow.headerBar.searchButton.get_active() is True:
            self.__mainWindow.headerBar.searchButton.clicked()

    def __currenciesSort (self, row1, row2):
        """
            Sort between currencies row1 and row2
        """
        sortMethodName = self.__mainWindow.getActualSortMethodName()
        baseCurrency = self.__mainWindow.getActualBaseCurrency()
        row1Cur = self.__mainWindow.currencies[row1.curSymbol]
        row2Cur = self.__mainWindow.currencies[row2.curSymbol]

        if not row1Cur.favorite and row2Cur.favorite:
            return 1
        elif row1Cur.favorite and not row2Cur.favorite:
            return -1
        else:
            # avoid two rows with None value to be randomly ordered
            rankAndNone = sortMethodName == 'rank' \
                and row1Cur.rank is None and row2Cur.rank is None
            dayPriceChangeAndNone = sortMethodName == 'dayPriceChange' \
                and (row1Cur.lastDayPriceUSD is None \
                    or row1Cur.priceUSD is None) \
                and (row2Cur.lastDayPriceUSD is None \
                    or row2Cur.priceUSD is None)
            volumeAndNone = sortMethodName == 'volume' \
                and row1Cur.dayVolumeUSD is None \
                and row2Cur.dayVolumeUSD is None
            athAndNone = sortMethodName == 'ath' \
                and ((baseCurrency.symbol == 'USD' and row1Cur.athUSD is None \
                and row2Cur.athUSD is None and row1Cur.alltimeGraphDataUSD is None \
                and row2Cur.alltimeGraphDataUSD is None) or (baseCurrency.symbol != 'USD' \
                and row1Cur.alltimeGraphDataUSD is None and row2Cur.alltimeGraphDataUSD is None))

            if rankAndNone or dayPriceChangeAndNone or volumeAndNone \
                    or athAndNone:
                sortMethodName = 'name'

            if sortMethodName == 'name':
                if row1Cur.name < row2Cur.name:
                    return -1
                else:
                    return 1
            elif sortMethodName == 'rank':
                if row1Cur.rank is None:
                    return 1
                elif row2Cur.rank is None:
                    return -1
                elif row1Cur.rank < row2Cur.rank:
                    return -1
                else:
                    return 1
            elif sortMethodName == 'dayPriceChange':
                if baseCurrency.lastDayPriceUSD is None \
                        or baseCurrency.priceUSD is None:
                    return 0
                elif row1Cur.lastDayPriceUSD is None \
                        or row1Cur.priceUSD is None:
                    return 1
                elif row2Cur.lastDayPriceUSD is None \
                        or row2Cur.priceUSD is None:
                    return -1
                else:
                    row1DayPriceChange = float(row1Cur.lastDayPriceUSD) \
                                       / float(baseCurrency.lastDayPriceUSD)
                    row1DayPriceChange = (float(row1Cur.priceUSD) \
                        / float(baseCurrency.priceUSD)) / row1DayPriceChange
                    row2DayPriceChange = float(row2Cur.lastDayPriceUSD) \
                                       / float(baseCurrency.lastDayPriceUSD)
                    row2DayPriceChange = (float(row2Cur.priceUSD) \
                        / float(baseCurrency.priceUSD)) / row2DayPriceChange
                    if row1DayPriceChange > row2DayPriceChange:
                        return -1
                    else:
                        return 1
            elif sortMethodName == 'volume':
                if row1Cur.dayVolumeUSD is None:
                    return 1
                elif row2Cur.dayVolumeUSD is None:
                    return -1
                elif row1Cur.dayVolumeUSD > row2Cur.dayVolumeUSD:
                    return -1
                else:
                    return 1
            elif sortMethodName == 'ath':
                if baseCurrency.symbol == 'USD':
                    if row1Cur.athUSD is not None:
                        row1AthRatio = row1Cur.priceUSD / row1Cur.athUSD[0]
                    else:
                        row1AthRatio = row1Cur.calculateAth(baseCurrency)[0] 
                    if row2Cur.athUSD is not None:
                        row2AthRatio = row2Cur.priceUSD / row2Cur.athUSD[0]
                    else:
                        row2AthRatio = row2Cur.calculateAth(baseCurrency)[0]

                    if row1AthRatio > row2AthRatio:
                        return -1
                    else:
                        return 1
                else: # base currency != USD
                    row1AthRatio = row1Cur.calculateAth(baseCurrency)[0]
                    row2AthRatio = row2Cur.calculateAth(baseCurrency)[0]
                    if row1AthRatio > row2AthRatio:
                        return -1
                    else:
                        return 1
