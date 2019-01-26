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
import gettext

# app version
appVersion = '1.0.2'

class HeaderBar (Gtk.HeaderBar):
    def __init__ (self, mainWindow):
        Gtk.HeaderBar.__init__(self)
        self.mainWindow = mainWindow
        self.set_show_close_button(True)
        self.set_title('Digital Assets')

        self.baseCurrencies =  self.mainWindow.getCurrencies()
        self.actualBaseCurrencySymbol = self.baseCurrencies[list(self.baseCurrencies.keys())[0]].symbol
        self.actualSortMethodName = 'rank' # default sort method
        self.createMenu()
        self.createBaseCurrencySwitch()
        self.createSearchEntry()
        self.createSortMethodSwitch()

    def createMenu (self):
        # create and add menu widgets to the header bar

        menuButton = Gtk.ToggleButton()
        image = Gtk.Image().new_from_icon_name('open-menu-symbolic', 1)
        menuButton.add(image)
        self.pack_end(menuButton)

        menuPopover = Gtk.Popover(relative_to = menuButton, border_width = 6)
        menuPopoverBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        menuPopover.add(menuPopoverBox)

        def menuPopoverClosedEvent (obj = None, data = None):
            menuButton.set_active(False)


        def menuButtonToggledEvent (obj = None, data = None):
            if (menuButton.get_active() is True):
                menuPopover.popup()

        menuPopover.connect('closed', menuPopoverClosedEvent)
        menuButton.connect('toggled', menuButtonToggledEvent)

        def showAboutDialog (obj = None, data = None):
            menuPopover.popdown()
            aboutDialog = Gtk.AboutDialog(
                authors = ['François Grabenstaetter'],
                license_type = Gtk.License.GPL_3_0_ONLY,
                program_name = 'Digital Assets',
                version = appVersion,
                comments = _('Prices, statistics and informations about Digital Assets\nThanks to Nomics (https://nomics.com) for their free API\nDonations') + ' BTC:   bc1qejj6y2gvya5rrun4sfsl08qdeyv36ndhm0ml85',
                website = 'https://github.com/fgrabenstaetter/digital-assets',
                website_label = 'GitHub'
            )
            aboutDialog.set_modal(True)
            aboutDialog.set_transient_for(self.mainWindow)
            aboutDialog.show()

        menuPopoverButtonAbout = Gtk.ModelButton(_('About'), xalign = 0)
        menuPopoverButtonAbout.connect('clicked', showAboutDialog)
        menuPopoverButtonQuit = Gtk.ModelButton(_('Quit'), xalign = 0)
        menuPopoverButtonQuit.connect('clicked', self.mainWindow.quit)

        menuPopoverBox.add(menuPopoverButtonAbout)
        menuPopoverBox.add(menuPopoverButtonQuit)
        menuPopoverBox.show_all()

    def createBaseCurrencySwitch (self):
        # create and add base currency switch widgets to the header bar
        actualBaseCurrency = self.baseCurrencies[self.actualBaseCurrencySymbol]

        buttonBox = Gtk.Box(spacing = 10)
        self.switchButtonLabelName = Gtk.Label()
        self.switchButtonLabelName.set_markup('<b>' + actualBaseCurrency.name + '</b>')
        self.switchButtonLabelSymbol = Gtk.Label(actualBaseCurrency.symbol)
        panDownImg = Gtk.Image().new_from_icon_name('pan-down-symbolic', 1)

        buttonBox.add(self.switchButtonLabelName)
        buttonBox.add(self.switchButtonLabelSymbol)
        buttonBox.add(panDownImg)

        switchButton = Gtk.ToggleButton()
        switchButton.curSymbol = actualBaseCurrency.symbol
        switchButton.add(buttonBox)
        self.pack_start(switchButton)

        # pop-over
        popover = Gtk.Popover(relative_to = switchButton, border_width = 6)
        popoverBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        popoverScrolledWindow = Gtk.ScrolledWindow()
        popoverScrolledWindow.set_min_content_height(200)
        popoverScrolledWindow.set_max_content_height(200)
        popoverScrolledWindow.set_min_content_width(180)
        popoverScrolledWindow.set_max_content_width(180)

        popoverScrolledWindow.add(popoverBox)
        popover.add(popoverScrolledWindow)

        def popoverClosedEvent (obj = None, data = None):
            switchButton.set_active(False)

        def buttonToggledEvent (obj = None, data = None):
            if (switchButton.get_active() is True):
                popover.popup()

        popover.connect('closed', popoverClosedEvent)
        switchButton.connect('toggled', buttonToggledEvent)

        def changeBaseCurrency (obj, data = None):
            self.actualBaseCurrencySymbol = obj.curSymbol
            popover.popdown()
            otherCurrencies = []

            for curSymbol in self.baseCurrencies.keys():
                if (self.actualBaseCurrencySymbol != curSymbol):
                    otherCurrencies.append(self.baseCurrencies[curSymbol])

            self.switchButtonLabelName.set_markup('<b>' + obj.curName + '</b>')
            self.switchButtonLabelSymbol.set_text(obj.curSymbol)

            def assignStr (button):
                assert len(otherCurrencies) > 0
                button.labelName.set_markup('<b>' + otherCurrencies[0].name + '</b>')
                button.labelSymbol.set_label(otherCurrencies[0].symbol)
                button.curName = otherCurrencies[0].name
                button.curSymbol = otherCurrencies[0].symbol
                del otherCurrencies[0]
            popoverBox.foreach(assignStr)

            # sort again currencies
            self.mainWindow.currencySwitcher.invalidate_sort()

            # reload currencyView
            self.mainWindow.currencyView.reload()

        popoverButtons = []
        for curSymbol in self.baseCurrencies.keys():
            if (curSymbol != self.actualBaseCurrencySymbol):
                cur = self.baseCurrencies[curSymbol]
                button = Gtk.ModelButton(xalign = 0)

                button.curName = cur.name
                button.curSymbol = cur.symbol
                button.connect('clicked', changeBaseCurrency)

                buttonBox = button.get_children()[0]
                button.labelName = Gtk.Label(wrap = True, xalign = 0)
                button.labelName.set_markup('<b>' + cur.name + '</b>')
                button.labelSymbol = Gtk.Label(cur.symbol, name = 'baseCurrencyPopoverSymbol')

                buttonBox.pack_start(button.labelName, False, False, 0)
                buttonBox.pack_end(button.labelSymbol, False, False, 0)
                popoverBox.add(button)

        popoverScrolledWindow.show_all()

    def createSearchEntry (self):
        # create and add search widgets to the headerbar

        self.searchButton = Gtk.ToggleButton()
        icon = Gtk.Image().new_from_icon_name('system-search-symbolic', 1)
        self.searchButton.add(icon)
        self.pack_start(self.searchButton)

        def searchButtonClicked (obj = None, data = None):
            if (self.searchButton.get_active() is False):
                self.mainWindow.searchEntryRevealer.set_reveal_child(False)
                self.mainWindow.searchEntry.set_text('')
            else:
                self.mainWindow.searchEntryRevealer.set_reveal_child(True)
                self.mainWindow.searchEntry.grab_focus()

        self.searchButton.connect('clicked', searchButtonClicked)

    def createSortMethodSwitch (self):
        # create and add currencies sort method switch widgets to the header bar

        button = Gtk.ToggleButton()
        buttonImage = Gtk.Image().new_from_icon_name('view-list-symbolic', 1)
        button.add(buttonImage)

        def buttonToggledEvent (obj = None, data = None):
            if (button.get_active() is True):
                popover.popup()

        # popover
        popover = Gtk.Popover(relative_to = button, border_width = 6)
        popOverBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        def popOverClosedEvent (obj = None, data = None):
            button.set_active(False)

        button.connect('toggled', buttonToggledEvent)
        popover.connect('closed', popOverClosedEvent)

        sortMethodNames = (
            ('rank', _('Rank')),
            ('name', _('Name')),
            ('dayPriceChange', _('Change')),
            ('volume', _('Volume'))
        )

        def rowClickedEvent (obj, data = None):
            obj.radioButton.clicked()
            self.actualSortMethodName = obj.name
            popover.popdown()
            self.mainWindow.currencySwitcher.invalidate_sort()

        for name, str in sortMethodNames:
            row = Gtk.ModelButton()
            row.name = name
            row.connect('clicked', rowClickedEvent)

            rowBox = row.get_children()[0]
            label = Gtk.Label(str)

            popOverBoxChildren = popOverBox.get_children()
            if (len(popOverBoxChildren) > 0):
                radioButton = Gtk.RadioButton(group = popOverBoxChildren[0].radioButton)
            else:
                radioButton = Gtk.RadioButton()

            rowBox.pack_start(label, False, False, 0)
            rowBox.pack_end(radioButton, False, False, 0)

            row.radioButton = radioButton
            popOverBox.add(row)

        popover.add(popOverBox)
        popOverBox.show_all()
        self.add(button)
