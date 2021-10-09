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

class SettingsWindow ():

    def __init__ (self, app):
        self.__app = app
        self.__app.addCssProvider('settingsWindow')
        self.__builder = self.__app.newBuilder('settingsWindow')

        self.__node = self.__builder.get_object('settingsWindow')
        self.__node.set_transient_for(self.__app.builder.get_object('window'))
        self.__node.connect('close-request', self.__closeRequest)

        self.__apiKeyEntryNode = self.__builder.get_object('settingsApiKeyEntry')
        self.__setApiKey()

        controllerKey = Gtk.EventControllerKey()
        self.__node.add_controller(controllerKey)
        controllerKey.connect('key-pressed', self.__keyPressed)

    def show (self):
        self.__node.show()

    ###########
    # PRIVATE #
    ###########

    def __keyPressed (self, ctrl, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.__closeRequest()

    def __setApiKey (self):
        nomicsApiKey = self.__app.settings.loadNomicsAPIKey()
        self.__apiKeyEntryNode.set_text(nomicsApiKey)

    def __closeRequest (self, obj = None, data = None):
        nomicsAPIKey = self.__apiKeyEntryNode.get_text()
        self.__app.settings.saveNomicsAPIKey(nomicsAPIKey)
        self.__node.hide()
