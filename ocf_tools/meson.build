# This part of the meson.build cycle installs all the required package
# files and scripts

# List all Python source files to include
python_sources = [
    '__init__.py',
    'culvert_tools.py',
    'ocf_tools.py',
    'storage_routing.py',
    'weir_tools.py'
]

test_sources = [
  'test/test_objects.py'
  ]

# Populate if/when data are distributed with the model
#data_sources = [
#]

# Install the Python source files
py3.install_sources(
  python_sources,
  subdir: 'ocf_tools'
)

# Install the package test files
py3.install_sources(
  test_sources,
  subdir: 'ocf_tools/test',
  install_tag: 'tests'
) 

# Install the package data files ... when present
#py3.install_sources(
#    data_sources,
#    subdir: 'ocf_tools/data',
#    install_tag: 'data'
# 



