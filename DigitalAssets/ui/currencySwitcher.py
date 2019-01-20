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
from gi.repository import Gtk
from DigitalAssets.data import currencies

class CurrencySwitcher (Gtk.ListBox):
    def __init__ (self, mainWindow):
        Gtk.ListBox.__init__(self, name = 'currencySwitcher')
        self.mainWindow = mainWindow
        self.currentRow = None
        self.set_sort_func(self.currenciesSort)
        self.connect('row-activated', self.rowActivatedEvent)

        for symbol in self.mainWindow.currencies.keys():
            if (symbol != 'USD'):
                self.addCurrency(self.mainWindow.currencies[symbol])

        self.currentRow = self.get_children()[0]
        self.show_all()

    def addCurrency (self, currency):
        # add a currency to the currency switcher

        row = Gtk.ListBoxRow()
        row.curName = currency.name
        row.curSymbol = currency.symbol

        icon = Gtk.Image().new_from_file(self.mainWindow.sharePath + 'img/' + currency.symbol + '.svg')

        nameBox = Gtk.Box(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 2
        )

        nameLabel = Gtk.Label(xalign = 0)
        nameLabel.set_line_wrap(True)
        nameLabel.set_markup('<b>' + currency.name + '</b>')

        favoriteImage = Gtk.Image(xalign = 1)
        favoriteImage.set_from_icon_name('starred-symbolic', 1)
        row.favoriteImageRevealer = Gtk.Revealer(transition_type = Gtk.RevealerTransitionType.CROSSFADE, transition_duration = 1000)
        row.favoriteImageRevealer.add(favoriteImage)
        if (currency.favorite):
            row.favoriteImageRevealer.set_reveal_child(True)

        nameTopBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, hexpand = True)
        nameTopBox.pack_start(nameLabel, False, False, 0)
        nameTopBox.pack_end(row.favoriteImageRevealer, True, True, 0)

        symbolLabel = Gtk.Label(currency.symbol, xalign = 0)

        nameBox.add(nameTopBox)
        nameBox.add(symbolLabel)

        box = Gtk.Box(hexpand = False)
        box.set_spacing(16)
        box.set_border_width(10)
        box.add(icon)
        box.add(nameBox)

        row.add(box)
        self.add(row)

    def rowActivatedEvent (self, obj, row):
        # a currency button has been activated

        if (self.currentRow is not None):
            if (self.currentRow is not row):
                # load stack
                if (self.mainWindow.currencies[row.curSymbol].price is not None):
                    self.mainWindow.currencyView.reload(self.mainWindow.currencies[row.curSymbol], True)

        self.currentRow = row

        # if search entry showed, hide it
        if (self.mainWindow.headerBar.searchButton.get_active() is True):
            self.mainWindow.headerBar.searchButton.clicked()

    def currenciesSort (self, row1, row2):
        # sort currencies in the currencies switcher

        sortMethodName = self.mainWindow.headerBar.actualSortMethodName
        row1Cur = self.mainWindow.currencies[row1.curSymbol]
        row2Cur = self.mainWindow.currencies[row2.curSymbol]

        if (((sortMethodName == 'rank') and ((row1Cur.rank is None) or (row2Cur.rank is None))) or ((sortMethodName == 'dayPriceChange') and ((row1Cur.lastDayPrice is None) or (row2Cur.lastDayPrice is None)))):
            sortMethodName = 'name'

        if (not row1Cur.favorite and row2Cur.favorite):
            return 1
        elif (row1Cur.favorite and not row2Cur.favorite):
            return -1
        else:
            if (sortMethodName == 'name'):
                if (row1Cur.name < row2Cur.name):
                    return -1
                else:
                    return 1
            elif (sortMethodName == 'rank'):
                if (row1Cur.rank < row2Cur.rank):
                    return -1
                else:
                    return 1
            elif (sortMethodName == 'dayPriceChange'):
                baseCurrency = self.mainWindow.currencies[self.mainWindow.headerBar.actualBaseCurrencySymbol]

                row1DayPriceChange = float(row1Cur.lastDayPrice) / float(baseCurrency.lastDayPrice)
                row1DayPriceChange = (float(row1Cur.price) / float(baseCurrency.price)) / row1DayPriceChange

                row2DayPriceChange = float(row2Cur.lastDayPrice) / float(baseCurrency.lastDayPrice)
                row2DayPriceChange = (float(row2Cur.price) / float(baseCurrency.price)) / row2DayPriceChange

                if (row1DayPriceChange > row2DayPriceChange):
                    return -1
                else:
                    return 1
            elif (sortMethodName == 'volume'):
                if (row1Cur.dayVolume > row2Cur.dayVolume):
                    return -1
                else:
                    return 1
