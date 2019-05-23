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
from gi.repository import Gtk, Gdk
from dassets.sys.settings import Settings

class SettingsWindow (Gtk.Window):

    def __init__ (self, mainWindow):
        """
            Init SettingsWindow
        """
        Gtk.Window.__init__(self, modal = True, resizable = False,
                            transient_for =  mainWindow)
        headerBar = Gtk.HeaderBar(title = _('Settings'),
                                  show_close_button = True)
        self.set_titlebar(headerBar)
        self.add_events(Gdk.EventType.KEY_PRESS)
        self.connect('key-press-event', self.__keyPressEvent)
        self.connect('delete-event', self.__deleteEvent)
        self.__settings = Settings()

        # Content
        self.set_border_width(30)
        listBox = Gtk.ListBox(selection_mode = Gtk.SelectionMode.NONE,
                              activate_on_single_click = False,
                              can_focus = False)

        # Nomics API Key
        apiKeyHBox = Gtk.Box(spacing = 18, border_width = 6)
        apiKeyLabel = Gtk.Label(label = _('Nomics API Key'), expand = True,
                                xalign = 0)
        self.__apiKeyEntry = Gtk.Entry(width_chars = 32, expand = True,
                                    text = self.__settings.loadNomicsAPIKey())
        apiKeyHBox.add(apiKeyLabel)
        apiKeyHBox.add(self.__apiKeyEntry)

        apiKeyInfosLabel = Gtk.Label(label = _('Please choose a new Nomics API key,'
                                     ' as the default one can be overloaded'),
                                     wrap = True,
                                     max_width_chars = 40,
                                     expand = True,
                                     name = 'settingsAPIKeyInfos')
        apiKeyInfosWebsite = Gtk.LinkButton.new_with_label(
                                                    'https://www.nomics.com',
                                                    'Nomics')

        apiKeyInfosBox = Gtk.Box(spacing = 18, border_width = 6)
        apiKeyInfosBox.add(apiKeyInfosLabel)
        apiKeyInfosBox.add(apiKeyInfosWebsite)
        apiKeyVBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                             border_width = 12,
                             spacing = 6)
        apiKeyVBox.add(apiKeyHBox)
        apiKeyVBox.add(apiKeyInfosBox)
        listBox.add(apiKeyVBox)

        self.add(listBox)
        self.show_all()

    def __keyPressEvent (self, obj, data):
        """
            Close the settings window if the key pressed is Escape (ESC)
        """
        if data.keyval == Gdk.KEY_Escape:
            self.close()

    def __deleteEvent (self, obj = None, data = None):
        """
            Save the settings when closing the window
        """
        nomicsAPIKey = self.__apiKeyEntry.get_text()
        self.__settings.saveNomicsAPIKey(nomicsAPIKey)
