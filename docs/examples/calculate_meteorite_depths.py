#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse Results
===============

This example builds on the *Quick Start* example, then demonstrates some of the
functions in the `analysis` module by calculating the depth of formation of
two pallasite meteorites.

"""

# %%
# Producing output data (see "Quick Start" example for more information

import pytesimal.load_plot_save
import pytesimal.quick_workflow
import pytesimal.analysis

# Define a filepath and filename for the parameter file:
folderpath = 'example_default/'
filename = 'example_parameters'
filepath = f'{folderpath}{filename}.txt'

# Save a default parameters file to the filepath:
pytesimal.load_plot_save.make_default_param_file(filepath)

# Load the default parameter file:
pytesimal.quick_workflow.workflow(filename, folderpath)

# %%
# Now that results have been saved, we can load these in to analyse and plot:

filepath = 'example_default/example_parameters_results.npz'
(temperatures,
 coretemp,
 dT_by_dt,
 dT_by_dt_core) = pytesimal.load_plot_save.read_datafile(filepath)

# %%
# Now we can use the `pytesimal.analysis` module to find out more
# about the model run.
# We can check when the core was freezing,
# so we can compare this to the cooling history of meteorites
# and see whether they can be expected to record magnetic remnants
# of a core dynamo:

# (core_frozen,
#  times_frozen,
#  time_core_frozen,
#  fully_frozen) = pytesimal.analysis.core_freezing(coretemp,
#                                         max_time,
#                                         times,
#                                         latent,
#                                         temp_core_melting,
#                                         timestep)