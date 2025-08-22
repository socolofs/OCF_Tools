============================
OCF_Tools Installation Guide
============================

.. contents::

OCF_Tools is a Python package for making typical calculations in open-channel hydraulics and engineering.  This is a pure-python package that should install easily on Mac OS, Windows, or Linux given the correct dependencies.  This page describes the steps to install the OCF_Tools package in a virtual Python environment that contains the required Python version and dependences.  

.. _requirements:

Requirements
============

The OCF_Tools package requires the following Python packages.  These should be installed from the `conda_forge` channel repository.  For instructions on installing these packages using the provided `environment.yml` file, see :ref:`Creating a Python Environment virtual-env`, below.  

The current Python dependencies and a brief description of their purpose or use is as follows:

* python 3.11 or higher.  Older version of Python are not compatible with the 
  new install methods that use `pyproject.toml` and the present implementation
  using Meson through `meson.build`.
  
* meson 1.5.0 or higher.  Handles package installation.

* meson-python 0.15.0 or higher.  Handles package installation.

* ninja.  Allows for editable installs.

* pkg-config.  Part of the package installation requirements.
  
* pytest.  Needed to run package tests.

* numpy 1.25.2 or higher.  Allows for matrix and array operations.

* scipy 1.13.0 or higher.  Allows for numerical solutions to diverse problems,
  including root-finding to find critical and normal depths in
  non-rectangualar channels and solving differential equations to obtain
  backwater curves.

* matplotlib.  Needed for plotting.

* pandas.  Used to open Excel files.

* openpyxl.  Used with `pandas` to open Excel files.

To create a convenient development environment, the following options packages are also recommended:

* ipython.  Provides a command-line interface to Python.

* spyder.  This is a full-featured integrated development environment (IDE).

* jupyterlab.  This is a modern interface that allows enhanced text 
  documentation together with Python code excerpts

Install Instructions
====================

Because this is a simple Python package, the following installation instructions should work on Mac OS, Windows, and Linux.

Installing Conda
----------------

The easiest way to install Python, the above dependencies, and this package is
to use Conda to manage package installation. A lightweight package manager
that is linked to :ref:`conda-forge https://conda-forge.org` is Miniforge. You
can download and install Miniforge from the :ref:`Miniforge Release
https://conda-forge.org/miniforge/` page. Choose a stable release for your
computer's operating system and architecture. To be on the safe side, reboot
your machine after installation.

To use Miniforge, you need to open a terminal window:

* **Windows.** On Windows, go to the `Start` menu and search for the Miniforge Prompt.  This should open a terminal window.

* **Mac OS.** On Mac OS, you can open the native terminal app, which is found in the `Applications/utilities` directory.  You may also optionally install :ref:`iTerm2 https://iterm2.com`, a more full-featured terminal for Mac OS.

* **Linux.** Like Mac OS, the terminal is a native application on Linux machines.  It is full-featured and should work as described below.

Once you open an appropriate terminal window, you should see a command prompt with the text ``(base)`` included.  This means that the window has opened in the base conda environment.  If this term is not displayed, your terminal may not have found the Miniforge installation.  Test your installation with::

   conda config --show channels

If `conda` is installed, this should list your current channels.  If not, you need to find the appropriate terminal window that is linked to Miniforge.  See the steps above to try to debug your situation.  

Once the `conda` command is working, if `conda-forge` is listed first, then you are all set to continue.  If not, make `conda-forge` the default channel using::

   conda config --add channels conda-forge

Recheck your channels with the ``--show channels`` command.  Everything should be set up correctly now.

We will avoid installing anything in the ``(base)`` conda environment.  Instead, we will use a virtual environment, as described in the next section.

.. _virtual-env:

Creating a Python Environment
-----------------------------

OCF_Tools is distributed with an ``environment.yml`` file that will auto-install of the required and optional packages listed in the :ref:`Requirements requirements` section.  To do this, navigate in your terminal window to the base directory of OCF_Tools, where the ``environment.yml`` file is located.  From that position, use the conda command::

   conda create -n <my-env> -f environment.yml

where ``<my-env>`` is a name you want to assign to your new virtual environment.  The default is ``ocf_tools``, but any name will work.  Follow the on-screem prompts.  After everything has installed, activate the environment using::

   conda activate <my-env>

This should change the prompt so that the text ``(base)`` is replaced with ``(<my-env>)``.  You will need to execute this command every time you want to use OCF_Tools since we will install the package in this virtual environment.  

If you have several existing virtual environments on your machine and you are using the Spyder IDE, you will need to make sure Spyder is using this virtual environment.  You can open the ``Spyder`` -> ``Python`` -> ``Preferences`` panel, select ``Python interpreter`` and select the radio button to ``Use the following Python interpreter``.  Make sure this points to your virtual environment created above.

Installing OCF_Tools
--------------------

If you want to install this package one time and not make changes to the source code, you can use::

   pip install .

I recommend you instead install an editable version so that you can include your own changes and enhancements to the package.  To do this, you should use::

   pip install --no-build-isolation --config-settings=builddir=<mydir> --editable .
   
where ``<mydir>>`` is the name of a directory where you would like Meson to build this package.  You may use something like ``build`` or ``build-laptop``.  
To check whether everything is installed properly, run the tests.  First, change directory to the ``./test`` directory included with the OCF Tools package.  Then run the command::

   pytest -v

This should launch all of the tests included with the package.  

Documentation
=============

To learn how to use OCF_Tools, you should work through the :ref:`Tutorials ./tutorial/index`.  To see the documentation for each method and function included in the OCF_Tools package, visit the :ref:`API Reference ./reference/index`. 


