# Install resources and locale
install_subdir('resources',
               install_dir: join_paths(DATA_DIR, meson.project_name()),
               strip_directory: true)
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
       args: [meson.project_name() + '.desktop'])
endif

# Install the desktop file
desktop_file_install = find_program('desktop-file-install')
run_command(desktop_file_install, meson.project_name() + '.desktop')

# Validate the gschema file
glib_compile_schemas = find_program('glib-compile-schemas')
test('Validating the gschema file',
     glib_compile_schemas,
     args: ['--strict', '--dry-run', meson.project_name() + 'gschema.xml'])

# Install the gschema file
install_data(meson.project_name() + '.gschema.xml',
             install_dir: join_paths(DATA_DIR, 'glib-2.0/schemas'))
run_command(glib_compile_schemas, join_paths(DATA_DIR, 'glib-2.0/schemas'))

# Validate the appdata file
appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validating the appdata file',
       appstream_util,
       args: ['validate-relax', meson.project_name() + '.appdata.xml'])
endif

# Install the appdata file
install_data(meson.project_name() + '.appdata.xml',
             install_dir: join_paths(DATA_DIR, 'metainfo'))

# Install icons
install_subdir('icons', install_dir: DATA_DIR)
run_command('gtk-update-icon-cache', '-qtf', join_paths(DATA_DIR, 'icons/hicolor'))
