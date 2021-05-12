Parameter Files
==============

The `pytesimal.load_plot_save` module contains a number of functions to help you build, load and save
parameter files. These files allow you to set and record the values of different variables, making
reproducible research easier. This section gives an overview of the different inputs and how to use
these functions, while documentation for each of the individual functions is available in the API
documentation section.

Making and loading input parameter files
----------------------------------------

The `make_default_param_file()` function quickly generates a `json` format file loaded with a set
of default variable values (that recreate the constant properties result from Murphy Quinlan et
al., 2021):

    folder = 'path/to/folder'
    filename = 'example_param_file.txt'
    filepath=f'{folder}/{filename}'

    check_folder_exists(folder)
    make_default_param_file(filepath=filepath)

The `check_folder_exists()` function does what it says on the tin, then will create the folder
if one does not exist.
The `filepath` needs to include the absolute path to the folder, as wel as the filename
including `.txt` file extension.
This parameters file in `json` format can then be opened, edited, renamed or
moved, and loaded in to set parameter values for a model run.

The file content looks like a Python dictionary:

    {
    "run_ID": "example_default",
    "folder": "example_default",
    "timestep": 100000000000.0,
    "r_planet": 250000.0,
    "core_size_factor": 0.5,
    "reg_fraction": 0.032,
    "max_time": 400,
    "temp_core_melting": 1200.0,
    "mantle_heat_cap_value": 819.0,
    "mantle_density_value": 3341.0,
    "mantle_conductivity_value": 3.0,
    "core_cp": 850.0,
    "core_density": 7800.0,
    "temp_init": 1600.0,
    "temp_surface": 250.0,
    "core_temp_init": 1600.0,
    "core_latent_heat": 270000.0,
    "kappa_reg": 5e-08,
    "dr": 1000.0,
    "cond_constant": "y",
    "density_constant": "y",
    "heat_cap_constant": "y"
    }

A description of each of these parameters is given in the docstring of `save_params_and_results`,
but we'll look at a few of them here.

- `run_ID`: this is a string identifier for your model run, for your reference (set it to something
  short and descriptive)
  
- `folder`: this should be the absolute path to the folder where you want the results to be saved (if 
  you are saving results)
  
- `timestep`, `dr` and material properties: make sure you check that your combination of discretisation
  scheme and material properties is stable (see section below on stability); `tiemstep` is in s and
  `dr` is in m.
  
- `max_time`: in Myr, how long the model will run for. 

- `cond_constant`, `density_constant`, `heat_cap_constant`: string values that define whether
  to use constant or temperature-dependent material properties. Feed these parameters in as
  arguments when instantiating the mantle properties.
  
Once you have edited/copied/renamed/moved this file as you wish, it can be loaded in using
the following function call:

    load_params_from_file(filepath)

Where filepath again must be the absolute path to the file, including the filename with
`.txt` extension.

Saving output parameter files
-----------------------------

The `save_params_and_results` function should be called after you have run your model,
to record the parameters used. This output parameter file is formatted so that it can
be read as an input parameter file too, allowing model runs to be reproduced and rerun
exactly. It adds a number of fields to the original input parameter file, in order
to save results:

- `"core_begins_to_freeze": time_core_frozen / myr` - this takes the modelled start time
of the period of core crystallisation (in seconds) and converts it to millions of years
  
- `"core finishes freezing": fully_frozen / myr` - saves the modelled end time of the
period of core crystallisation and converts from seconds to millions of years
  
- `meteorite_results` - optional; this should be formatted
as a dictionary, listing any timing or depth data that should be saved. Extra notes
  can also be added here.
  
- `latent_list_len` - optional; `len(latent)` should be passed in as an argument to
record the length of the latent heat list (to later calculate core crystallisation timing).
  This is also an optional argument for `save_result_arrays`.
  
**Important**: note that depending on the analysis carried out, you may not yet
have results for all of the above. The parameter file can still be saved by substituting
an obvious placeholder string, `0`, or `None` for one of the above values. Make note
of this within the `meteorite_results` or `run_ID` fields.

Numerical Stability
===================

You can check whether your choice of diffusivity, timestep and
radial discretisation meet Von Neumann stability criteria using
the functions provided in the `pytesimal.numerical_methods`
module.

Thermal diffusivity can be calculated from the conductivity,
heat capacity and density using `calculate_diffusivity`, and
then tested using the `check_stability` function. You should
use the maximum diffusivity of your system to find the most
restrictive criteria, and use this to inform your choice
of timestep.

Note that other instabilities may arise when defining custom
functions for thermal properties; please regularly plot the
output data to check for unexpected behaviour.