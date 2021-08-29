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

import datetime

def beautifyNumber (number):
    """
        If needed, add spaces to a number (int or float) and return the
        beautified number in a string
    """
    numberStr = list(str(number))
    numberStr.reverse()
    numberStr = ''.join(numberStr)
    newNumberStr = ''
    canPutSpace = False
    isFloat = '.' in numberStr
    if isFloat is False:
        canPutSpace = True
    i = 0
    for char in numberStr:
        newNumberStr = char + newNumberStr
        if canPutSpace is True:
            i += 1
            if (i % 3) == 0:
                newNumberStr = ' ' + newNumberStr
        if char == '.':
            canPutSpace = True
    return newNumberStr

def bestDigitsNumberAfterDecimalPoint (currencyPrice, baseCurrencyPrice):
    """
        Return the best digits number (after decimal point) for the currency
        price and the base currency price given
    """
    return len(str(round((baseCurrencyPrice * 1000) / currencyPrice)))

def datetimeToStr (dt):
    """
        Return the string format of a datetime (YYY-MM-DDTHH-MM-SSZ)
    """
    dtStr = '{}-{}-{}T{}:{}:{}Z'.format(str(dt.year).zfill(4),
                                        str(dt.month).zfill(2),
                                        str(dt.day).zfill(2),
                                        str(dt.hour).zfill(2),
                                        str(dt.minute).zfill(2),
                                        str(dt.second).zfill(2))
    return dtStr

def print_warning (str):
    """
        Print warning message followed by the str string and continue the app
    """
    print(' >>> WARNING: ' + str)

def utcToLocal (dt):
    return dt.replace(tzinfo = datetime.timezone.utc).astimezone(tz = None)
