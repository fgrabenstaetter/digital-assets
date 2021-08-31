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
from dassets.sys import tools
import math, datetime

class Graph (Gtk.DrawingArea):

    def __init__ (self):
        """
            Init Graph
        """
        Gtk.DrawingArea.__init__(self)
        self.set_size_request(600, 250)
        self.connect('draw', self.__drawGraph)

        self.__textBorderSpace = 10
        self.__padding = {'top': 40, 'right': 20, 'bottom': 60, 'left': 90}
        self.__graphData = None
        self.__graphInfos = {}
        self.__quoteCurrency = None

        self.show_all()

    def setGraph (self, graphData, graphTime, quoteCurrency, priceNbDigitsAfterDecimalPoint):
        """
            Load a new graph into the Graph object
        """
        # Change prices to consider quoteCurrency prices
        if quoteCurrency.symbol == 'USD':
            newGraphData = graphData
        else:
            quoteCurrencyGraphData = getattr(quoteCurrency, graphTime + 'GraphDataUSD')
            if len(graphData) == 0 or len(quoteCurrencyGraphData) == 0:
                newGraphData = None
            else:
                newGraphData = []
                i1, i2 = 0, 0
                l1, l2 = len(graphData), len(quoteCurrencyGraphData)

                while i1 < l1 and i2 < l2:
                    d1 = graphData[i1][0]
                    d2 = quoteCurrencyGraphData[i2][0]
                    tdelta = d1 - d2

                    if tdelta.days == 0:
                        p1 = graphData[i1][1]
                        p2 = quoteCurrencyGraphData[i2][1]
                        price = p1 / p2
                        newGraphData.append((d1, price))
                        i1 += 1
                        i2 += 1
                    elif tdelta.days < 0:
                        i1 += 1
                    else:
                        i2 += 1

        self.__graphData = newGraphData
        self.__quoteCurrency = quoteCurrency
        self.__priceNbDigitsAfterDecimalPoint = priceNbDigitsAfterDecimalPoint

        # loading graph infos
        minPrice, maxPrice, nbPrices = None, None, 0

        if self.__graphData is not None:
            for gp in self.__graphData:
                if minPrice is None or gp[1] < minPrice:
                    minPrice = gp[1]
                if maxPrice is None or gp[1] > maxPrice:
                    maxPrice = gp[1]
                nbPrices += 1

        self.__graphInfos['minPrice'] = minPrice
        self.__graphInfos['maxPrice'] = maxPrice
        self.__graphInfos['nbPrices'] = nbPrices
        self.__graphInfos['time'] = graphTime

        self.queue_draw()

    ###########
    # PRIVATE #
    ###########

    def __drawGraph (self, obj, ctx):
        """
            Draw the current graph
        """
        # graphData is an array of (timestamp, price)
        if self.__graphData is None or len(self.__graphData) < 3:
            # no data for this period and this currency / quote currency
            ctx.set_source_rgba(0, 0, 0, 0)
            ctx.fill()
            return

        areaWidth = self.get_size_request()[0] - self.__padding['left'] - self.__padding['right']
        areaHeight = self.get_size_request()[1] - self.__padding['top'] - self.__padding['bottom']
        coords = []
        cnt = 0

        # calculate coords and draw dates
        dateTextModulo = math.ceil(self.__graphInfos['nbPrices'] / 8)
        fontColor = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        fontColor.parse('rgba')
        ctx.set_source_rgba(fontColor.red, fontColor.green, fontColor.blue, fontColor.alpha)
        ctx.set_font_size(12)

        for dateTime, price in self.__graphData:
            x = (cnt / self.__graphInfos['nbPrices']) * areaWidth + self.__padding['left']

            if self.__graphInfos['minPrice'] == self.__graphInfos['maxPrice']:
                y = areaHeight - 0.5 * areaHeight + self.__padding['top']
            else:
                y = areaHeight - ((price - self.__graphInfos['minPrice']) / (self.__graphInfos['maxPrice'] - self.__graphInfos['minPrice'])) * areaHeight + self.__padding['top']

            coords.append((x, y))

            # draw date text (not for each item)
            if (cnt % dateTextModulo) == 0:
                dateTextX = x
                dateTextY = areaHeight + self.__padding['top'] + self.__padding['bottom'] - self.__textBorderSpace

                if self.__graphInfos['time'] == 'day':
                    dateStr = str(dateTime.strftime('%X')).split(':')[0] + str(dateTime.strftime(' %p'))
                elif self.__graphInfos['time'] == 'month':
                    dateStr = str(dateTime.day).zfill(2)
                elif self.__graphInfos['time'] == 'year':
                    dateStr = str(dateTime.month).zfill(2)
                elif self.__graphInfos['time'] == 'alltime':
                    dateStr = str(dateTime.year).zfill(2)
                else:
                    return

                ctx.move_to(dateTextX, dateTextY)
                ctx.show_text(dateStr)

            cnt += 1

        # draw graphic representation
        lineWidth = 3
        minBodyHeight = 12
        areaBodyBottom = areaHeight + self.__padding['top'] + minBodyHeight
        ctx.new_path()

        for x, y in coords:
            ctx.line_to(x, y)
        path = ctx.copy_path() # save current path

        # draw light body
        ctx.line_to(coords[-1][0], areaBodyBottom)
        ctx.line_to(coords[0][0], areaBodyBottom)
        ctx.set_source_rgb(0.73, 0.87, 0.98)
        ctx.fill()

        # draw head bold line
        ctx.append_path(path)
        ctx.set_line_width(lineWidth)
        ctx.set_source_rgb(0.26, 0.65, 0.96)
        ctx.stroke()

        # draw prices
        priceTextX = self.__textBorderSpace
        priceTextY = self.__padding['top']
        pricesToDraw = []
        nbPricesToShow = 5
        priceTextYAdd = areaHeight / (nbPricesToShow - 1)

        if self.__graphInfos['maxPrice'] == self.__graphInfos['minPrice']:
            midPrice = self.__graphInfos['maxPrice'] - (self.__graphInfos['maxPrice'] - self.__graphInfos['minPrice']) / 2
            pricesToDraw.append(midPrice)
            priceTextY += areaHeight / 2
        else:
            for i in range(nbPricesToShow):
                price = self.__graphInfos['minPrice'] + (self.__graphInfos['maxPrice'] - self.__graphInfos['minPrice']) * (((nbPricesToShow - 1) - i) / (nbPricesToShow - 1))
                pricesToDraw.append(price)

        ctx.set_source_rgba(fontColor.red, fontColor.green, fontColor.blue, fontColor.alpha)

        for price in pricesToDraw:
            priceRounded = round(price, self.__priceNbDigitsAfterDecimalPoint)
            ctx.move_to(priceTextX, priceTextY)
            ctx.show_text(tools.beautifyNumber(priceRounded))
            priceTextY += priceTextYAdd

        # draw dates label
        ctx.select_font_face('', cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)

        if (self.__graphInfos['time'] == 'day'):
            timeDataType = _('Hour')
        elif (self.__graphInfos['time'] == 'month'):
            timeDataType = _('Day')
        elif (self.__graphInfos['time'] == 'year'):
            timeDataType = _('Month')
        elif (self.__graphInfos['time'] == 'alltime'):
            timeDataType = _('Year')
        else:
            return

        ctx.move_to(self.__textBorderSpace, areaHeight + self.__padding['top'] + self.__padding['bottom'] - self.__textBorderSpace)
        ctx.show_text(timeDataType)

        # draw prices label
        ctx.move_to(self.__textBorderSpace, self.__textBorderSpace)
        ctx.show_text(_('Price') + ' (' + self.__quoteCurrency.symbol + ')')
