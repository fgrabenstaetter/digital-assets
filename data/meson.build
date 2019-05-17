install_subdir('resources',
               install_dir: join_paths(DATA_DIR, meson.project_name()),
               strip_directory: true)
install_subdir('locale',
               install_dir: LOCALE_DIR,
               strip_directory: true,
               exclude_files: [meson.project_name() + '.pot',
                               'fr/LC_MESSAGES/' + meson.project_name() + '.po'])

desktop_file_install = find_program('desktop-file-install')
if desktop_file_install.found()
  run_command('desktop-file-install', meson.project_name() + '.desktop')
endif

install_data(meson.project_name() + '.gschema.xml',
             install_dir: join_paths(DATA_DIR, 'glib-2.0/schemas'))

glib_compile_schemas = find_program('glib-compile-schemas')
if glib_compile_schemas.found()
  run_command('glib-compile-schemas', join_paths(DATA_DIR, 'glib-2.0/schemas'))
endif

install_data(meson.project_name() + '.appdata.xml',
             install_dir: join_paths(DATA_DIR, 'metainfo'))
install_subdir('icons', install_dir: DATA_DIR)

run_command('gtk-update-icon-cache', '-qtf', join_paths(DATA_DIR, 'icons/hicolor'))
