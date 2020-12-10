Pytesimal
========

Pytesimal models the conductive cooling of planetesimals with temperature-dependent material properties.

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
