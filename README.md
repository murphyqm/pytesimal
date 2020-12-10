Pytesimal
========

Pytesimal models the conductive cooling of planetesimals with temperature-dependent material properties.

Pytesimal is a finite difference code to perform numerical models of a conductively cooling planetesimal, both with constant and temperature-dependent properties. It returns a thermal history of the planetesimal, and the estimated timing and depth of pallasite meteorite genesis.

The code currently recreates the cases described in [Murphy Quinlan et al. (2020 - preprint)](https://www.essoar.org/doi/abs/10.1002/essoar.10504913.1). References for the default parameters used can be found therein. We plan to extend it and make it more modular in future updates.

To run a case with default parameters:

    from modular_cond_cooling import conductive_cooling

    # Give your model set-up a unique file name:
    run_ID = "file_name"

    # Point it to a folder to save the outputs:
    folder = "folder_path" 

    # Let your planetesimal evolve:
    conductive_cooling(run_ID, folder,)

See the Jupyter notebooks provided for working examples.

Features
--------

- Constant or variable material properties
- Download and plot data from NGDC

Installation
------------
This software relies on python (version 3) and various other python packages. Examples are distributed as Jupyter notebooks, which need Jupyter and Matplotlib to run. Installation and management of all these dependencies is most easily done in a conda environment. Download of the software and creation of an isolated conda environment can be done by running:


    git clone https://github.com/murphyqm/pytesimal.git
    cd pytesimal
    conda create -n=pytesimal python=3.8
    conda activate pytesimal
    pip install -r requirements.txt


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
