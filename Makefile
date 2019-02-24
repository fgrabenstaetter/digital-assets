$(info [1 / 2] Checking if required packages are installed)

# check if packages are installed
GTK3_OK = $(shell ldconfig -p | grep -F libgtk-3.so 2> /dev/null)
ifeq ($(GTK3_OK), )
	$(error package 'gtk3' not found)
endif

PYTHON3_OK = $(shell python3 --version 2> /dev/null)
ifeq ($(PYTHON3_OK), )
	$(error package 'python3' not found)
endif

PIP3_OK = $(shell pip3 --version 2> /dev/null 2> /dev/null)
ifeq ($(PIP3_OK), )
	$(error package 'pip3' not found)
endif

PYGOBJECT_OK = $(shell pip3 list | grep -F PyGObject 2> /dev/null)
ifeq ($(PYGOBJECT_OK), )
	$(error python package 'PyGObject' not found. You can install it with 'pip3 install PyGObject')
endif

PYCAIRO_OK = $(shell pip3 list | grep -F pycairo 2> /dev/null)
ifeq ($(PYCAIRO_OK), )
	$(error python package 'pycairo' not found. You can install it with 'pip3 install pycairo')
endif

PYTHON_DIR_NAME = python$(shell python3 --version | cut -f 2 -d " " | cut -f 1,2 -d ".")
DATA_DIR = share/
PACKAGE_NAME = DigitalAssets
EXEC_FILE = digital-assets

RESOURCES_DIR = $(DATA_DIR)resources/
ICONS_DIR = $(DATA_DIR)icons/
DESKTOP_FILE = $(DATA_DIR)$(EXEC_FILE).desktop
PACKAGE_DIR = DigitalAssets/

USER_RESOURCES_DIR = /usr/share/$(EXEC_FILE)/
USER_ICONS_DIR = /usr/share/icons/hicolor/
USER_DESKTOP_FILE_DIR = /usr/share/applications/
USER_PACKAGE_DIR = /usr/lib/$(PYTHON_DIR_NAME)/site-packages/
USER_EXEC_FILE_DIR = /usr/bin/

.SILENT: install
install: $(DATA_DIR) $(PACKAGE_DIR) $(EXEC_FILE)

	$(info [2 / 2] Installing files)

	# copy resources
	mkdir -p $(USER_RESOURCES_DIR)
	cp -R $(RESOURCES_DIR)* $(USER_RESOURCES_DIR)

	# copy app icons
	cp $(ICONS_DIR)scalable/$(EXEC_FILE).svg $(USER_ICONS_DIR)scalable/apps/
	cp $(ICONS_DIR)64x64/$(EXEC_FILE).png $(USER_ICONS_DIR)64x64/apps/
	cp $(ICONS_DIR)48x48/$(EXEC_FILE).png $(USER_ICONS_DIR)48x48/apps/
	cp $(ICONS_DIR)32x32/$(EXEC_FILE).png $(USER_ICONS_DIR)32x32/apps/
	cp $(ICONS_DIR)24x24/$(EXEC_FILE).png $(USER_ICONS_DIR)24x24/apps/
	cp $(ICONS_DIR)22x22/$(EXEC_FILE).png $(USER_ICONS_DIR)22x22/apps/

	# copy desktop file
	cp $(DESKTOP_FILE) $(USER_DESKTOP_FILE_DIR)

	# copy executable file (and make it executable)
	chmod +x $(EXEC_FILE)
	cp $(EXEC_FILE) $(USER_EXEC_FILE_DIR)

	# copy package
	mkdir -p $(USER_PACKAGE_DIR)
	cp -R $(PACKAGE_DIR) -t $(USER_PACKAGE_DIR)

	# update gtk icon cache
	gtk-update-icon-cache $(USER_ICONS_DIR)
