# Install locale files
install_subdir('locale',
               install_dir: LOCALE_DIR,
               strip_directory: true,
               exclude_files: [meson.project_name() + '.pot',
                               'fr/LC_MESSAGES/' + meson.project_name() + '.po'])

# Validate the desktop file
desktop_file_validate = find_program('desktop-file-validate', required: false)
if desktop_file_validate.found()
  test('Validating the desktop file',
       desktop_file_validate,
       args: join_paths(meson.current_source_dir(), meson.project_name() + '.desktop'))
endif

# Install the desktop file
desktop_file_install = find_program('desktop-file-install')
run_command(desktop_file_install, meson.project_name() + '.desktop')
install_data(meson.project_name() + '.desktop',
			 install_dir: join_paths(DATA_DIR, 'applications'))

# Validate the gschema file
glib_compile_schemas = find_program('glib-compile-schemas')
test('Validating the gschema file',
     glib_compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])

# Install the gschema file
install_data(meson.project_name() + '.gschema.xml',
             install_dir: join_paths(DATA_DIR, 'glib-2.0/schemas'))
run_command(glib_compile_schemas, join_paths(DATA_DIR, 'glib-2.0/schemas/'))

# Install the gresource file
gnome = import('gnome')
gnome.compile_resources (
  meson.project_name(),
  meson.project_name() + '.gresource.xml',
  gresource_bundle: true,
  source_dir: '.',
  install_dir: join_paths(DATA_DIR, meson.project_name()),
  install: true
)

# Validate the appdata file
appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validating the appdata file',
       appstream_util,
       args: ['validate', join_paths(meson.current_source_dir(), meson.project_name() + '.appdata.xml')])
endif

# Install the appdata file
install_data(meson.project_name() + '.appdata.xml',
             install_dir: join_paths(DATA_DIR, 'metainfo'))

# Install icons
install_subdir('icons', install_dir: DATA_DIR)
run_command('gtk-update-icon-cache', '-qtf', join_paths(DATA_DIR, 'icons/hicolor'))
