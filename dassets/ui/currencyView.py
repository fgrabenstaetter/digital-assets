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
from dassets.sys import tools
from dassets.ui.graph import Graph
from dassets.env import *
import datetime

class CurrencyView (Gtk.Box):

    def __init__ (self, mainWindow):
        """
            Init CurrencyView
        """
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, expand = True, border_width = 32)
        self.__mainWindow = mainWindow
        self.__actualGraphTime = None
        self.__create()

    def reload (self, animate = False):
        """
            Reload widgets values according to the actual currency and the
            actual quote currency
        """
        currency = self.__mainWindow.getActualCurrency()
        quoteCurrency = self.__mainWindow.getActualQuoteCurrency()

        if animate is True:
            self.__revealer.destroy()
            self.__revealer = None
            self.__create()

        # update window title
        self.__mainWindow.headerBar.set_title(currency.name + ' (' + currency.symbol + ')')

        # top (header)
        pixbuf = GdkPixbuf.Pixbuf().new_from_resource_at_scale(PRGM_PATH + 'img/' + currency.symbol + '.svg', 100, 100, True)
        self.__image.set_from_pixbuf(pixbuf)

        # name and symbol
        self.__nameLabel.set_text(currency.name)
        self.__symbolLabel.set_text(currency.symbol)

        # price
        if currency.priceUSD is None or quoteCurrency.priceUSD is None:
            priceText = '. . .'
            self.__priceUpDownLabel.set_text('')
        else:
            if currency.lastPriceUSD is not None and quoteCurrency.lastPriceUSD is not None:
                actualPrice = currency.priceUSD / quoteCurrency.priceUSD
                lastPrice = currency.lastPriceUSD / quoteCurrency.lastPriceUSD

                if actualPrice < lastPrice:
                    self.__priceUpDownLabel.set_text('↓')
                    self.__priceUpDownLabel.set_name('currencyPriceDown')
                elif actualPrice > lastPrice:
                    self.__priceUpDownLabel.set_text('↑')
                    self.__priceUpDownLabel.set_name('currencyPriceUp')
                else:
                    self.__priceUpDownLabel.set_text('')
            else:
                self.__priceUpDownLabel.set_text('')

            nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quoteCurrency.priceUSD)
            priceRounded = round(currency.priceUSD / quoteCurrency.priceUSD, nbDigitsAfterDecimalPoint)
            priceText = tools.beautifyNumber(priceRounded)

        self.__priceLabel.set_text(priceText)
        self.__quoteCurrencySymbolLabel.set_text(quoteCurrency.symbol)

        # actions box
        self.__websiteButton.set_uri(currency.websiteURL)

        if currency.favorite is True:
            with self.__favoriteButton.handler_block(self.__favoriteButton.handlerID):
                self.__favoriteButton.set_active(True)
                self.__favoriteButtonImage.set_from_icon_name('starred-symbolic', 1)

        if currency.priceUSD is not None:
            if self.__infosBoxRevealer.get_child_revealed() is False:
                self.__infosBoxRevealer.set_reveal_child(True)

            if self.__spinnerInfos is not None:
                self.__spinnerInfos.set_size_request(60, 60)

            # general informations (day variation, day volume)

            # last day price
            if currency.lastDayPriceUSD is None or currency.priceUSD is None or quoteCurrency.lastDayPriceUSD is None or quoteCurrency.priceUSD is None:
                self.__dayPriceChangeLabel.set_text(_('Undefined'))
            else:
                dayPriceChange = currency.lastDayPriceUSD / quoteCurrency.lastDayPriceUSD
                dayPriceChange = round(((currency.priceUSD / quoteCurrency.priceUSD) / dayPriceChange) * 100 - 100, 1)
                dayPriceChangeStr = ''
                if dayPriceChange > 0:
                    self.__dayPriceChangeLabel.set_name('priceGreen')
                    dayPriceChangeStr = '+ ' + str(abs(dayPriceChange)) + ' %'
                elif dayPriceChange < 0:
                    self.__dayPriceChangeLabel.set_name('priceRed')
                    dayPriceChangeStr = '- ' + str(abs(dayPriceChange)) + ' %'
                else:
                    self.__dayPriceChangeLabel.set_name('priceGrey')
                    dayPriceChangeStr = '0 %'
                self.__dayPriceChangeLabel.set_text(dayPriceChangeStr)

            # marketcap
            if currency.marketCapUSD is None or quoteCurrency.priceUSD is None:
                self.__marketCapLabel.set_text(_('Undefined'))
            else:
                marketCapRounded = round(currency.marketCapUSD / quoteCurrency.priceUSD)
                self.__marketCapLabel.set_text(tools.beautifyNumber(marketCapRounded))
                self.__marketCapQuoteCurrencySymbolLabel.set_text(quoteCurrency.symbol)

            # day volume
            if currency.dayVolumeUSD is None or quoteCurrency.priceUSD is None:
                self.__volumeLabel.set_text(_('Undefined'))
            else:
                volumeRounded = round(currency.dayVolumeUSD / quoteCurrency.priceUSD)
                self.__volumeLabel.set_text(tools.beautifyNumber(volumeRounded))
                self.__volumeQuoteCurrencySymbolLabel.set_text(quoteCurrency.symbol)

            # ATH (actual % relative to ATH)
            if quoteCurrency.symbol == 'USD' and currency.athUSD is not None and currency.priceUSD is not None:
                if self.__spinnerATH.get_visible() is True:
                    self.__spinnerATH.hide()
                    self.__athLabel.show()

                athPercentage = round((currency.priceUSD / currency.athUSD[0]) * 100, 1)
                self.__athLabel.set_text(str(athPercentage) + ' %')

                athPrice = currency.athUSD[0]
                bestDecimalDigitsNb = tools.bestDigitsNumberAfterDecimalPoint(athPrice, 1)
                dtStr = str(tools.beautifyNumber(round(athPrice, bestDecimalDigitsNb))) + ' ' + quoteCurrency.symbol + ' - '
                dtStr += currency.athUSD[1].strftime('%x')
                self.__athLabel.set_tooltip_text(dtStr)

            elif currency.alltimeGraphDataUSD is not None and currency.priceUSD is not None and quoteCurrency.priceUSD is not None and (quoteCurrency.alltimeGraphDataUSD is not None or quoteCurrency.symbol == 'USD'):
                self.__spinnerATH.hide()
                self.__athLabel.show()
                ath = currency.calculateAth(quoteCurrency)
                athPercentage = round(ath[0] * 100, 1)
                self.__athLabel.set_text(str(athPercentage) + ' %')

                athPrice = (currency.priceUSD / quoteCurrency.priceUSD) / ath[0]
                bestDecimalDigitsNb = tools.bestDigitsNumberAfterDecimalPoint(athPrice, 1)
                dtStr = str(tools.beautifyNumber(round(athPrice, bestDecimalDigitsNb))) + ' ' + quoteCurrency.symbol + ' - '
                dtStr += ath[1].strftime('%x')
                self.__athLabel.set_tooltip_text(dtStr)
            else:
                self.__spinnerATH.show()
                self.__athLabel.hide()

            # rank
            if currency.rank is None:
                self.__rankLabel.set_text(_('Undefined'))
            else:
                self.__rankLabel.set_text(str(currency.rank))

            # circulating supply
            if currency.circulatingSupply is None:
                self.__circulatingSupplyLabel.set_text(_('Undefined'))
            else:
                circulatingSupplyRounded = round(currency.circulatingSupply)
                self.__circulatingSupplyLabel.set_text(tools.beautifyNumber(circulatingSupplyRounded))
                self.__circulatingSupplyQuoteCurrencySymbolLabel.set_text(currency.symbol)

            # max supply
            if currency.maxSupply is None:
                self.__maxSupplyLabel.set_text(_('Undefined'))
            else:
                maxSupplyRounded = tools.beautifyNumber(round(currency.maxSupply))
                self.__maxSupplyLabel.set_text(str(maxSupplyRounded))
                self.__maxSupplyQuoteCurrencySymbolLabel.set_text(currency.symbol)

            # day graph prices is the first loaded
            if currency.dayGraphDataUSD is not None:
                self.__spinnerInfos.destroy()

                if self.__graphBoxRevealer.get_child_revealed() is False:
                    self.__graphBoxRevealer.set_reveal_child(True)

                # change graphSwitcher buttons sensitivity if needed
                for child in self.__graphSwitcher.get_children():
                    childGraphData = getattr(currency, child.name + 'GraphDataUSD')

                    if child.get_sensitive() is False and childGraphData is not None:
                        child.set_sensitive(True)
                        child.spinner.destroy()
                    elif child.get_sensitive() is True and childGraphData is None:
                        child.set_sensitive(False)

                # graph set value
                if self.__actualGraphTime is None:
                    self.__graphSwitcher.get_children()[0].set_active(True)
                else:
                    for child in self.__graphSwitcher.get_children():
                        if child.name == self.__actualGraphTime:
                            # always re-update
                            child.set_active(True)
                            break

        if self.__revealer is not None:
            self.__revealer.set_reveal_child(True)

    ###########
    # PRIVATE #
    ###########

    def __create (self):
        """
            Create widgets
        """
        # widgets
        self.__image = Gtk.Image()
        self.__nameLabel = Gtk.Label(name = 'currencyName', xalign = 0)
        self.__symbolLabel = Gtk.Label(name = 'currencySymbol', xalign = 0)
        self.__priceUpDownLabel = Gtk.Label()
        self.__priceLabel = Gtk.Label(name = 'currencyPrice')
        self.__quoteCurrencySymbolLabel = Gtk.Label(name = 'quote')

        self.__dayPriceChangeNameLabel = Gtk.Label(label = _('Change'), name = 'infoTitle')
        self.__dayPriceChangeLabel = Gtk.Label()

        self.__marketCapNameLabel = Gtk.Label(label = _('Market Cap'), name = 'infoTitle')
        self.__marketCapLabel = Gtk.Label()
        self.__marketCapQuoteCurrencySymbolLabel = Gtk.Label(name = 'quote')

        self.__volumeNameLabel = Gtk.Label(label = _('Volume'), name = 'infoTitle')
        self.__volumeLabel = Gtk.Label()
        self.__volumeQuoteCurrencySymbolLabel = Gtk.Label(name = 'quote')

        self.__athNameLabel = Gtk.Label(label = 'ATH', name = 'infoTitle')
        self.__athLabel = Gtk.Label(visible = None)

        self.__rankNameLabel = Gtk.Label(label = _('Rank'), name = 'infoTitle')
        self.__rankLabel = Gtk.Label()

        self.__circulatingSupplyNameLabel = Gtk.Label(label = _('Circulating Supply'), name = 'infoTitle')
        self.__circulatingSupplyLabel = Gtk.Label()
        self.__circulatingSupplyQuoteCurrencySymbolLabel = Gtk.Label(name = 'quote')

        self.__maxSupplyNameLabel = Gtk.Label(label = _('Max Supply'), name = 'infoTitle')
        self.__maxSupplyLabel = Gtk.Label()
        self.__maxSupplyQuoteCurrencySymbolLabel = Gtk.Label(name = 'quote')

        # graph
        self.__graph = Graph()

        # website link and favorite button
        self.__websiteButton = Gtk.LinkButton(label = _('Website'), name = 'linkButton')

        self.__favoriteButtonImage = Gtk.Image().new_from_icon_name('non-starred-symbolic', 1)
        self.__favoriteButton = Gtk.ToggleButton(valign = Gtk.Align.CENTER)
        self.__favoriteButton.add(self.__favoriteButtonImage)
        self.__favoriteButton.handlerID = self.__favoriteButton.connect('toggled', self.__favoriteButtonToggledEvent)

        # spinners
        self.__spinnerATH = Gtk.Spinner(active = True)
        self.__spinnerInfos = Gtk.Spinner(active = True)
        self.__spinnerInfos.set_size_request(100, 100)

        # containers

        # top box
        titleRightBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, valign = Gtk.Align.CENTER, spacing = 10)
        titleRightBox.add(self.__nameLabel)
        titleRightBox.add(self.__symbolLabel)

        titleBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 40)
        titleBox.add(self.__image)
        titleBox.add(titleRightBox)

        priceBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 10, name = 'priceBox')
        priceBox.add(self.__priceUpDownLabel)
        priceBox.add(self.__priceLabel)
        priceBox.add(self.__quoteCurrencySymbolLabel)

        topBoxMain = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 100, border_width = 20)
        topBoxMain.add(titleBox);
        topBoxMain.add(priceBox)

        topBox = Gtk.Button()
        topBox.add(topBoxMain)

        # general informations box
        dayPriceChangeBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10, halign = Gtk.Align.CENTER)
        dayPriceChangeBox.add(self.__dayPriceChangeNameLabel)
        dayPriceChangeBox.add(self.__dayPriceChangeLabel)

        marketCapValueBox = Gtk.Box(spacing = 10, halign = Gtk.Align.CENTER)
        marketCapValueBox.add(self.__marketCapLabel)
        marketCapValueBox.add(self.__marketCapQuoteCurrencySymbolLabel)
        marketCapBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        marketCapBox.add(self.__marketCapNameLabel)
        marketCapBox.add(marketCapValueBox)

        volumeValueBox = Gtk.Box(spacing = 10, halign = Gtk.Align.CENTER)
        volumeValueBox.add(self.__volumeLabel)
        volumeValueBox.add(self.__volumeQuoteCurrencySymbolLabel)
        volumeBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        volumeBox.add(self.__volumeNameLabel)
        volumeBox.add(volumeValueBox)

        athBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10, halign = Gtk.Align.CENTER)
        athBox.add(self.__athNameLabel)
        athBox.add(self.__athLabel)
        athBox.add(self.__spinnerATH)

        generalInfosBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 60)
        generalInfosBox.add(dayPriceChangeBox)
        generalInfosBox.add(marketCapBox)
        generalInfosBox.add(volumeBox)
        generalInfosBox.add(athBox)

        # supply infos box (and rank)
        rankBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10, halign = Gtk.Align.CENTER)
        rankBox.add(self.__rankNameLabel)
        rankBox.add(self.__rankLabel)

        circulatingSupplyValueBox = Gtk.Box(spacing = 10, halign = Gtk.Align.CENTER)
        circulatingSupplyValueBox.add(self.__circulatingSupplyLabel)
        circulatingSupplyValueBox.add(self.__circulatingSupplyQuoteCurrencySymbolLabel)
        circulatingSupplyBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        circulatingSupplyBox.add(self.__circulatingSupplyNameLabel)
        circulatingSupplyBox.add(circulatingSupplyValueBox)

        maxSupplyValueBox = Gtk.Box(spacing = 10, halign = Gtk.Align.CENTER)
        maxSupplyValueBox.add(self.__maxSupplyLabel)
        maxSupplyValueBox.add(self.__maxSupplyQuoteCurrencySymbolLabel)
        maxSupplyBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        maxSupplyBox.add(self.__maxSupplyNameLabel)
        maxSupplyBox.add(maxSupplyValueBox)

        supplyInfosBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 60)
        supplyInfosBox.add(rankBox)
        supplyInfosBox.add(circulatingSupplyBox)
        supplyInfosBox.add(maxSupplyBox)

        # actions box
        actionsBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 40)
        actionsBox.add(self.__websiteButton)
        actionsBox.add(self.__favoriteButton)

        # graph box
        self.__graphSwitcher = Gtk.StackSwitcher(halign = Gtk.Align.CENTER)

        for name, str in (('day', _('Day')),
                          ('month', _('Month')),
                          ('year', _('Year')),
                          ('alltime', _('All'))):
            button = Gtk.ToggleButton(sensitive = False)
            button.name = name
            button.handlerID = button.connect('toggled', self.__graphSwitcherButtonToggledEvent)

            buttonBox = Gtk.Box(spacing = 8, border_width = 4, halign = Gtk.Align.CENTER)
            buttonLabel = Gtk.Label.new(str)
            buttonSpinner = Gtk.Spinner(active = True)
            button.spinner = buttonSpinner

            buttonBox.add(buttonLabel)
            buttonBox.add(buttonSpinner)
            button.add(buttonBox)

            button.set_size_request(100, -1)
            self.__graphSwitcher.add(button)

        graphBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, spacing = 30, name = 'graphBox')
        graphBox.add(self.__graphSwitcher)
        graphBox.add(self.__graph)

        # main containers
        infosBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, name = 'infosBox')
        infosBox.add(generalInfosBox)
        infosBox.add(supplyInfosBox)

        self.__infosBoxRevealer = Gtk.Revealer()
        self.__infosBoxRevealer.add(infosBox)
        self.__graphBoxRevealer = Gtk.Revealer()
        self.__graphBoxRevealer.add(graphBox)

        bottomBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, spacing = 30)
        bottomBox.add(self.__infosBoxRevealer)
        bottomBox.add(self.__spinnerInfos)
        bottomBox.add(self.__graphBoxRevealer)

        mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, spacing = 40, border_width = 10, name = 'mainBox')
        mainBox.add(topBox)
        mainBox.add(bottomBox)
        mainBox.add(actionsBox)

        self.__revealer = Gtk.Revealer(transition_type = Gtk.RevealerTransitionType.CROSSFADE)
        self.__revealer.add(mainBox)

        self.add(self.__revealer)
        self.show_all()

    def __favoriteButtonToggledEvent (self, obj = None, data = None):
        """
            When click on favorite button, make currency favorite or remove it
            from favorites
        """
        currency = self.__mainWindow.getActualCurrency()
        currency.favorite = not currency.favorite

        if currency.favorite is True:
            self.__favoriteButtonImage.set_from_icon_name('starred-symbolic', 1)
            self.__mainWindow.currencySwitcher.actualRow.favoriteImageRevealer.set_reveal_child(True)
        else:
            self.__favoriteButtonImage.set_from_icon_name('non-starred-symbolic', 1)
            self.__mainWindow.currencySwitcher.actualRow.favoriteImageRevealer.set_reveal_child(False)

        self.__mainWindow.currencySwitcher.invalidate_sort()

    def __graphSwitcherButtonToggledEvent (self, obj, data = None):
        """
            Change the graph period (day / month / year / all time) when click
            on button
        """
        if obj.get_active() is False and self.__actualGraphTime == obj.name:
            with obj.handler_block(obj.handlerID):
                obj.set_active(True)
        else:
            for child in self.__graphSwitcher.get_children():
                if child is not obj and child.get_active() is True:
                    with child.handler_block(child.handlerID):
                        child.set_active(False)

        self.__actualGraphTime = obj.name
        currency = self.__mainWindow.getActualCurrency()
        quoteCurrency = self.__mainWindow.getActualQuoteCurrency()
        nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quoteCurrency.priceUSD)

        self.__graph.setGraph(getattr(currency, obj.name + 'GraphDataUSD'), obj.name, quoteCurrency, nbDigitsAfterDecimalPoint)
