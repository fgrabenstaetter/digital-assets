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

def beautifyNumber (number):
    # if needed, add spaces to a number (int or float) and return the beautified number in a str

    numberStr = list(str(number))
    numberStr.reverse()
    numberStr = ''.join(numberStr)
    newNumberStr = ''
    canPutSpace = False
    isFloat = '.' in numberStr
    if (isFloat is False):
        canPutSpace = True
    i = 0
    for char in numberStr:
        newNumberStr = char + newNumberStr
        if (canPutSpace is True):
            i += 1
            if ((i % 3) == 0):
                newNumberStr = ' ' + newNumberStr

        if (char == '.'):
            canPutSpace = True

    return newNumberStr

def bestDigitsNumberAfterDecimalPoint (currencyPrice, baseCurrencyPrice):
    
    return len(str(round((baseCurrencyPrice * 1000) / currencyPrice)))
