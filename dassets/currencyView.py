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
from dassets import tools
from dassets.graph import Graph
from dassets.env import *

class CurrencyView ():

    def __init__ (self, app):
        self.__app = app
        self.__app.addCssProvider('currencyView')
        self.__builder = self.__app.newBuilder('currencyView')
        self.__node = self.__builder.get_object('currencyView')
        self.__app.builder.get_object('currencyViewbox').set_child(self.__node)

        self.__actualGraphTime = 'day'
        self.__graph = Graph(self.__builder)

        self.__discoverNodes()
        self.__initUi()
        self.reload()

    def reload (self):
        """
            Reload widgets values according to the actual currency and the
            actual quote currency
        """
        currency = self.__app.getActualCurrency()
        quote = self.__app.getActualQuote()

        self.__app.changeTitle(currency.name + ' (' + currency.symbol + ')')

        self.__currencyLogoNode.set_from_resource(IMG_RPATH + currency.symbol + '.png')
        self.__currencyNameNode.set_text(currency.name)
        self.__currencySymbolNode.set_text(currency.symbol)

        # bottom actions
        self.__currencyWebsiteNode.set_uri(currency.websiteURL)
        self.__favoriteIsReady = False # to not change currency.favorite when activate
        self.__currencyFavoriteButtonNode.set_active(currency.favorite)
        self.__favoriteIsReady = True
        self.__favoriteChanged()

        self.__currencyPriceQuoteNode.set_text(quote.symbol)

        # rank
        if currency.rank is None:
            rankStr = '# ?'
        else:
            rankStr = '# ' + str(currency.rank)
        self.__currencyRankNode.set_text(rankStr)

        # price
        if not currency.priceUSD or not quote.priceUSD:
            self.__currencyPriceNode.set_text('. . .')
            self.__currencyPriceIndicatorNode.set_text('')
        else:
            if self.__currencyInfosRevealerNode.get_child_revealed() is False:
                self.__currencyInfosRevealerNode.set_reveal_child(True)

            nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quote.priceUSD)
            priceRounded = round(currency.priceUSD / quote.priceUSD, nbDigitsAfterDecimalPoint)
            priceText = tools.beautifyNumber(priceRounded)
            self.__currencyPriceNode.set_text(priceText)

            # price indicator
            if not currency.lastPriceUSD or not quote.lastPriceUSD:
                self.__currencyPriceIndicatorNode.set_text('')
            else:
                actualPrice = currency.priceUSD / quote.priceUSD
                lastPrice = currency.lastPriceUSD / quote.lastPriceUSD

                if actualPrice < lastPrice:
                    self.__currencyPriceIndicatorNode.set_text('↓')
                    self.__currencyPriceIndicatorNode.set_css_classes(['red'])
                elif actualPrice > lastPrice:
                    self.__currencyPriceIndicatorNode.set_text('↑')
                    self.__currencyPriceIndicatorNode.set_css_classes(['green'])
                else:
                    self.__currencyPriceIndicatorNode.set_text('')

        # day price change value
        if not currency.lastDayPriceUSD or not quote.lastDayPriceUSD or not currency.priceUSD or not quote.priceUSD:
            self.__currencyPriceChangeValueNode.set_text('')
        else:
            nbDigitsAfterDecimalPoint = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quote.priceUSD)
            dayPriceChangeValue = round(currency.priceUSD / quote.priceUSD - currency.lastDayPriceUSD / quote.lastDayPriceUSD, nbDigitsAfterDecimalPoint)
            dayPriceChangeValueText = tools.beautifyNumber(abs(dayPriceChangeValue))
            self.__currencyPriceChangeValueNode.set_text('(' + dayPriceChangeValueText + ')')

        # day price change percentage
        self.__setChangePercentage(self.__currencyPriceChangePercentageNode, currency.priceUSD, currency.lastDayPriceUSD, quote.priceUSD, quote.lastDayPriceUSD)

        # marketcap
        self.__currencyMarketcapQuoteNode.set_text(quote.symbol)
        if not currency.marketcapUSD or not quote.priceUSD:
            self.__currencyMarketcapValueNode.set_text(_('Undefined'))
        else:
            marketcapRounded = round(currency.marketcapUSD / quote.priceUSD)
            self.__currencyMarketcapValueNode.set_text(tools.beautifyNumber(marketcapRounded))

        # change
        self.__setChangePercentage(self.__currencyMarketcapChangeNode, currency.marketcapUSD, currency.lastDayMarketcapUSD, quote.marketcapUSD, quote.lastDayMarketcapUSD)

        # day volume value
        self.__currencyVolumeQuoteNode.set_text(quote.symbol)
        if not currency.dayVolumeUSD or not quote.priceUSD:
            self.__currencyVolumeValueNode.set_text(_('Undefined'))
        else:
            volumeRounded = round(currency.dayVolumeUSD / quote.priceUSD)
            self.__currencyVolumeValueNode.set_text(tools.beautifyNumber(volumeRounded))

        # day volume change
        if currency is quote:
            # fix the 0% change if same currency/quote
            quoteVal = 1
            quoteLastVal = 1
        else:
            quoteVal = quote.dayVolumeUSD
            quoteLastVal = quote.lastDayVolumeUSD

        self.__setChangePercentage(self.__currencyVolumeChangeNode, currency.dayVolumeUSD, currency.lastDayVolumeUSD, quoteVal, quoteLastVal)

        # circulating supply
        self.__currencySupplyCirculatingQuoteNode.set_text(currency.symbol)
        if not currency.circulatingSupply:
            self.__currencySupplyCirculatingNode.set_text(_('Undefined'))
        else:
            circulatingSupplyRounded = round(currency.circulatingSupply)
            self.__currencySupplyCirculatingNode.set_text(tools.beautifyNumber(circulatingSupplyRounded))

        # max supply
        self.__currencySupplyMaxQuoteNode.set_text(currency.symbol)
        if not currency.maxSupply:
            self.__currencySupplyMaxNode.set_text(_('Undefined'))
        else:
            maxSupplyRounded = round(currency.maxSupply)
            self.__currencySupplyMaxNode.set_text(tools.beautifyNumber(maxSupplyRounded))

        # supply progress bar
        if not currency.circulatingSupply or not currency.maxSupply:
            barFraction = 0
            fractionText = _('Unlimited')
        else:
            barFraction = currency.circulatingSupply / currency.maxSupply
            fractionText = str(round(barFraction * 100, 1)) + ' %'

        self.__currencySupplyBarNode.set_fraction(barFraction)
        self.__currencySupplyBarNode.set_text(fractionText)

        # ATH
        self.__currencyAthQuoteNode.set_text(quote.symbol)
        ath = currency.calculateAth(quote)

        if not ath or not currency.priceUSD or not currency.athUSD:
            if self.__app.currencies['BTC'].allCandlesUSD:
                # all candles loaded but ATH is None
                self.__currencyAthValueNode.set_text(_('Undefined'))
                self.__currencyAthChangeNode.set_text('? %')
            else: # candles not loaded for now
                self.__currencyAthValueNode.set_text('. . .')
                self.__currencyAthChangeNode.set_text('')
        else:
            actualPrice = currency.priceUSD / quote.priceUSD
            athPercentage = round(actualPrice / ath[0] * 100, 1)
            bestDecimalDigitsNb = tools.bestDigitsNumberAfterDecimalPoint(currency.priceUSD, quote.priceUSD)
            athPriceText = tools.beautifyNumber(round(ath[0], bestDecimalDigitsNb))

            self.__currencyAthValueNode.set_text(athPriceText)
            self.__currencyAthChangeNode.set_text(str(athPercentage) + ' %')

            # tooltip
            tooltipStr = ath[1].strftime('%x')
            self.__currencyAthValueNode.set_tooltip_text(tooltipStr)

        # candles graph

        # day graph prices is the first loaded
        if currency.dayCandlesUSD and not self.__currencyGraphRevealerNode.get_child_revealed():
            self.__currencySpinnerNode.hide()
            self.__currencyGraphRevealerNode.set_reveal_child(True)

        # change graphSwitcher buttons sensitivity if needed
        periodButton = self.__currencyGraphButtonsNode.get_first_child()

        while periodButton:
            candles = getattr(currency, periodButton.get_name() + 'CandlesUSD')
            if candles and not periodButton.get_sensitive():
                periodButton.set_sensitive(True)
                periodButton.get_first_child().get_first_child().hide() # hide spinner
            elif not candles and periodButton.get_sensitive():
                periodButton.set_sensitive(False)
            periodButton = periodButton.get_next_sibling()

        self.__graphReload()

    ###########
    # PRIVATE #
    ###########

    def __discoverNodes (self):
        # main infos
        self.__currencySpinnerNode = self.__builder.get_object('currencySpinner')
        self.__currencyInfosRevealerNode = self.__builder.get_object('currencyInfosRevealer')

        self.__currencyRankNode = self.__builder.get_object('currencyRank')
        self.__currencyLogoNode = self.__builder.get_object('currencyLogo')
        self.__currencyNameNode = self.__builder.get_object('currencyName')
        self.__currencySymbolNode = self.__builder.get_object('currencySymbol')

        self.__currencyPriceIndicatorNode = self.__builder.get_object('currencyPriceIndicator')
        self.__currencyPriceNode = self.__builder.get_object('currencyPrice')
        self.__currencyPriceQuoteNode = self.__builder.get_object('currencyPriceQuote')
        self.__currencyPriceChangePercentageNode = self.__builder.get_object('currencyPriceChangePercentage')
        self.__currencyPriceChangeValueNode = self.__builder.get_object('currencyPriceChangeValue')

        # market infos
        self.__currencyMarketcapTitleNode = self.__builder.get_object('currencyMarketcapTitle')
        self.__currencyMarketcapValueNode = self.__builder.get_object('currencyMarketcapValue')
        self.__currencyMarketcapQuoteNode = self.__builder.get_object('currencyMarketcapQuote')
        self.__currencyMarketcapChangeNode = self.__builder.get_object('currencyMarketcapChange')

        self.__currencyVolumeTitleNode = self.__builder.get_object('currencyVolumeTitle')
        self.__currencyVolumeValueNode = self.__builder.get_object('currencyVolumeValue')
        self.__currencyVolumeQuoteNode = self.__builder.get_object('currencyVolumeQuote')
        self.__currencyVolumeChangeNode = self.__builder.get_object('currencyVolumeChange')

        self.__currencySupplyCirculatingNode = self.__builder.get_object('currencySupplyCirculating')
        self.__currencySupplyCirculatingQuoteNode = self.__builder.get_object('currencySupplyCirculatingQuote')
        self.__currencySupplyMaxNode = self.__builder.get_object('currencySupplyMax')
        self.__currencySupplyMaxQuoteNode = self.__builder.get_object('currencySupplyMaxQuote')
        self.__currencySupplyBarNode = self.__builder.get_object('currencySupplyBar')

        self.__currencyAthValueNode = self.__builder.get_object('currencyAthValue')
        self.__currencyAthQuoteNode = self.__builder.get_object('currencyAthQuote')
        self.__currencyAthChangeNode = self.__builder.get_object('currencyAthChange')

        # graph
        self.__currencyGraphRevealerNode = self.__builder.get_object('currencyGraphRevealer')
        self.__currencyGraphButtonsNode = self.__builder.get_object('currencyGraphButtons')
        self.__currencyGraphDrawingAreaNode = self.__builder.get_object('currencyGraphDrawingArea')

        # actions
        self.__currencyWebsiteNode = self.__builder.get_object('currencyWebsite')
        self.__currencyFavoriteButtonNode = self.__builder.get_object('currencyFavoriteButton')
        self.__currencyFavoriteImageNode = self.__builder.get_object('currencyFavoriteImage')

    def __initUi (self):
        # period buttons
        periodButton = self.__currencyGraphButtonsNode.get_first_child()
        while periodButton:
            periodButton.connect('toggled', self.__graphSwitcherButtonToggled)
            periodButton = periodButton.get_next_sibling()

        # favorite button
        self.__currencyFavoriteButtonNode.connect('toggled', self.__favoriteButtonToggled)

    def __favoriteChanged (self):
        """
            Change favorite icon in view and switcher
        """
        currency = self.__app.getActualCurrency()
        if currency.favorite:
            self.__currencyFavoriteImageNode.set_from_icon_name('starred-symbolic')
            self.__app.currencySwitcher.setCurrentFavorite(True)
        else:
            self.__currencyFavoriteImageNode.set_from_icon_name('non-starred-symbolic')
            self.__app.currencySwitcher.setCurrentFavorite(False)

    def __favoriteButtonToggled (self, obj = None, data = None):
        if not self.__favoriteIsReady:
            return

        currency = self.__app.getActualCurrency()
        currency.favorite = not currency.favorite
        self.__favoriteChanged()
        self.__app.currencySwitcher.sort()

    def __graphSwitcherButtonToggled (self, obj, data = None):
        if not obj.get_active() or self.__actualGraphTime == obj.get_name():
            return

        self.__actualGraphTime = obj.get_name()
        self.__graphReload()

    def __graphReload (self):
        currency = self.__app.getActualCurrency()
        quote = self.__app.getActualQuote()
        self.__graph.setGraph(currency, quote, self.__actualGraphTime)

    def __setChangePercentage (self, node, currencyVal, currencyLastVal, quoteVal, quoteLastVal):
        if not currencyVal or not currencyLastVal or not quoteVal or not quoteLastVal:
            node.set_text('? %')
            node.set_css_classes([])
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

            node.set_css_classes([changeCss])
            node.set_text(changeStr)
