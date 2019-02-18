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
from DigitalAssets.data import tools
from DigitalAssets.ui.graph import Graph

class CurrencyView (Gtk.Box):
    def __init__ (self, mainWindow):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, expand = True, border_width = 40)
        self.mainWindow = mainWindow
        self.actualCurrencySymbol = None
        self.actualGraphTime = None

        self.spinner1 = Gtk.Spinner()
        self.spinner1.set_size_request(200, 200)
        self.spinner1.start()
        self.add(self.spinner1)

        self.show_all()

    def create (self):
        # create widgets

        if (isinstance(self.spinner1, Gtk.Spinner)):
            self.spinner1.destroy()
            self.spinner1 = None

        # widgets
        self.image = Gtk.Image()
        self.nameLabel = Gtk.Label(name = 'currencyName', xalign = 0)
        self.symbolLabel = Gtk.Label(name = 'currencySymbol', xalign = 0)
        self.priceLabel = Gtk.Label(name = 'currencyPrice')
        self.baseCurrencySymbolLabel = Gtk.Label(name = 'currencyPrice')

        self.dayPriceChangeNameLabel = Gtk.Label(_('Change'), name = 'infoTitle', xalign = 0)
        self.dayPriceChangeLabel = Gtk.Label(xalign = 0)

        self.marketCapNameLabel = Gtk.Label(_('Markep Cap'), name = 'infoTitle', xalign = 0)
        self.marketCapLabel = Gtk.Label(xalign = 0)
        self.marketCapBaseCurrencySymbolLabel = Gtk.Label()

        self.volumeNameLabel = Gtk.Label(_('Volume'), name = 'infoTitle', xalign = 0)
        self.volumeLabel = Gtk.Label(xalign = 0)
        self.volumeBaseCurrencySymbolLabel = Gtk.Label()

        self.athNameLabel = Gtk.Label('ATH', name = 'infoTitle', xalign = 0)
        self.athLabel = Gtk.Label(xalign = 0)

        self.rankNameLabel = Gtk.Label(_('Rank'), name = 'infoTitle', xalign = 0)
        self.rankLabel = Gtk.Label(xalign = 0)

        self.circulatingSupplyNameLabel = Gtk.Label(_('Circulating Supply'), name = 'infoTitle', xalign = 0)
        self.circulatingSupplyLabel = Gtk.Label(xalign = 0)
        self.circulatingSupplyBaseCurrencySymbolLabel = Gtk.Label()

        self.maxSupplyNameLabel = Gtk.Label(_('Max Supply'), name = 'infoTitle', xalign = 0)
        self.maxSupplyLabel = Gtk.Label(xalign = 0)
        self.maxSupplyBaseCurrencySymbolLabel = Gtk.Label()

        self.websiteButton = Gtk.LinkButton(label = _('Website'), name = 'linkButton')
        actionsBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 40)

        self.favoriteButtonImage = Gtk.Image().new_from_icon_name('non-starred-symbolic', 1)
        self.favoriteButton = Gtk.ToggleButton(valign = Gtk.Align.CENTER)
        self.favoriteButton.add(self.favoriteButtonImage)
        self.favoriteButton.handlerID = self.favoriteButton.connect('toggled', self.favoriteButtonToggledEvent)

        # graph
        self.graph = Graph()

        # spinners
        self.spinner2 = Gtk.Spinner()
        self.spinner2.set_size_request(100, 100)
        self.spinner2.start()

        # containers

        # top box
        titleRightBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        titleRightBox.add(self.nameLabel)
        titleRightBox.add(self.symbolLabel)

        titleBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 40)
        titleBox.add(self.image)
        titleBox.add(titleRightBox)

        priceBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 10)
        priceBox.add(self.priceLabel)
        priceBox.add(self.baseCurrencySymbolLabel)

        topBoxMain = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 100, border_width = 20)
        topBoxMain.add(titleBox);
        topBoxMain.add(priceBox)

        topBox = Gtk.Button()
        topBox.add(topBoxMain)

        # general informations box
        dayPriceChangeBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        dayPriceChangeBox.add(self.dayPriceChangeNameLabel)
        dayPriceChangeBox.add(self.dayPriceChangeLabel)

        marketCapValueBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 10)
        marketCapValueBox.add(self.marketCapLabel)
        marketCapValueBox.add(self.marketCapBaseCurrencySymbolLabel)
        marketCapBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        marketCapBox.add(self.marketCapNameLabel)
        marketCapBox.add(marketCapValueBox)

        volumeValueBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 10)
        volumeValueBox.add(self.volumeLabel)
        volumeValueBox.add(self.volumeBaseCurrencySymbolLabel)
        volumeBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        volumeBox.add(self.volumeNameLabel)
        volumeBox.add(volumeValueBox)

        athBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        athBox.add(self.athNameLabel)
        athBox.add(self.athLabel)

        generalInfosBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 60)
        generalInfosBox.add(dayPriceChangeBox)
        generalInfosBox.add(marketCapBox)
        generalInfosBox.add(volumeBox)
        generalInfosBox.add(athBox)

        # supply infos box (and rank)
        rankBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        rankBox.add(self.rankNameLabel)
        rankBox.add(self.rankLabel)

        circulatingSupplyValueBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 10)
        circulatingSupplyValueBox.add(self.circulatingSupplyLabel)
        circulatingSupplyValueBox.add(self.circulatingSupplyBaseCurrencySymbolLabel)
        circulatingSupplyBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        circulatingSupplyBox.add(self.circulatingSupplyNameLabel)
        circulatingSupplyBox.add(circulatingSupplyValueBox)

        maxSupplyValueBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 10)
        maxSupplyValueBox.add(self.maxSupplyLabel)
        maxSupplyValueBox.add(self.maxSupplyBaseCurrencySymbolLabel)
        maxSupplyBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        maxSupplyBox.add(self.maxSupplyNameLabel)
        maxSupplyBox.add(maxSupplyValueBox)

        supplyInfosBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 60)
        supplyInfosBox.add(rankBox)
        supplyInfosBox.add(circulatingSupplyBox)
        supplyInfosBox.add(maxSupplyBox)

        # actions box
        actionsBox.add(self.websiteButton)
        actionsBox.add(self.favoriteButton)

        # graph box
        self.graphSwitcher = Gtk.StackSwitcher(halign = Gtk.Align.CENTER)
        for name, str in (('day', _('Day')), ('month', _('Month')), ('year', _('Year')), ('all', _('All'))):
            button = Gtk.ToggleButton(sensitive = False)
            button.name = name
            button.handlerID = button.connect('toggled', self.graphSwitcherButtonToggledEvent)

            buttonBox = Gtk.Box(spacing = 8, border_width = 4, halign = Gtk.Align.CENTER)
            buttonLabel = Gtk.Label(str)
            buttonSpinner = Gtk.Spinner(active = True)
            button.spinner = buttonSpinner

            buttonBox.add(buttonLabel)
            buttonBox.add(buttonSpinner)
            button.add(buttonBox)

            button.set_size_request(100, -1)
            self.graphSwitcher.add(button)

        graphBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, spacing = 30, name = 'graphBox')
        graphBox.add(self.graphSwitcher)
        graphBox.add(self.graph)

        # main containers
        infosBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, name = 'infosBox')
        infosBox.add(generalInfosBox)
        infosBox.add(supplyInfosBox)
        infosBox.add(actionsBox)

        self.infosBoxRevealer = Gtk.Revealer()
        self.infosBoxRevealer.add(infosBox)

        self.graphBoxRevealer = Gtk.Revealer()
        self.graphBoxRevealer.add(graphBox)

        bottomBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, spacing = 30)
        bottomBox.add(self.infosBoxRevealer)
        bottomBox.add(self.spinner2)
        bottomBox.add(self.graphBoxRevealer)

        mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, spacing = 40, border_width = 10, name = 'mainBox')
        mainBox.add(topBox)
        mainBox.add(bottomBox)

        self.revealer = Gtk.Revealer(transition_type = Gtk.RevealerTransitionType.CROSSFADE)
        self.revealer.add(mainBox)

        self.add(self.revealer)
        self.show_all()

    def reload (self, animate = False):
        # set widgets value

        currency = self.mainWindow.getActualCurrency()
        baseCurrency = self.mainWindow.getActualBaseCurrency()

        if ((currency.price is None) or (baseCurrency.price is None)):
            return

        if (isinstance(self.spinner1, Gtk.Widget)):
            self.create()
        elif (animate is True):
            self.revealer.destroy()
            self.revealer = None
            self.create()

        # update window title
        self.mainWindow.headerBar.set_title(currency.name + ' (' + currency.symbol + ')')

        # top (header)
        self.actualCurrencySymbol = currency.symbol
        pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_scale(self.mainWindow.sharePath + 'img/' + currency.symbol + '.svg', 100, 100, True)
        self.image.set_from_pixbuf(pixbuf)

        # name and symbol
        self.nameLabel.set_label(currency.name)
        self.symbolLabel.set_label(currency.symbol)

        # price
        nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.price, baseCurrency.price)
        priceRounded = round(currency.price / baseCurrency.price, nbDigitsAfterDecimalPoint)

        self.priceLabel.set_label(tools.beautifyNumber(priceRounded))
        self.baseCurrencySymbolLabel.set_label(baseCurrency.symbol)

        if (currency.dayVolume is not None): # only when all data has been loaded into currency
            if (self.infosBoxRevealer.get_child_revealed() is False):
                self.infosBoxRevealer.set_reveal_child(True)

            if ((self.spinner2 is not None) and (self.spinner2.get_visible() is True)):
                self.spinner2.set_size_request(60, 60)

            # general informations (day variation, day volume)

            # last day price
            dayPriceChange = currency.lastDayPrice / baseCurrency.lastDayPrice
            dayPriceChange = round(((currency.price / baseCurrency.price) / dayPriceChange) * 100 - 100, 1)
            dayPriceChangeStr = ''

            if (dayPriceChange >= 0):
                self.dayPriceChangeLabel.set_name('priceGreen')
                dayPriceChangeStr = '+ ' + str(abs(dayPriceChange)) + ' %'
            else:
                self.dayPriceChangeLabel.set_name('priceRed')
                dayPriceChangeStr = '- ' + str(abs(dayPriceChange)) + ' %'

            self.dayPriceChangeLabel.set_label(dayPriceChangeStr)

            # marketcap
            marketCapRounded = round(currency.marketCap / baseCurrency.price)
            self.marketCapLabel.set_label(tools.beautifyNumber(marketCapRounded))
            self.marketCapBaseCurrencySymbolLabel.set_label(baseCurrency.symbol)

            # day volume
            volumeRounded = round(currency.dayVolume / baseCurrency.price)
            self.volumeLabel.set_label(tools.beautifyNumber(volumeRounded))
            self.volumeBaseCurrencySymbolLabel.set_label(baseCurrency.symbol)

            # ATH (actual % relative to ATH)
            if (currency.ath is not None):
                # percentage in USD only: can't get the price of base currency at currency ATH for now
                athRelativePercentage = round((currency.price / currency.ath) * 100, 1)
                self.athLabel.set_label(str(athRelativePercentage) + ' %')
            else:
                self.athLabel.set_label(_('Undefined'))

            # rank
            self.rankLabel.set_text(str(currency.rank))

            # circulating supply
            circulatingSupplyRounded = round(currency.circulatingSupply)
            self.circulatingSupplyLabel.set_label(tools.beautifyNumber(circulatingSupplyRounded))
            self.circulatingSupplyBaseCurrencySymbolLabel.set_label(currency.symbol)

            # max supply
            maxSupplyStr = ''
            maxSupplyBaseCurrencyStr = ''
            if (currency.maxSupply is None):
                maxSupplyStr = _('Unlimited')
            else:
                maxSupplyRounded = tools.beautifyNumber(round(currency.maxSupply))
                maxSupplyStr = str(maxSupplyRounded)
                maxSupplyBaseCurrencyStr = currency.symbol

            self.maxSupplyLabel.set_label(maxSupplyStr)
            self.maxSupplyBaseCurrencySymbolLabel.set_label(maxSupplyBaseCurrencyStr)

            # actions box
            self.websiteButton.set_uri(currency.websiteURL)

            if (currency.favorite is True):
                with self.favoriteButton.handler_block(self.favoriteButton.handlerID):
                    self.favoriteButton.set_active(True)
                    self.favoriteButtonImage.set_from_icon_name('starred-symbolic', 1)

            if (currency.dayGraphData is not None): # day graph prices is the first loaded
                if (isinstance(self.spinner2, Gtk.Spinner)):
                    self.spinner2.destroy()
                    self.spinner2 = None

                if (self.graphBoxRevealer.get_child_revealed() is False):
                    self.graphBoxRevealer.set_reveal_child(True)

                # change graphSwitcher buttons sensitivity if needed
                for child in self.graphSwitcher.get_children():
                    childGraphData = getattr(currency, child.name + 'GraphData')

                    if ((child.get_sensitive() is False) and (childGraphData is not None)):
                        child.set_sensitive(True)
                        child.spinner.destroy()
                    elif ((child.get_sensitive() is True) and (childGraphData is None)):
                        child.set_sensitive(False)

                # graph set value
                if ((self.actualGraphTime is None) and (len(self.graphSwitcher.get_children()) > 0)):
                    self.graphSwitcher.get_children()[0].set_active(True)
                else:
                    for child in self.graphSwitcher.get_children():
                        if (child.name == self.actualGraphTime):
                            if (child.get_active() is True):
                                # re-activate
                                child.set_active(False)
                            child.set_active(True)
                            break

        # redraw CurrencyView widget
        self.queue_draw()

        if (self.revealer is not None):
            self.revealer.set_reveal_child(True)

    def favoriteButtonToggledEvent (self, obj = None, data = None):
        # when click on favorite button, make currency favorite or remove it from favorites

        currency = self.mainWindow.currencies[self.actualCurrencySymbol]
        currency.favorite = not currency.favorite
        if (currency.favorite is True):
            self.favoriteButtonImage.set_from_icon_name('starred-symbolic', 1)
            self.mainWindow.currencySwitcher.actualRow.favoriteImageRevealer.set_reveal_child(True)
        else:
            self.favoriteButtonImage.set_from_icon_name('non-starred-symbolic', 1)
            self.mainWindow.currencySwitcher.actualRow.favoriteImageRevealer.set_reveal_child(False)

        self.mainWindow.currencySwitcher.invalidate_sort()

    def graphSwitcherButtonToggledEvent (self, obj, data = None):
        if ((obj.get_active() is False) and (self.actualGraphTime == obj.name)):
            with obj.handler_block(obj.handlerID):
                obj.set_active(True)
        else:
            for child in self.graphSwitcher.get_children():
                if ((child is not obj) and (child.get_active() is True)):
                    with child.handler_block(child.handlerID):
                        child.set_active(False)

        self.actualGraphTime = obj.name
        currency = self.mainWindow.currencies[self.actualCurrencySymbol]
        baseCurrency = self.mainWindow.getActualBaseCurrency()
        nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.price, baseCurrency.price)

        self.graph.setGraph(getattr(currency, obj.name + 'GraphData'), obj.name, baseCurrency, nbDigitsAfterDecimalPoint)
        self.graph.redraw()
