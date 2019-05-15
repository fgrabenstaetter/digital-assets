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

class Currency ():

    def __init__ (self, name, symbol, websiteURL):
        """
            Init Currency
        """
        self.name = name
        self.symbol = symbol
        self.websiteURL = websiteURL

        self.price = None # in USD
        self.lastDayPrice = None
        self.dayVolume = None
        self.circulatingSupply = None
        self.maxSupply = None
        self.marketCap = None
        self.rank = None
        self.ath = None
        self.dayGraphData = None
        self.monthGraphData = None
        self.yearGraphData = None
        self.allGraphData = None
        self.favorite = False
