.. contents::
   :depth: 3
..

Pytesimal
=========

Pytesimal models the conductive cooling of planetesimals with
temperature-dependent material properties.

Pytesimal is a finite difference code to perform numerical models of a
conductively cooling planetesimal, both with constant and
temperature-dependent properties. It returns a thermal history of the
planetesimal, and the estimated timing and depth of pallasite meteorite
genesis. The conduction equation is solved numerically using an explicit
finite difference scheme, FTCS (Forward-Time Central-Space). FTCS gives
first-order convergence in time and second-order in space, and is
conditionally stable when applied to the heat equation. In 1D, it must
satisfy Von Neumann stability analysis - please see `Murphy Quinlan et
al. (2020 -
preprint) <https://www.essoar.org/doi/abs/10.1002/essoar.10504913.1>`__
for more information on choice of time-step.

The code currently recreates the cases described in `Murphy Quinlan et
al. (2020 -
preprint) <https://www.essoar.org/doi/abs/10.1002/essoar.10504913.1>`__.
References for the default parameters used can be found therein. We plan
to extend it and make it more modular in future updates.

Quick Start
-----------

|Binder|

To run a case with default parameters:

::

   from modular_cond_cooling import conductive_cooling

   # Give your model set-up a unique file name:
   run_ID = "file_name"

   # Point it to a folder to save the outputs:
   folder = "folder_path" 

   # Let your planetesimal evolve:
   conductive_cooling(run_ID, folder,)

See the Jupyter notebooks provided for working examples.

**To download data from NGDC and plot it:**

Navigate to the ``downloading_and_plotting_data`` directory. From the
command line, run the required script to download the .dat files from
the NGDC:

``$ python downloaddata.py``

Once the data is downloaded from the NGDC, it is available to plot using
``coolingplot.py`` with the filename you wish to plot:

``$ python coolingplot.py constant_properties.dat``

For more information run:

``$ python coolingplot.py -h``

Features
--------

-  Constant or variable material properties
-  Download and plot data from NGDC
-  Choose to return compressed ``.npz`` NumPy arrays of temperature and
   cooling rates through time and radius
-  Plot temperature or cooling rate heatmaps
-  Return timing of core solidification, and depth and timing of
   meteorite formation
-  Return ``pickle`` objects with output parameter values
-  Return a parameter ``.txt`` file with details of input parameters and
   results

Installation
------------

This software relies on python (version 3) and various other python
packages. Examples are distributed as Jupyter notebooks, which need
Jupyter and Matplotlib to run. Installation and management of all these
dependencies is most easily done in a conda environment. Download of the
software and creation of an isolated conda environment can be done by
running:

::

   git clone https://github.com/murphyqm/pytesimal.git
   cd pytesimal
   conda create -n=pytesimal python=3.8
   conda activate pytesimal
   pip install -r requirements.txt

Contribute
----------

-  Issue Tracker: github.com/murphyqm/pytesimal/issues
-  Source Code: github.com/murphyqm/pytesimal

Support
-------

If you are having issues, please let us know. You can email us at
eememq@leeds.ac.uk

License
-------

The project is licensed under the MIT license.

.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/murphyqm/pytesimal/rearranging-folders
