project('digital-assets', version: '2.0.0')

pymod = import('python')
pyins = pymod.find_installation('python3')
dependency('glib-2.0')
dependency('gtk4')
dependency('gobject-introspection-1.0')
dependency('py3cairo')

PRGM_PATH = '/fr/fgrabenstaetter/digital-assets/'
PRGM_HNAME = 'Digital Assets'
APP_ID = 'fr.fgrabenstaetter.DigitalAssets'
PYTHON_PACKAGE_NAME = 'dassets'
PYTHON_DIR = pyins.get_install_dir()
BIN_DIR = join_paths(get_option('prefix'), get_option('bindir'))
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'))
LOCALE_DIR = join_paths(get_option('prefix'), get_option('localedir'))

conf = configuration_data()
conf.set('PYTHON_DIR', PYTHON_DIR)
conf.set('LOCALE_DIR', LOCALE_DIR)
conf.set('DATA_DIR', join_paths(DATA_DIR, meson.project_name()))
conf.set('PRGM_VERSION', meson.project_version())
conf.set('PRGM_NAME', meson.project_name())
conf.set('PRGM_HNAME', PRGM_HNAME)
conf.set('PRGM_PATH', PRGM_PATH)
conf.set('APP_ID', APP_ID)

# Configure and install exec file
configure_file(input: join_paths(PYTHON_PACKAGE_NAME, meson.project_name() + '.in'),
               output: meson.project_name(),
               configuration: conf)
install_data(join_paths(meson.current_build_dir(), meson.project_name()),
             install_dir: BIN_DIR)

# Configure and install env file
configure_file(input: join_paths(PYTHON_PACKAGE_NAME, 'env.in'),
               output: 'env.py',
               configuration: conf)
install_data(join_paths(meson.current_build_dir(), 'env.py'),
             install_dir: join_paths(PYTHON_DIR, PYTHON_PACKAGE_NAME))

# Install the python package
install_subdir(PYTHON_PACKAGE_NAME,
               install_dir: PYTHON_DIR,
               exclude_files: ['env.in', meson.project_name() + '.in'])

subdir('data')
