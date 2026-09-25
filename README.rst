===========================================================
ocf_tools - Computational Tools for Open-Channel Hydraulics
===========================================================

`ocf_tools` is a Python package to compute functions and numerical solutions
relevant to ocean channel hydraulics. This package has been developed through
solving problems in Sturm, "Open Channel Hydraulics," Third Edition, McGraw
Hill: New York, 2021. The Sturm (2021) textbook comes with a Matlab package
for making open channel hydraulics calculations. The present Python package
was created to perform similar calculations, but without consultation of any
of the Matlab code. Any similarities between this package and the Sturm Matlab
package are due to either the limited options for solving similar equations
and/or to an attempt to produce similarly formatted output. Any errors in this
Python package are solely the responsibility of the present author and should
not be attributed to Terry Sturm or McGraw Hill.

Version 0.1.0:  This is the first release of `ocf_tools` with the Meson build 
   utilities. The package contents have not yet been fully verified. Hence,
   this is not a production build.

Requirements
============

All packages should be installed with `conda-forge` as the primary channel for obtaining packages.  Using Miniconda, you can set `conda-forge` as your default channel using::

   >>> conda config --add channels conda-forge 

You can verify that `conda-forge` is the top-level channel using::

   >>> conda config --show channels
   
The `conda-forge` channel should be listed at the top of the list

This package requires:

* python 3.11 or higher.  Older version of Python are not compatible with the 
  new install methods that use `pyproject.toml` and the present implementation
  using Meson through `meson.build`.
  
* meson 1.5.0 or higher.  Handles package installation

* meson-python 0.15.0 or higher.  Handles package installation

* ninja.  Allows for editable installs

* pkg-config.  Part of the package installation requirements
  
* pytest.  Needed to run package tests

* numpy 1.25.2 or higher.  Allows for matrix and array operations

* scipy 1.13.0 or higher.  Allows for numerical solutions to diverse problems

* matplotlib.  Needed for plotting

* pandas.  Used to open Excel files

* openpyxl.  Used with `pandas` to open Excel files

To create a convenient development environment, the following options packages are also recommended:

* ipython.  Provides a command-line interface to Python

* spyder.  This is a full-featured integrated development environment

* jupyterlab.  This is a modern interface that allows enhanced text documentation together with Python code excerpts

Quick Start 
===========

This is a very simple Python package that should install directly.  From a miniconda command prompt at the root directory of the package where this file is stored, create a conda environment for use with this package::

   >>> conda env create -n <env_name> --file conda_requirements.txt

where `-n <env_name>` is optional and `<env_name>` is the name you want to 
assign to this virtual Python environment.  Once you create the environment, 
you will always have to activate it to use it::

   >>> conda activate <env_name>

where `<env_name>` is the name assigned above or the default name, 
`ocf_tools`.  

Within the activate conda Python environment, install `ocf_tools` by issuing
the following command from a command prompt at the root directory of the
package where this README.rst file is stored::

   >>> pip install .
   
If you prefer to install an editable version of the package, use::

   >>> pip install --editable .
       
where `<mydir>` is the name of the local directory where you want Meson to install some of the source code.  If you will use `ocf_tools` on more than
one computer synchonized to the same cloud directory, set a different `<mydir>` on each computer.  Otherwise, this parameter can be ignored.

To check whether everything is installed properly, run the tests.  First, change directory out of the package directory.  Then run the command::

   >>> pytest -v --pyargs ocf_tools

Documentation
=============

A comprehensive set of web documentation is provided in the `./docs/` directory.  Open the `index.html` file within that directory to access the documentation.

Examples
========

A set of examples scripts implementing various common use-cases for `ocf_tools` is provided in the `./examples/` directory.  See those files for details.  
 
