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
from gi.repository import Gtk, Gdk
from dassets.sys.settings import Settings

class SettingsWindow ():

    def __init__ (self, builder):
        """
            Init SettingsWindow
        """
        self.__builder = builder
        self.__settings = Settings()
        self.__uiObj = self.__builder.get_object('settingsWindow')
        self.__uiObj.connect('close-request', self.__closeEvent)

        self.__settingsApiKeyEntryUiObj = self.__builder.get_object('settingsApiKeyEntry')

        controllerKey = Gtk.EventControllerKey()
        self.__uiObj.add_controller(controllerKey)
        controllerKey.connect('key-pressed', self.__keyPressEvent)

        self.__setApiKey()

    def __keyPressEvent (self, ctrl, keyval, keycode, state):
        """
            Close the settings window if the key pressed is Escape (ESC)
        """
        if keyval == Gdk.KEY_Escape:
            self.__closeEvent()

    def __setApiKey (self):
        """
            Load API key from settings and put it in the entry
        """
        nomicsApiKey = self.__settings.loadNomicsAPIKey()
        self.__settingsApiKeyEntryUiObj.set_text(nomicsApiKey)

    def __closeEvent (self, obj = None, data = None):
        """
            Save the settings when closing the window
        """
        nomicsAPIKey = self.__settingsApiKeyEntryUiObj.get_text()
        self.__settings.saveNomicsAPIKey(nomicsAPIKey)
        self.__uiObj.hide()
