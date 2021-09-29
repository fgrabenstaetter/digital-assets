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
from gi.repository import Gtk
from dassets.sys import tools
from dassets.ui.graph import Graph
from dassets.env import *
import datetime

class CurrencyView (Gtk.Box):

    def __init__ (self, mainWindow):
        """
            Init CurrencyView
        """
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)
        self.__mainWindow = mainWindow
        self.__actualGraphTime = 'day'
        self.__builder = self.__mainWindow.builder
        self.__uiObj = self.__builder.get_object('currencyMain')
        self.__graph = Graph(self.__builder)
        self.__discoverUiObjs()
        self.__initUi()
        self.reload()

    def reload (self, otherCrypto = False):
        """
            Reload widgets values according to the actual currency and the
            actual quote currency
        """
        currency = self.__mainWindow.getActualCurrency()
        quote = self.__mainWindow.getActualQuote()

        if otherCrypto is True:
            pass

        self.__mainWindow.changeTitle(currency.name + ' (' + currency.symbol + ')')

        self.__currencyLogoUiObj.set_from_resource(PRGM_PATH + 'img/' + currency.symbol + '.svg')
        self.__currencyNameUiObj.set_text(currency.name)
        self.__currencySymbolUiObj.set_text(currency.symbol)

        # bottom actions
        self.__currencyWebsiteUiObj.set_uri(currency.websiteURL)
        self.__favoriteIsReady = False # to not change currency.favorite when activate
        self.__currencyFavoriteButtonUiObj.set_active(currency.favorite)
        self.__favoriteIsReady = True
        self.__favoriteChanged()

        self.__currencyPriceQuoteUiObj.set_text(quote.symbol)

        # rank
        if currency.rank is None:
            rankStr = '# ?'
        else:
            rankStr = '# ' + str(currency.rank)
        self.__currencyRankUiObj.set_text(rankStr)


        # price
        if not currency.priceUSD or not quote.priceUSD:
            self.__currencyPriceUiObj.set_text('. . .')
            self.__currencyPriceIndicatorUiObj.set_text('')
        else:
            if self.__currencyInfosRevealerUiObj.get_child_revealed() is False:
                self.__currencyInfosRevealerUiObj.set_reveal_child(True)

            nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quote.priceUSD)
            priceRounded = round(currency.priceUSD / quote.priceUSD, nbDigitsAfterDecimalPoint)
            priceText = tools.beautifyNumber(priceRounded)
            self.__currencyPriceUiObj.set_text(priceText)

            # price indicator
            if currency.lastPriceUSD is not None and quote.lastPriceUSD is not None:
                actualPrice = currency.priceUSD / quote.priceUSD
                lastPrice = currency.lastPriceUSD / quote.lastPriceUSD

                if actualPrice < lastPrice:
                    self.__currencyPriceIndicatorUiObj.set_text('↓')
                    self.__currencyPriceIndicatorUiObj.set_css_classes(['red'])
                elif actualPrice > lastPrice:
                    self.__currencyPriceIndicatorUiObj.set_text('↑')
                    self.__currencyPriceIndicatorUiObj.set_css_classes(['green'])
                else:
                    self.__currencyPriceIndicatorUiObj.set_text('')
            else:
                self.__currencyPriceIndicatorUiObj.set_text('')

        # day price change

        # change value
        if currency.lastDayPriceUSD is None or quote.lastDayPriceUSD is None or currency.priceUSD is None or quote.priceUSD is None:
            self.__currencyPriceChangeValueUiObj.set_text('')
        else:
            nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quote.priceUSD)
            dayPriceChangeValue = round(currency.priceUSD / quote.priceUSD - currency.lastDayPriceUSD / quote.lastDayPriceUSD, nbDigitsAfterDecimalPoint)
            dayPriceChangeValueText = tools.beautifyNumber(abs(dayPriceChangeValue))
            self.__currencyPriceChangeValueUiObj.set_text('(' + dayPriceChangeValueText + ')')
        # change percentage
        self.__setChangePercentage(self.__currencyPriceChangePercentageUiObj, currency.priceUSD, currency.lastDayPriceUSD, quote.priceUSD, quote.lastDayPriceUSD)

        # marketcap
        self.__currencyMarketcapQuoteUiObj.set_text(quote.symbol)
        if currency.marketcapUSD is None or quote.priceUSD is None:
            self.__currencyMarketcapValueUiObj.set_text(_('Undefined'))
        else:
            marketcapRounded = round(currency.marketcapUSD / quote.priceUSD)
            self.__currencyMarketcapValueUiObj.set_text(tools.beautifyNumber(marketcapRounded))

        # change
        self.__setChangePercentage(self.__currencyMarketcapChangeUiObj, currency.marketcapUSD, currency.lastDayMarketcapUSD, quote.marketcapUSD, quote.lastDayMarketcapUSD)

        # day volume
        self.__currencyVolumeQuoteUiObj.set_text(quote.symbol)
        if currency.dayVolumeUSD is None or quote.priceUSD is None:
            self.__currencyVolumeValueUiObj.set_text(_('Undefined'))
        else:
            volumeRounded = round(currency.dayVolumeUSD / quote.priceUSD)
            self.__currencyVolumeValueUiObj.set_text(tools.beautifyNumber(volumeRounded))

        # change

        if currency == quote:
            # workaround to fix the 0% change if same currency/quote
            quoteVal = 1
            quoteLastVal = 1
        else:
            quoteVal = quote.dayVolumeUSD
            quoteLastVal = quote.lastDayVolumeUSD

        self.__setChangePercentage(self.__currencyVolumeChangeUiObj, currency.dayVolumeUSD, currency.lastDayVolumeUSD, quoteVal, quoteLastVal)

        # supply

        # circulating supply
        self.__currencySupplyCirculatingQuoteUiObj.set_text(currency.symbol)
        if currency.circulatingSupply is None:
            self.__currencySupplyCirculatingUiObj.set_text(_('Undefined'))
        else:
            circulatingSupplyRounded = round(currency.circulatingSupply)
            self.__currencySupplyCirculatingUiObj.set_text(tools.beautifyNumber(circulatingSupplyRounded))

        # max supply
        self.__currencySupplyMaxQuoteUiObj.set_text(currency.symbol)
        if currency.maxSupply is None:
            self.__currencySupplyMaxUiObj.set_text(_('Undefined'))
        else:
            maxSupplyRounded = round(currency.maxSupply)
            self.__currencySupplyMaxUiObj.set_text(tools.beautifyNumber(maxSupplyRounded))

        # progress bar
        barFraction = 0
        fractionText = _('Unlimited')
        if currency.circulatingSupply is not None and currency.maxSupply is not None:
            barFraction = currency.circulatingSupply / currency.maxSupply
            fractionText = str(round(barFraction * 100, 1)) + ' %'
        self.__currencySupplyBarUiObj.set_fraction(barFraction)
        self.__currencySupplyBarUiObj.set_text(fractionText)

        # ATH

        self.__currencyAthQuoteUiObj.set_text(quote.symbol)
        ath = currency.calculateAth(quote)

        if ath is None or currency.priceUSD is None or currency.athUSD is None:
            if self.__mainWindow.getCurrencyBySymbol('BTC').allCandlesUSD is not None:
                self.__currencyAthValueUiObj.set_text(_('Undefined'))
                self.__currencyAthChangeUiObj.set_text('? %')
        else:
            actualPrice = currency.priceUSD / quote.priceUSD
            athPercentage = round(actualPrice / ath[0] * 100, 1)
            bestDecimalDigitsNb = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quote.priceUSD)
            athPriceText = tools.beautifyNumber(round(ath[0], bestDecimalDigitsNb))

            self.__currencyAthValueUiObj.set_text(athPriceText)
            self.__currencyAthChangeUiObj.set_text(str(athPercentage) + ' %')

            # tooltip
            tooltipStr = ath[1].strftime('%x')
            self.__currencyAthValueUiObj.set_tooltip_text(tooltipStr)

        # candles graph

        # day graph prices is the first loaded
        if currency.dayCandlesUSD is not None and self.__currencyGraphRevealerUiObj.get_child_revealed() is False:
            self.__currencySpinnerUiObj.hide()
            self.__currencyGraphRevealerUiObj.set_reveal_child(True)

        # change graphSwitcher buttons sensitivity if needed
        periodButton = self.__currencyGraphButtonsUiObj.get_first_child()
        while periodButton is not None:
            candles = getattr(currency, periodButton.get_name() + 'CandlesUSD')

            if candles is not None and periodButton.get_sensitive() is False:
                periodButton.set_sensitive(True)
                periodButton.get_first_child().get_first_child().hide()
            elif candles is None and periodButton.get_sensitive() is True:
                periodButton.set_sensitive(False)

            if periodButton.get_name() == self.__actualGraphTime:
                self.__graphReload()

            periodButton = periodButton.get_next_sibling()

    ###########
    # PRIVATE #
    ###########

    def __discoverUiObjs (self):
        """
            Put each UI currency view object with an ID into a variable
        """
        # main infos
        self.__currencySpinnerUiObj = self.__builder.get_object('currencySpinner')
        self.__currencyInfosRevealerUiObj = self.__builder.get_object('currencyInfosRevealer')

        self.__currencyRankUiObj = self.__builder.get_object('currencyRank')
        self.__currencyLogoUiObj = self.__builder.get_object('currencyLogo')
        self.__currencyNameUiObj = self.__builder.get_object('currencyName')
        self.__currencySymbolUiObj = self.__builder.get_object('currencySymbol')

        self.__currencyPriceIndicatorUiObj = self.__builder.get_object('currencyPriceIndicator')
        self.__currencyPriceUiObj = self.__builder.get_object('currencyPrice')
        self.__currencyPriceQuoteUiObj = self.__builder.get_object('currencyPriceQuote')
        self.__currencyPriceChangePercentageUiObj = self.__builder.get_object('currencyPriceChangePercentage')
        self.__currencyPriceChangeValueUiObj = self.__builder.get_object('currencyPriceChangeValue')

        # market infos
        self.__currencyMarketcapTitleUiObj = self.__builder.get_object('currencyMarketcapTitle')
        self.__currencyMarketcapValueUiObj = self.__builder.get_object('currencyMarketcapValue')
        self.__currencyMarketcapQuoteUiObj = self.__builder.get_object('currencyMarketcapQuote')
        self.__currencyMarketcapChangeUiObj = self.__builder.get_object('currencyMarketcapChange')

        self.__currencyVolumeTitleUiObj = self.__builder.get_object('currencyVolumeTitle')
        self.__currencyVolumeValueUiObj = self.__builder.get_object('currencyVolumeValue')
        self.__currencyVolumeQuoteUiObj = self.__builder.get_object('currencyVolumeQuote')
        self.__currencyVolumeChangeUiObj = self.__builder.get_object('currencyVolumeChange')

        self.__currencySupplyCirculatingUiObj = self.__builder.get_object('currencySupplyCirculating')
        self.__currencySupplyCirculatingQuoteUiObj = self.__builder.get_object('currencySupplyCirculatingQuote')
        self.__currencySupplyMaxUiObj = self.__builder.get_object('currencySupplyMax')
        self.__currencySupplyMaxQuoteUiObj = self.__builder.get_object('currencySupplyMaxQuote')
        self.__currencySupplyBarUiObj = self.__builder.get_object('currencySupplyBar')

        self.__currencyAthValueUiObj = self.__builder.get_object('currencyAthValue')
        self.__currencyAthQuoteUiObj = self.__builder.get_object('currencyAthQuote')
        self.__currencyAthChangeUiObj = self.__builder.get_object('currencyAthChange')

        # graph
        self.__currencyGraphRevealerUiObj = self.__builder.get_object('currencyGraphRevealer')
        self.__currencyGraphButtonsUiObj = self.__builder.get_object('currencyGraphButtons')
        self.__currencyGraphDrawingAreaUiObj = self.__builder.get_object('currencyGraphDrawingArea')

        # actions
        self.__currencyWebsiteUiObj = self.__builder.get_object('currencyWebsite')
        self.__currencyFavoriteButtonUiObj = self.__builder.get_object('currencyFavoriteButton')
        self.__currencyFavoriteImageUiObj = self.__builder.get_object('currencyFavoriteImage')

    def __initUi (self):
        """
            Connect widgets with signal and other inits
        """
        # period buttons
        periodButton = self.__currencyGraphButtonsUiObj.get_first_child()
        while periodButton is not None:
            periodButton.connect('toggled', self.__graphSwitcherButtonToggledEvent)
            periodButton = periodButton.get_next_sibling()

        # favorite button
        self.__currencyFavoriteButtonUiObj.connect('toggled', self.__favoriteButtonToggledEvent)

    def __favoriteChanged (self):
        """
            Change favorite icon in view and switcher
        """
        currency = self.__mainWindow.getActualCurrency()
        if currency.favorite is True:
            self.__currencyFavoriteImageUiObj.set_from_icon_name('starred-symbolic')
            self.__mainWindow.currencySwitcher.setCurrentFavorite(True)
        else:
            self.__currencyFavoriteImageUiObj.set_from_icon_name('non-starred-symbolic')
            self.__mainWindow.currencySwitcher.setCurrentFavorite(False)

    def __favoriteButtonToggledEvent (self, obj = None, data = None):
        """
            When click on favorite button, make currency favorite or remove it
            from favorites
        """
        if not self.__favoriteIsReady:
            return

        currency = self.__mainWindow.getActualCurrency()
        currency.favorite = not currency.favorite
        self.__favoriteChanged()
        self.__mainWindow.currencySwitcher.sort()

    def __graphSwitcherButtonToggledEvent (self, obj, data = None):
        """
            Change the graph period (day / month / year / all) when click
            on button
        """
        if obj.get_active() is False or self.__actualGraphTime == obj.get_name():
            return
        self.__actualGraphTime = obj.get_name()
        self.__graphReload()

    def __graphReload (self):
        """
            Reload graph data with actualGraphTime
        """
        currency = self.__mainWindow.getActualCurrency()
        quote = self.__mainWindow.getActualQuote()
        self.__graph.setGraph(currency, quote, self.__actualGraphTime)

    def __setChangePercentage (self, uiObj, currencyVal, currencyLastVal, quoteVal, quoteLastVal):
        if currencyVal is None or currencyLastVal is None or quoteVal is None or quoteLastVal is None:
            uiObj.set_text('? %')
            uiObj.set_css_classes([])
        else:
            val = currencyVal / quoteVal
            lastVal = currencyLastVal / quoteLastVal
            change = round(val / lastVal * 100 - 100, 1)

            if change > 0:
                changeCss = 'green'
                changeStr = '+ ' + str(abs(change)) + ' %'
            elif change < 0:
                changeCss = 'red'
                changeStr = '- ' + str(abs(change)) + ' %'
            else:
                changeCss = 'grey'
                changeStr = '0 %'

            uiObj.set_css_classes([changeCss])
            uiObj.set_text(changeStr)
