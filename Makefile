PYTHON_DIR_NAME = python$(shell python3 --version | cut -f 2 -d " " | cut -f 1,2 -d ".")
DATA_DIR = data/

RESOURCES_DIR = $(DATA_DIR)resources/
ICONS_DIR = $(DATA_DIR)icons/
DESKTOP_FILE = $(DATA_DIR)digital-assets.desktop
PACKAGE_DIR = DigitalAssets/
EXEC_FILE = digital-assets

USER_RESOURCES_DIR = /usr/share/digital-assets/
USER_ICONS_DIR = /usr/share/icons/hicolor/
USER_DESKTOP_FILE_DIR = /usr/share/applications/
USER_PACKAGE_DIR = /usr/lib/$(PYTHON_DIR_NAME)/site-packages/DigitalAssets/
USER_EXEC_FILE_DIR = /usr/bin/

install: $(DATA_DIR) $(PACKAGE_DIR) $(EXEC_FILE)
	# copy resources
	mkdir -p $(USER_RESOURCES_DIR)
	cp -R $(RESOURCES_DIR)* $(USER_RESOURCES_DIR)

	# copy app icons
	cp $(ICONS_DIR)scalable/digital-assets.svg $(USER_ICONS_DIR)scalable/apps/
	cp $(ICONS_DIR)64x64/digital-assets.png $(USER_ICONS_DIR)64x64/apps/
	cp $(ICONS_DIR)48x48/digital-assets.png $(USER_ICONS_DIR)48x48/apps/
	cp $(ICONS_DIR)32x32/digital-assets.png $(USER_ICONS_DIR)32x32/apps/
	cp $(ICONS_DIR)24x24/digital-assets.png $(USER_ICONS_DIR)24x24/apps/
	cp $(ICONS_DIR)22x22/digital-assets.png $(USER_ICONS_DIR)22x22/apps/

	# copy desktop file
	cp $(DESKTOP_FILE) $(USER_DESKTOP_FILE_DIR)

	# copy executable file (and make it executable)
	chmod +x $(EXEC_FILE)
	cp $(EXEC_FILE) $(USER_EXEC_FILE_DIR)

	# copy package
	cp -R $(PACKAGE_DIR) $(USER_PACKAGE_DIR)
