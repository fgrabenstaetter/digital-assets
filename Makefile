WHOAMI = $(shell whoami)
ifneq ($(WHOAMI), root)
$(error "You should execute this script as root")
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

.SILENT: install packages_ok
install: $(DATA_DIR) $(PACKAGE_DIR) $(EXEC_FILE) packages_ok
	mkdir -p $(USER_RESOURCES_DIR)
	cp -R $(RESOURCES_DIR)* $(USER_RESOURCES_DIR)

	cp $(ICONS_DIR)scalable/$(EXEC_FILE).svg $(USER_ICONS_DIR)scalable/apps/
	cp $(ICONS_DIR)64x64/$(EXEC_FILE).png $(USER_ICONS_DIR)64x64/apps/
	cp $(ICONS_DIR)48x48/$(EXEC_FILE).png $(USER_ICONS_DIR)48x48/apps/
	cp $(ICONS_DIR)32x32/$(EXEC_FILE).png $(USER_ICONS_DIR)32x32/apps/
	cp $(ICONS_DIR)24x24/$(EXEC_FILE).png $(USER_ICONS_DIR)24x24/apps/
	cp $(ICONS_DIR)22x22/$(EXEC_FILE).png $(USER_ICONS_DIR)22x22/apps/

	cp $(DESKTOP_FILE) $(USER_DESKTOP_FILE_DIR)
	chmod +x $(EXEC_FILE)
	cp $(EXEC_FILE) $(USER_EXEC_FILE_DIR)
	
	mkdir -p $(USER_PACKAGE_DIR)
	cp -R $(PACKAGE_DIR) -t $(USER_PACKAGE_DIR)
	gtk-update-icon-cache $(USER_ICONS_DIR) 2> /dev/null
	$(info => Success)

packages_ok:
	(pkgconf --exists python3) || (echo "Package 'python3' not found."; exit 1)
	(pkgconf --exists gtk+-3.0) || (echo "Package 'gtk3' not found."; exit 1)
	(pkgconf --exists pygobject-3.0) || (echo "Package 'pygobject3' not found."; exit 1)
	(pkgconf --exists py3cairo) || (echo "Package 'py3cairo' not found."; exit 1)
