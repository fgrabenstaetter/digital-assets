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

class CurrencyView (Gtk.Box):

    def __init__ (self, mainWindow):
        """
            Init CurrencyView
        """
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL,
                         expand = True, border_width = 40)
        self.__mainWindow = mainWindow
        self.__actualCurrencySymbol = None
        self.__actualGraphTime = None

        self.__spinner1 = Gtk.Spinner()
        self.__spinner1.set_size_request(200, 200)
        self.__spinner1.start()
        self.add(self.__spinner1)

        self.show_all()

    def reload (self, animate = False):
        """
            Reload widgets values according to the actual currency and the
            actual base currency
        """
        currency = self.__mainWindow.getActualCurrency()
        baseCurrency = self.__mainWindow.getActualBaseCurrency()

        if currency.priceUSD is None or baseCurrency.priceUSD is None:
            return

        if self.__spinner1 is not None:
            self.__create()
        elif animate is True:
            self.__revealer.destroy()
            self.__revealer = None
            self.__create()

        # update window title
        self.__mainWindow.headerBar.set_title(currency.name \
                                            + ' (' + currency.symbol + ')')

        # top (header)
        self.__actualCurrencySymbol = currency.symbol
        pixbuf = GdkPixbuf.Pixbuf().new_from_resource_at_scale(
                PRGM_PATH + 'img/' + currency.symbol + '.svg', 100, 100, True)
        self.__image.set_from_pixbuf(pixbuf)

        # name and symbol
        self.__nameLabel.set_label(currency.name)
        self.__symbolLabel.set_label(currency.symbol)

        # price
        nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(
                                            currency.priceUSD, baseCurrency.priceUSD)
        priceRounded = round(currency.priceUSD / baseCurrency.priceUSD,
                             nbDigitsAfterDecimalPoint)

        self.__priceLabel.set_label(tools.beautifyNumber(priceRounded))
        self.__baseCurrencySymbolLabel.set_label(baseCurrency.symbol)

        # actions box
        self.__websiteButton.set_uri(currency.websiteURL)

        if currency.favorite is True:
            with self.__favoriteButton.handler_block(
                                                self.__favoriteButton.handlerID):
                self.__favoriteButton.set_active(True)
                self.__favoriteButtonImage.set_from_icon_name(
                                                        'starred-symbolic', 1)

        # only when all data has been loaded into currency
        if currency.dayVolumeUSD is not None:
            if self.__infosBoxRevealer.get_child_revealed() is False:
                self.__infosBoxRevealer.set_reveal_child(True)

            if self.__spinner2 is not None \
                    and self.__spinner2.get_visible() is True:
                self.__spinner2.set_size_request(60, 60)

            # general informations (day variation, day volume)

            # last day price
            if currency.lastDayPriceUSD is None \
                    or baseCurrency.lastDayPriceUSD is None:
                self.__dayPriceChangeLabel.set_label(_('Undefined'))
            else:
                dayPriceChange = currency.lastDayPriceUSD \
                               / baseCurrency.lastDayPriceUSD
                dayPriceChange = round(((currency.priceUSD / baseCurrency.priceUSD) \
                                        / dayPriceChange) * 100 - 100, 1)
                dayPriceChangeStr = ''
                if dayPriceChange >= 0:
                    self.__dayPriceChangeLabel.set_name('priceGreen')
                    dayPriceChangeStr = '+ ' + str(abs(dayPriceChange)) + ' %'
                else:
                    self.__dayPriceChangeLabel.set_name('priceRed')
                    dayPriceChangeStr = '- ' + str(abs(dayPriceChange)) + ' %'
                self.__dayPriceChangeLabel.set_label(dayPriceChangeStr)

            # marketcap
            if currency.marketCapUSD is None:
                self.__marketCapLabel.set_label(_('Undefined'))
            else:
                marketCapRounded = round(currency.marketCapUSD \
                                       / baseCurrency.priceUSD)
                self.__marketCapLabel.set_label(tools.beautifyNumber(
                                                            marketCapRounded))
                self.__marketCapBaseCurrencySymbolLabel.set_label(
                                                            baseCurrency.symbol)

            # day volume
            if currency.dayVolumeUSD is None:
                self.__volumeLabel.set_label(_('Undefined'))
            else:
                volumeRounded = round(currency.dayVolumeUSD / baseCurrency.priceUSD)
                self.__volumeLabel.set_label(tools.beautifyNumber(volumeRounded))
                self.__volumeBaseCurrencySymbolLabel.set_label(
                                                            baseCurrency.symbol)

            # ATH (actual % relative to ATH)
            if baseCurrency.symbol == 'USD':
                if self.__athSpinner.get_visible() is True:
                    self.__athSpinner.set_visible(False)
                    self.__athLabel.set_visible(True)
                if currency.athUSD is None:
                    self.__athLabel.set_label(_('Undefined'))
                else:
                    athPercentage = round((currency.priceUSD / currency.athUSD) \
                                          * 100, 1)
                    self.__athLabel.set_label(str(athPercentage) + ' %')
            elif currency.alltimeGraphDataUSD is not None \
                    and baseCurrency.alltimeGraphDataUSD is not None:
                if self.__athSpinner.get_visible() is True:
                    self.__athSpinner.set_visible(False)
                    self.__athLabel.set_visible(True)
                athPercentage = round(currency.calculateAth(baseCurrency) \
                                * 100, 1)
                self.__athLabel.set_label(str(athPercentage) + ' %')
            else:
                self.__athSpinner.set_visible(True)
                self.__athLabel.set_visible(False)

            # rank
            if currency.rank is None:
                self.__rankLabel.set_text(_('Undefined'))
            else:
                self.__rankLabel.set_text(str(currency.rank))

            # circulating supply
            if currency.circulatingSupply is None:
                self.__circulatingSupplyLabel.set_label(_('Undefined'))
            else:
                circulatingSupplyRounded = round(currency.circulatingSupply)
                self.__circulatingSupplyLabel.set_label(tools.beautifyNumber(
                                                    circulatingSupplyRounded))
                self.__circulatingSupplyBaseCurrencySymbolLabel.set_label(
                                                                currency.symbol)

            # max supply
            if currency.maxSupply is None:
                self.__maxSupplyLabel.set_label(_('Undefined'))
            else:
                maxSupplyRounded = tools.beautifyNumber(round(
                                                            currency.maxSupply))
                self.__maxSupplyLabel.set_label(str(maxSupplyRounded))
                self.__maxSupplyBaseCurrencySymbolLabel.set_label(currency.symbol)

            # day graph prices is the first loaded
            if currency.dayGraphDataUSD is not None:
                if self.__spinner2 is not None:
                    self.__spinner2.destroy()
                    self.__spinner2 = None

                if self.__graphBoxRevealer.get_child_revealed() is False:
                    self.__graphBoxRevealer.set_reveal_child(True)

                # change graphSwitcher buttons sensitivity if needed
                for child in self.__graphSwitcher.get_children():
                    childGraphData = getattr(currency,
                                             child.name + 'GraphDataUSD')

                    if child.get_sensitive() is False \
                            and childGraphData is not None:
                        child.set_sensitive(True)
                        child.spinner.destroy()
                    elif child.get_sensitive() is True \
                            and childGraphData is None:
                        child.set_sensitive(False)

                # graph set value
                if self.__actualGraphTime is None \
                        and len(self.__graphSwitcher.get_children()) > 0:
                    self.__graphSwitcher.get_children()[0].set_active(True)
                else:
                    for child in self.__graphSwitcher.get_children():
                        if child.name == self.__actualGraphTime:
                            if child.get_active() is True:
                                # re-activate
                                child.set_active(False)
                            child.set_active(True)
                            break
        self.queue_draw()
        if self.__revealer is not None:
            self.__revealer.set_reveal_child(True)

    ###########
    # PRIVATE #
    ###########

    def __create (self):
        """
            Create widgets
        """
        if self.__spinner1 is not None:
            self.__spinner1.destroy()
            self.__spinner1 = None

        # widgets
        self.__image = Gtk.Image()
        self.__nameLabel = Gtk.Label(name = 'currencyName', xalign = 0)
        self.__symbolLabel = Gtk.Label(name = 'currencySymbol', xalign = 0)
        self.__priceLabel = Gtk.Label(name = 'currencyPrice')
        self.__baseCurrencySymbolLabel = Gtk.Label(name = 'currencyPrice')

        self.__dayPriceChangeNameLabel = Gtk.Label(_('Change'),
                                                 name = 'infoTitle')
        self.__dayPriceChangeLabel = Gtk.Label()

        self.__marketCapNameLabel = Gtk.Label(_('Markep Cap'), name = 'infoTitle')
        self.__marketCapLabel = Gtk.Label()
        self.__marketCapBaseCurrencySymbolLabel = Gtk.Label()

        self.__volumeNameLabel = Gtk.Label(_('Volume'), name = 'infoTitle')
        self.__volumeLabel = Gtk.Label()
        self.__volumeBaseCurrencySymbolLabel = Gtk.Label()

        self.__athNameLabel = Gtk.Label('ATH', name = 'infoTitle')
        self.__athLabel = Gtk.Label(visible = None)

        self.__rankNameLabel = Gtk.Label(_('Rank'), name = 'infoTitle')
        self.__rankLabel = Gtk.Label()

        self.__circulatingSupplyNameLabel = Gtk.Label(_('Circulating Supply'),
                                                    name = 'infoTitle')
        self.__circulatingSupplyLabel = Gtk.Label()
        self.__circulatingSupplyBaseCurrencySymbolLabel = Gtk.Label()

        self.__maxSupplyNameLabel = Gtk.Label(_('Max Supply'), name = 'infoTitle')
        self.__maxSupplyLabel = Gtk.Label()
        self.__maxSupplyBaseCurrencySymbolLabel = Gtk.Label()

        # graph
        self.__graph = Graph()

        # website link and favorite button
        self.__websiteButton = Gtk.LinkButton(label = _('Website'),
                                            name = 'linkButton')

        self.__favoriteButtonImage = Gtk.Image().new_from_icon_name(
                                                    'non-starred-symbolic', 1)
        self.__favoriteButton = Gtk.ToggleButton(valign = Gtk.Align.CENTER)
        self.__favoriteButton.add(self.__favoriteButtonImage)
        self.__favoriteButton.handlerID = self.__favoriteButton.connect(
                                                'toggled',
                                                self.__favoriteButtonToggledEvent)

        # spinners
        self.__spinner2 = Gtk.Spinner()
        self.__spinner2.set_size_request(100, 100)
        self.__spinner2.start()

        self.__athSpinner = Gtk.Spinner()
        self.__athSpinner.start()

        # containers

        # top box
        titleRightBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                                valign = Gtk.Align.CENTER,
                                spacing = 10)
        titleRightBox.add(self.__nameLabel)
        titleRightBox.add(self.__symbolLabel)

        titleBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 40)
        titleBox.add(self.__image)
        titleBox.add(titleRightBox)

        priceBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 10)
        priceBox.add(self.__priceLabel)
        priceBox.add(self.__baseCurrencySymbolLabel)

        topBoxMain = Gtk.Box(halign = Gtk.Align.CENTER,
                             spacing = 100,
                             border_width = 20)
        topBoxMain.add(titleBox);
        topBoxMain.add(priceBox)

        topBox = Gtk.Button()
        topBox.add(topBoxMain)

        # general informations box
        dayPriceChangeBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                                    spacing = 10,
                                    halign = Gtk.Align.CENTER)
        dayPriceChangeBox.add(self.__dayPriceChangeNameLabel)
        dayPriceChangeBox.add(self.__dayPriceChangeLabel)

        marketCapValueBox = Gtk.Box(spacing = 10, halign = Gtk.Align.CENTER)
        marketCapValueBox.add(self.__marketCapLabel)
        marketCapValueBox.add(self.__marketCapBaseCurrencySymbolLabel)
        marketCapBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                               spacing = 10)
        marketCapBox.add(self.__marketCapNameLabel)
        marketCapBox.add(marketCapValueBox)

        volumeValueBox = Gtk.Box(spacing = 10, halign = Gtk.Align.CENTER)
        volumeValueBox.add(self.__volumeLabel)
        volumeValueBox.add(self.__volumeBaseCurrencySymbolLabel)
        volumeBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                            spacing = 10)
        volumeBox.add(self.__volumeNameLabel)
        volumeBox.add(volumeValueBox)

        athBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                         spacing = 10,
                         halign = Gtk.Align.CENTER)
        athBox.add(self.__athNameLabel)
        athBox.add(self.__athLabel)
        athBox.add(self.__athSpinner)

        generalInfosBox = Gtk.Box(halign = Gtk.Align.CENTER, spacing = 60)
        generalInfosBox.add(dayPriceChangeBox)
        generalInfosBox.add(marketCapBox)
        generalInfosBox.add(volumeBox)
        generalInfosBox.add(athBox)

        # supply infos box (and rank)
        rankBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                          spacing = 10,
                          halign = Gtk.Align.CENTER)
        rankBox.add(self.__rankNameLabel)
        rankBox.add(self.__rankLabel)

        circulatingSupplyValueBox = Gtk.Box(spacing = 10,
                                            halign = Gtk.Align.CENTER)
        circulatingSupplyValueBox.add(self.__circulatingSupplyLabel)
        circulatingSupplyValueBox.add(
                                self.__circulatingSupplyBaseCurrencySymbolLabel)
        circulatingSupplyBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                                       spacing = 10)
        circulatingSupplyBox.add(self.__circulatingSupplyNameLabel)
        circulatingSupplyBox.add(circulatingSupplyValueBox)

        maxSupplyValueBox = Gtk.Box(spacing = 10, halign = Gtk.Align.CENTER)
        maxSupplyValueBox.add(self.__maxSupplyLabel)
        maxSupplyValueBox.add(self.__maxSupplyBaseCurrencySymbolLabel)
        maxSupplyBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                               spacing = 10)
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
            button.handlerID = button.connect('toggled',
                                        self.__graphSwitcherButtonToggledEvent)

            buttonBox = Gtk.Box(spacing = 8, border_width = 4,
                                halign = Gtk.Align.CENTER)
            buttonLabel = Gtk.Label(str)
            buttonSpinner = Gtk.Spinner(active = True)
            button.spinner = buttonSpinner

            buttonBox.add(buttonLabel)
            buttonBox.add(buttonSpinner)
            button.add(buttonBox)

            button.set_size_request(100, -1)
            self.__graphSwitcher.add(button)

        graphBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                           halign = Gtk.Align.CENTER,
                           spacing = 30,
                           name = 'graphBox')
        graphBox.add(self.__graphSwitcher)
        graphBox.add(self.__graph)

        # main containers
        infosBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                           halign = Gtk.Align.CENTER,
                           name = 'infosBox')
        infosBox.add(generalInfosBox)
        infosBox.add(supplyInfosBox)

        self.__infosBoxRevealer = Gtk.Revealer()
        self.__infosBoxRevealer.add(infosBox)
        self.__graphBoxRevealer = Gtk.Revealer()
        self.__graphBoxRevealer.add(graphBox)

        bottomBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                            halign = Gtk.Align.CENTER,
                            spacing = 30)
        bottomBox.add(self.__infosBoxRevealer)
        bottomBox.add(self.__spinner2)
        bottomBox.add(self.__graphBoxRevealer)

        mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                          halign = Gtk.Align.CENTER,
                          spacing = 40,
                          border_width = 10,
                          name = 'mainBox')
        mainBox.add(topBox)
        mainBox.add(bottomBox)
        mainBox.add(actionsBox)

        self.__revealer = Gtk.Revealer(
                        transition_type = Gtk.RevealerTransitionType.CROSSFADE)
        self.__revealer.add(mainBox)

        self.add(self.__revealer)
        self.show_all()

    def __favoriteButtonToggledEvent (self, obj = None, data = None):
        """
            When click on favorite button, make currency favorite or remove it
            from favorites
        """
        currency = self.__mainWindow.currencies[self.__actualCurrencySymbol]
        currency.favorite = not currency.favorite

        if currency.favorite is True:
            self.__favoriteButtonImage.set_from_icon_name('starred-symbolic', 1)
            self.__mainWindow.currencySwitcher.actualRow.favoriteImageRevealer \
                                                        .set_reveal_child(True)
        else:
            self.__favoriteButtonImage.set_from_icon_name(
                                                    'non-starred-symbolic', 1)
            self.__mainWindow.currencySwitcher.actualRow.favoriteImageRevealer \
                                                        .set_reveal_child(False)

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
        currency = self.__mainWindow.currencies[self.__actualCurrencySymbol]
        baseCurrency = self.__mainWindow.getActualBaseCurrency()
        nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(
                                            currency.priceUSD, baseCurrency.priceUSD)

        self.__graph.setGraph(getattr(currency, obj.name + 'GraphDataUSD'),
                            obj.name,
                            baseCurrency,
                            nbDigitsAfterDecimalPoint)
        self.__graph.redraw()
