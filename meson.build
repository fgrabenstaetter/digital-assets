project('digital-assets',
        version: '3.6',
        meson_version: '>= 0.48.0')


python_dep = dependency('python3', version: '>=3.5')
gtk_dep = dependency('gtk+-3.0')
pygobject_dep = dependency('pygobject-3.0')
pycairo_dep = dependency('py3cairo')

pymod = import('python')
pyins = pymod.find_installation('python3')

PYTHON_PACKAGE_NAME = 'dassets'
BIN_DIR = join_paths(get_option('prefix'), get_option('bindir'))
PYTHON_DIR = pyins.get_install_dir()
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'))
LOCALE_DIR = join_paths(get_option('prefix'), get_option('localedir'))

conf_exec = configuration_data()
conf_exec.set('PYTHON_DIR', PYTHON_DIR)
conf_exec.set('LOCALE_DIR', LOCALE_DIR)
conf_exec.set('LOCALE_DOMAIN', meson.project_name())
configure_file(input: meson.project_name() + '.in',
               output: meson.project_name(),
               configuration: conf_exec)

conf_env = configuration_data()
conf_env.set('DATA_DIR', join_paths(DATA_DIR, meson.project_name()))
conf_env.set('PRGM_VERSION', meson.project_version())
configure_file(input: join_paths(PYTHON_PACKAGE_NAME, 'env.in'),
               output: 'env.py',
               configuration: conf_env)

install_subdir(PYTHON_PACKAGE_NAME,
               install_dir: PYTHON_DIR,
               exclude_files: ['env.in'])
install_data(join_paths(meson.current_build_dir(), 'env.py'),
             install_dir: join_paths(PYTHON_DIR, PYTHON_PACKAGE_NAME))
install_data(join_paths(meson.current_build_dir(), meson.project_name()),
             install_dir: BIN_DIR)
subdir('data')
