Pytesimal
========

[![Documentation Status](https://readthedocs.org/projects/pytesimal/badge/?version=latest)](https://pytesimal.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/murphyqm/pytesimal/master?filepath=example-notebooks)
![GitHub](https://img.shields.io/github/license/murphyqm/pytesimal)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/murphyqm/pytesimal)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/murphyqm/pytesimal/Python%20package)
[![Updates](https://pyup.io/repos/github/murphyqm/pytesimal/shield.svg)](https://pyup.io/repos/github/murphyqm/pytesimal/)

Pytesimal models the conductive cooling of planetesimals with temperature-dependent material properties.

Pytesimal is a finite difference code to perform numerical models of a conductively cooling planetesimal, both with constant and temperature-dependent properties. It returns a thermal history of the planetesimal, and contains modules to estimate the timing and depth of pallasite meteorite genesis.

Features
--------

- Constant or variable material properties
- Choose to return compressed `.npz` NumPy arrays of temperature and cooling rates through time and radius
- Plot temperature or cooling rate heatmaps
- Return timing of core solidification, and depth and timing of meteorite formation
- Return a parameter `.json` file with details of input parameters and results

Installation
------------
This software relies on python (version 3.6 and up) and various other python packages. Examples are distributed as Jupyter notebooks, which need Jupyter and Matplotlib to run. Installation and management of all these dependencies is most easily done in a conda environment. 

    conda create -n=pytesimal python=3.8 jupyter
    conda activate pytesimal    
    pip install pytesimal

### Installation for development

The package can be downloaded and installed directly from Github for the most recent version. The software and its dependencies are best installed in a virtual environment of your choice. Download of the software and creation of an isolated conda environment can be done by running:

    git clone https://github.com/murphyqm/pytesimal.git
    cd pytesimal
    conda create -n=pytesimal python=3.8 jupyter
    conda activate pytesimal
    pip install -e .

The `-e` flag installs the package in editable mode so that any changes
to modules can be carried through. 

Getting started
---------------

Open up some examples on [Binder](https://mybinder.org/v2/gh/murphyqm/pytesimal/master?filepath=example-notebooks) or download some examples from our gallery [here](https://pytesimal.readthedocs.io/en/latest/examples/index.html).

Contribute
----------

- Issue Tracker: [github.com/murphyqm/pytesimal/issue](https://github.com/murphyqm/pytesimal/issues)
- Source Code: [github.com/murphyqm/pytesimal](https://github.com/murphyqm/pytesimal)

Support
-------

If you are having issues, please let us know.
You can email us at eememq@leeds.ac.uk

License
-------

The project is licensed under the MIT license.