.. Pytesimal documentation master file, created by
   sphinx-quickstart on Tue Feb  9 12:03:40 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   self
   README
   ../examples/index
   apiref

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
al. (2021) <https://doi.org/10.1029/2020JE006726>`__ for more
information on choice of time-step.

The code currently recreates the cases described in `Murphy Quinlan et
al. (2021) <https://doi.org/10.1029/2020JE006726>`__. References for the
default parameters used can be found therein. We plan to extend it and
make it more modular in future updates.

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/murphyqm/pytesimal/HEAD


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
