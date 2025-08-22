# This build file has been created by consulting similar examples in the
# scipy repository and in the Python packages created and managed by Scott A.
# Socolofsky (tamoc and pyfrac).  This build tries to implement the minimum
# code needed to install and manage the package.

# S. Socolofsky, Texas A&M University, June 2025, <socolofs@tamu.edu>

project(
    'ocf_tools',
    version: '0.1.0',   # Keep up-to-date with pyproject.toml
    license: 'MIT',
    meson_version: '>= 1.5.0',
    default_options: [
        'buildtype=debugoptimized',
        'b_ndebug=if-release',
        'c_std=c17',
        'warning_level=1',
    ],
)

# Get the Python command
py3 = import('python').find_installation(pure: false)
py3_dep = py3.dependency()

# Set a variable to hold the minimum Numpy version 
min_numpy_version = '1.25.2'   # keep in sync with pyproject.toml

# Emit a warning for 32-bit Python installs on Windows as this many not work
is_windows = host_machine.system() == 'windows'
if is_windows and py3.has_variable('EXT_SUFFIX')
    ext_suffix = py3.get_variable('EXT_SUFFIX')
    if ext_suffix.contains('win32')
        warning('You are building from source on a 32-bit Python install. This is untested; install 64-bit Python if you are having issues!')
    endif
endif

# Initialize a variable to hold the configuration data
conf_data = configuration_data()

# Add the machines
machines = {
    'HOST': host_machine,
    'BUILD': build_machine,
}

# Machines CPU and system information
foreach name, machine : machines
    conf_data.set(name + '_CPU', machine.cpu())
    conf_data.set(name + '_CPU_FAMILY', machine.cpu_family())
    conf_data.set(name + '_CPU_ENDIAN', machine.endian())
    conf_data.set(name + '_CPU_SYSTEM', machine.system())
endforeach

conf_data.set('CROSS_COMPILED', meson.is_cross_build())

# Python information
conf_data.set('PYTHON_PATH', py3.full_path())
conf_data.set('PYTHON_VERSION', py3.language_version())

# Install the pure Python parts of this package
# Get the directory where ocf_tools will be installed
ocftools_dir = py3.get_install_dir() / 'ocf_tools'

# Write the configuration data to __config__.py
configure_file(
  input: '__config__.py.in',
  output: '__config__.py',
  configuration : conf_data,
  install_dir: ocftools_dir,
  install_tag: 'python-runtime',
)

subdir('ocf_tools')
