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
from dassets.env import *
from dassets.ui.settingsWindow import SettingsWindow

class HeaderBar (Gtk.HeaderBar):

    def __init__ (self, mainWindow, defaultQuoteCurrencySymbol):
        """
            Init HeaderBar
        """
        Gtk.HeaderBar.__init__(self)
        self.__mainWindow = mainWindow
        self.set_show_close_button(True)
        self.set_title('Digital Assets')

        self.__quoteCurrencies =  self.__mainWindow.currencies
        self.actualQuoteCurrencySymbol = defaultQuoteCurrencySymbol
        # default sort method
        self.actualSortMethodName = 'rank'
        self.__createMenu()
        self.__createQuoteCurrencySwitch()
        self.__createSearchEntry()
        self.__createSortMethodSwitch()

    def showSettingsDialog (self, obj = None, data = None):
        settingsDialog = SettingsWindow(self.__mainWindow)

    def showAboutDialog (self, obj = None, data = None):
        aboutDialog = Gtk.AboutDialog(
            authors = ['François Grabenstaetter <francoisgrabenstaetter@gmail.com>'],
            license_type = Gtk.License.GPL_3_0_ONLY,
            version = PRGM_VERSION,
            comments = _('Cryptocurrencies prices and statistics') + '\nBTC:  bc1q4vupl5zwxctn7lwacqdqp4u07gfwj2jsy7ums0 \nETH:  0xE7F52826f22B0F48BD045b4f9B61a219A64cb5f8',
            website = 'https://gitlab.gnome.org/fgrabenstaetter/digital-assets',
            website_label = 'GitLab',
            copyright = _('Crypto market cap & pricing data provided by Nomics') + '\nhttps://nomics.com'
        )
        aboutDialog.set_modal(True)
        aboutDialog.set_transient_for(self.__mainWindow)
        aboutDialog.show()


    ###########
    # PRIVATE #
    ###########

    def __createMenu (self):
        """
            Create and add menu widgets to the HeaderBar
        """
        menuButton = Gtk.ToggleButton()
        image = Gtk.Image().new_from_icon_name('open-menu-symbolic', 1)
        menuButton.add(image)
        self.pack_end(menuButton)

        menuPopover = Gtk.Popover(relative_to = menuButton, border_width = 6)
        menupopoverCurrenciesBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        menuPopover.add(menupopoverCurrenciesBox)

        def menuPopoverClosedEvent (obj = None, data = None):
            menuButton.set_active(False)

        def menuButtonToggledEvent (obj = None, data = None):
            if (menuButton.get_active() is True):
                menuPopover.popup()

        menuPopover.connect('closed', menuPopoverClosedEvent)
        menuButton.connect('toggled', menuButtonToggledEvent)

        menuPopoverButtonSettings = Gtk.ModelButton(text = _('Settings'), xalign = 0)
        menuPopoverButtonSettings.connect('clicked', self.showSettingsDialog)
        menuPopoverButtonAbout = Gtk.ModelButton(text = _('About'), xalign = 0)
        menuPopoverButtonAbout.connect('clicked', self.showAboutDialog)

        menupopoverCurrenciesBox.add(menuPopoverButtonSettings)
        menupopoverCurrenciesBox.add(menuPopoverButtonAbout)
        menupopoverCurrenciesBox.show_all()

    def __createQuoteCurrencySwitch (self):
        """
            Create and add quote currency switch widgets to the HeaderBar
        """
        actualQuoteCurrency = self.__quoteCurrencies[self.actualQuoteCurrencySymbol]
        buttonBox = Gtk.Box(spacing = 10)
        switchButtonLabelName = Gtk.Label()
        switchButtonLabelName.set_markup('<b>' + actualQuoteCurrency.name + '</b>')
        switchButtonLabelSymbol = Gtk.Label.new(actualQuoteCurrency.symbol)

        buttonBox.add(switchButtonLabelName)
        buttonBox.add(switchButtonLabelSymbol)

        switchButton = Gtk.ToggleButton()
        switchButton.curSymbol = actualQuoteCurrency.symbol
        switchButton.add(buttonBox)
        self.pack_start(switchButton)

        # pop-over
        popover = Gtk.Popover(relative_to = switchButton, border_width = 6)
        popoverCurrenciesBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        popoverScrolledWindow = Gtk.ScrolledWindow()
        popoverScrolledWindow.set_min_content_height(200)
        popoverScrolledWindow.set_max_content_height(200)
        popoverScrolledWindow.set_min_content_width(180)
        popoverScrolledWindow.set_max_content_width(180)
        popoverScrolledWindow.add(popoverCurrenciesBox)

        def popoverClosedEvent (obj = None, data = None):
            switchButton.set_active(False)

        def buttonToggledEvent (obj = None, data = None):
            if switchButton.get_active() is True:
                popover.popup()
                # clear search entry
                searchEntry.set_text('')

                # reload buttons
                otherCurrencies = []
                for cur in self.__getQuoteCurrenciesSorted():
                    if cur.symbol != self.actualQuoteCurrencySymbol:
                        otherCurrencies.append(cur)

                def assignStr (button):
                    if isinstance(button, Gtk.SearchEntry):
                        return

                    assert len(otherCurrencies) > 0
                    button.labelName.set_markup('<b>' + otherCurrencies[0].name + '</b>')
                    button.labelSymbol.set_label(otherCurrencies[0].symbol)
                    button.curName = otherCurrencies[0].name
                    button.curSymbol = otherCurrencies[0].symbol
                    del otherCurrencies[0]

                popoverCurrenciesBox.foreach(assignStr)

        popover.connect('closed', popoverClosedEvent)
        switchButton.connect('toggled', buttonToggledEvent)

        def searchEntrySearchEvent (obj, data = None):
            text = obj.get_text().lower()
            for child in popoverCurrenciesBox.get_children():
                if child is not obj and text not in child.curName.lower() and text not in child.curSymbol.lower():
                    child.hide()
                else:
                    child.show()

        # add search entry
        searchEntry = Gtk.SearchEntry(margin_bottom = 10)
        searchEntry.connect('search-changed', searchEntrySearchEvent)

        # main box
        popoverBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        popoverBox.add(searchEntry)
        popoverBox.add(popoverScrolledWindow)
        popover.add(popoverBox)

        def changeQuoteCurrency (obj, data = None):
            self.actualQuoteCurrencySymbol = obj.curSymbol
            popover.popdown()
            switchButtonLabelName.set_markup('<b>' + obj.curName + '</b>')
            switchButtonLabelSymbol.set_text(obj.curSymbol)
            # sort again currencies
            self.__mainWindow.currencySwitcher.invalidate_sort()
            # reload currencyView
            self.__mainWindow.currencyView.reload()

        # create currencies buttons
        popoverButtons = []
        for cur in self.__getQuoteCurrenciesSorted():
            if cur.symbol != self.actualQuoteCurrencySymbol:
                button = Gtk.ModelButton(xalign = 0)
                button.connect('clicked', changeQuoteCurrency)
                button.labelName = Gtk.Label(wrap = True, xalign = 0)
                button.labelSymbol = Gtk.Label(name = 'quoteCurrencyPopoverSymbol')

                buttonBox = button.get_children()[0]
                buttonBox.pack_start(button.labelName, False, False, 0)
                buttonBox.pack_end(button.labelSymbol, False, False, 0)
                popoverCurrenciesBox.add(button)

        popoverBox.show_all()

    def __getQuoteCurrenciesSorted (self):
        """
            Return a sorted list of quote currencies
        """
        if self.__quoteCurrencies['BTC'].rank is not None:
            # sort by rank
            return sorted(list(self.__quoteCurrencies.values()), key = lambda cur: cur.rank if cur.rank is not None else 9999)
        else:
            # sort by name
            return sorted(list(self.__quoteCurrencies.values()), key = lambda cur: cur.name)

    def __createSearchEntry (self):
        """
            Create and add search widgets to the HeaderBar
        """
        self.searchButton = Gtk.ToggleButton()
        icon = Gtk.Image().new_from_icon_name('system-search-symbolic', 1)
        self.searchButton.add(icon)
        self.pack_start(self.searchButton)

        def searchButtonClicked (obj = None, data = None):
            if self.searchButton.get_active() is False:
                with self.searchButton.handler_block(handler):
                    self.__mainWindow.searchEntry.set_text('')
                    self.searchButton.set_active(False)
                self.__mainWindow.searchEntryRevealer.set_reveal_child(False)
                self.__mainWindow.currencySwitcher.scrollToActualChild()
            else:
                self.__mainWindow.searchEntryRevealer.set_reveal_child(True)
                self.__mainWindow.searchEntry.grab_focus_without_selecting()

        handler = self.searchButton.connect('clicked', searchButtonClicked)

    def __createSortMethodSwitch (self):
        """
            Create and add currencies sort method switch widgets to the
            HeaderBar
        """
        button = Gtk.ToggleButton()
        buttonImage = Gtk.Image().new_from_icon_name('view-list-symbolic', 1)
        button.add(buttonImage)

        def buttonToggledEvent (obj = None, data = None):
            if button.get_active() is True:
                popover.popup()

        # popover
        popover = Gtk.Popover(relative_to = button, border_width = 6)
        popoverCurrenciesBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        def popoverClosedEvent (obj = None, data = None):
            button.set_active(False)

        button.connect('toggled', buttonToggledEvent)
        popover.connect('closed', popoverClosedEvent)
        sortMethodNames = (
            ('rank', _('Rank')),
            ('name', _('Name')),
            ('dayPriceChange', _('Change')),
            ('volume', _('Volume')),
            ('ath', 'ATH'))

        def rowClickedEvent (obj, data = None):
            obj.radioButton.clicked()
            self.actualSortMethodName = obj.name
            popover.popdown()
            self.__mainWindow.currencySwitcher.invalidate_sort()

        for name, str in sortMethodNames:
            row = Gtk.ModelButton()
            row.name = name
            row.connect('clicked', rowClickedEvent)

            rowBox = row.get_children()[0]
            label = Gtk.Label.new(str)
            popoverCurrenciesBoxChildren = popoverCurrenciesBox.get_children()

            if len(popoverCurrenciesBoxChildren) > 0:
                radioButton = Gtk.RadioButton(group = popoverCurrenciesBoxChildren[0].radioButton)
            else:
                radioButton = Gtk.RadioButton()

            rowBox.pack_start(label, False, False, 0)
            rowBox.pack_end(radioButton, False, False, 0)
            row.radioButton = radioButton
            popoverCurrenciesBox.add(row)

        popover.add(popoverCurrenciesBox)
        popoverCurrenciesBox.show_all()
        self.add(button)
