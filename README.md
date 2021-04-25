Pytesimal
========

[![Documentation Status](https://readthedocs.org/projects/pytesimal/badge/?version=latest)](https://pytesimal.readthedocs.io/en/latest/?badge=latest)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/murphyqm/pytesimal/rearranging-folders)

Pytesimal models the conductive cooling of planetesimals with temperature-dependent material properties.

Pytesimal is a finite difference code to perform numerical models of a conductively cooling planetesimal, both with constant and temperature-dependent properties. It returns a thermal history of the planetesimal, and the estimated timing and depth of pallasite meteorite genesis.
The conduction equation is solved numerically using an explicit finite difference scheme, FTCS (Forward-Time Central-Space). FTCS gives first-order convergence in time and second-order in space, and is conditionally stable when applied to the heat equation.
In 1D, it must satisfy Von Neumann stability analysis - please see [Murphy Quinlan et al. (2021)](https://doi.org/10.1029/2020JE006726) for more information on choice of time-step.

The code currently recreates the cases described in [Murphy Quinlan et al. (2021)](https://doi.org/10.1029/2020JE006726). References for the default parameters used can be found therein. We plan to extend it and make it more modular in future updates.

Quick Start
-----------
[Read the full documentation here,](https://pytesimal.readthedocs.io/en/latest/pytesimal.html) [or launch a Jupyter Notebook example on Binder here.](https://mybinder.org/v2/gh/murphyqm/pytesimal/rearranging-folders)

To run a case with parameters loaded from file:

    import pytesimal.load_plot_save
    import pytesimal.quick_workflow

Define a filepath and filename for the parameter file:

    folderpath = 'path/to/the/example/'
    filename = 'example_parameters'
    filepath = f'{folderpath}{filename}.txt'

Save a default parameters file to the filepath:

    pytesimal.load_plot_save.make_default_param_file(filepath)

You can open this `json` file in a text editor and change the default values. Once you've edited and saved it, use it as an input file for a model run:

    pytesimal.quick_workflow.workflow(filename, folderpath)

Let your planetesimal evolve! This will take a minute or so to run. Once it has done do, you can load the results (from the folder you specified in the parameters file):

    filepath = 'results_folder/example_parameters_results.npz'
    (temperatures,
     coretemp,
     dT_by_dt,
     dT_by_dt_core) = pytesimal.load_plot_save.read_datafile(filepath)

Then you can plot heatmaps of the temperatures and cooling rates within the planetesimal:

    # Specify a figure width and height:
    fig_w = 6
    fig_h = 9
    
    pytesimal.load_plot_save.two_in_one(
    fig_w,
    fig_h,
    temperatures,
    coretemp,
    dT_by_dt,
    dT_by_dt_core)

See the Jupyter notebooks hosted on Binder for live working examples, or download the example scripts provided.

Features
--------

- Constant or variable material properties
- Choose to return compressed `.npz` NumPy arrays of temperature and cooling rates through time and radius
- Plot temperature or cooling rate heatmaps
- Return timing of core solidification, and depth and timing of meteorite formation
- Return a parameter `.json` file with details of input parameters and results

Installation
------------
This software relies on python (version 3) and various other python packages. Examples are distributed as Jupyter notebooks, which need Jupyter and Matplotlib to run. Installation and management of all these dependencies is most easily done in a conda environment. Download of the software and creation of an isolated conda environment can be done by running:


    git clone https://github.com/murphyqm/pytesimal.git
    cd pytesimal
    conda create -n=pytesimal python=3.8 jupyter
    conda activate pytesimal
    pip install -r requirements.txt

Pytesimal can then be installed as a package within the environment by running:

    pip install .

Contribute
----------

- Issue Tracker: github.com/murphyqm/pytesimal/issues
- Source Code: github.com/murphyqm/pytesimal

Support
-------

If you are having issues, please let us know.
You can email us at eememq@leeds.ac.uk

License
-------

The project is licensed under the MIT license.
