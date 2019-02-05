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
from gi.repository import Gtk, Gdk, cairo
from DigitalAssets.data import tools
import gettext, math

class Graph (Gtk.DrawingArea):
    def __init__ (self):
        Gtk.DrawingArea.__init__(self)
        self.set_size_request(600, 250)
        self.connect('draw', self.drawGraph)

        self.textBorderSpace = 10
        self.padding = {'top': 40, 'right': 10, 'bottom': 60, 'left': 80}
        self.graphData = None
        self.graphInfos = {}
        self.baseCurrency = None

        self.show_all()

    def setGraph (self, graphData, graphTime, baseCurrency, priceNbDigitsAfterDecimalPoint):

        # change prices to consider baseCurrency prices
        if (baseCurrency.symbol == 'USD'):
            newGraphData = graphData
        else:
            baseCurrencyGraphData = getattr(baseCurrency, graphTime + 'GraphData')

            if ((len(graphData) == 0) or (len(baseCurrencyGraphData) == 0)):
                newGraphData = None

            else:
                newGraphData = []
                for index1, (dateTime1, price1) in enumerate(graphData):
                    for index2, (dateTime2, price2) in enumerate(baseCurrencyGraphData):
                        if (dateTime1 == dateTime2):
                            newPrice = price1 / price2
                            newGraphData.append((dateTime1, newPrice))

        self.graphData = newGraphData
        self.baseCurrency = baseCurrency
        self.priceNbDigitsAfterDecimalPoint = priceNbDigitsAfterDecimalPoint

        # loading graph infos
        minPrice, maxPrice, nbPrices = None, None, 0

        if (self.graphData is not None):
            for gp in self.graphData:
                if ((minPrice is None) or (gp[1] < minPrice)):
                    minPrice = gp[1]
                if ((maxPrice is None) or (gp[1] > maxPrice)):
                    maxPrice = gp[1]
                nbPrices += 1

        self.graphInfos['minPrice'] = minPrice
        self.graphInfos['maxPrice'] = maxPrice
        self.graphInfos['nbPrices'] = nbPrices
        self.graphInfos['time'] = graphTime

    def redraw (self):
        self.queue_draw()

    def drawGraph (self, obj, ctx):
        # graphData is array of (timestamp, price)

        if (self.graphData is None):
            # no data for this period and this currency / base currency
            ctx.set_source_rgba(0, 0, 0, 0)
            ctx.fill()
            return

        fontColor = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        fontColor.parse('rgba')

        areaWidth = self.get_size_request()[0] - self.padding['left'] - self.padding['right']
        areaHeight = self.get_size_request()[1] - self.padding['top'] - self.padding['bottom']

        ctx.set_line_width(4)
        ctx.set_source_rgb(0.2, 0.7, 0.8)

        lastX, lastY = None, None
        dateTextModulo = math.ceil(self.graphInfos['nbPrices'] / 8)

        i = 0
        for dateTime, price in self.graphData:
            # draw line
            x = (i / self.graphInfos['nbPrices']) * areaWidth + self.padding['left']
            if (self.graphInfos['minPrice'] == self.graphInfos['maxPrice']):
                y = areaHeight - 0.5 * areaHeight + self.padding['top']
            else:
                y = areaHeight - ((price - self.graphInfos['minPrice']) / (self.graphInfos['maxPrice'] - self.graphInfos['minPrice'])) * areaHeight + self.padding['top']

            # graph color
            ctx.set_source_rgb(0.8, 0.6, 0.4)

            if ((lastX is not None) and (lastY is not None)):
                ctx.move_to(lastX, lastY)
            else:
                ctx.move_to(x, y)

            ctx.line_to(x, y)
            ctx.stroke()
            ctx.arc(x, y, 2, 0, 2 * math.pi)
            ctx.fill()
            lastX, lastY = x, y

            # draw date text (not for each item)
            if ((i % dateTextModulo) == 0):
                dateTextX = x
                dateTextY = areaHeight + self.padding['top'] + self.padding['bottom'] - self.textBorderSpace

                if (self.graphInfos['time'] == 'day'):
                    dateStr = str(dateTime.hour).zfill(2)
                elif (self.graphInfos['time'] == 'month'):
                    dateStr = str(dateTime.day).zfill(2)
                elif (self.graphInfos['time'] == 'year'):
                    dateStr = str(dateTime.month).zfill(2)
                elif (self.graphInfos['time'] == 'all'):
                    dateStr = str(dateTime.year).zfill(2)
                else:
                    return

                ctx.set_source_rgba(fontColor.red, fontColor.green, fontColor.blue, fontColor.alpha)
                ctx.move_to(dateTextX, dateTextY)
                ctx.show_text(dateStr)

            i += 1

        # draw price text
        priceTextX = self.textBorderSpace
        priceTextY = self.padding['top']
        pricesToDraw = []
        nbPricesToShow = 5
        priceTextYAdd = areaHeight / (nbPricesToShow - 1)

        if (self.graphInfos['maxPrice'] == self.graphInfos['minPrice']):
            midPrice = self.graphInfos['maxPrice'] - (self.graphInfos['maxPrice'] - self.graphInfos['minPrice']) / 2
            pricesToDraw.append(midPrice)
            priceTextY += areaHeight / 2
        else:
            for i in range(nbPricesToShow):
                price = self.graphInfos['minPrice'] + (self.graphInfos['maxPrice'] - self.graphInfos['minPrice']) * (((nbPricesToShow - 1) - i) / (nbPricesToShow - 1))
                pricesToDraw.append(price)

        ctx.set_source_rgba(fontColor.red, fontColor.green, fontColor.blue, fontColor.alpha)

        for price in pricesToDraw:
            priceRounded = round(price, self.priceNbDigitsAfterDecimalPoint)

            ctx.move_to(priceTextX, priceTextY)
            ctx.show_text(tools.beautifyNumber(priceRounded))
            priceTextY += priceTextYAdd

        # show date column name
        ctx.select_font_face('', cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)

        if (self.graphInfos['time'] == 'day'):
            timeDataType = _('Hour')
        elif (self.graphInfos['time'] == 'month'):
            timeDataType = _('Day')
        elif (self.graphInfos['time'] == 'year'):
            timeDataType = _('Month')
        elif (self.graphInfos['time'] == 'all'):
            timeDataType = _('Year')
        else:
            return

        ctx.move_to(self.textBorderSpace, areaHeight + self.padding['top'] + self.padding['bottom'] - self.textBorderSpace)
        ctx.show_text(timeDataType)

        # show price column name
        ctx.move_to(self.textBorderSpace, self.textBorderSpace)
        ctx.show_text(_('Price') + ' (' + self.baseCurrency.symbol + ')')
