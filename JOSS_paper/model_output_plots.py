#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 29/04/2021
by murphyqm

"""
import matplotlib.pyplot as plt

# Roundabout import without package installed
from context import setup_functions
from context import load_plot_save
from context import numerical_methods
from context import analysis
from context import core_function
from context import mantle_properties

# the same params as Murphy Quinlan et al., 2021

timestep = 1E11  # s
r_planet = 250_000.0  # m
core_size_factor = 0.5  # fraction of r_planet
reg_fraction = 0.032  # fraction of r_planet
max_time = 400  # Myr
temp_core_melting = 1200.0  # K
core_cp = 850.0  # J/(kg K)
core_density = 7800.0  # kg/m^3
temp_init = 1600.0  # K
temp_surface = 250.0  # K
core_temp_init = 1600.0  # K
core_latent_heat = 270_000.0  # J/kg
kappa_reg = 5e-8  # m^2/s
dr = 1000.0  # m

(r_core,
 radii,
 core_radii,
 reg_thickness,
 where_regolith,
 times,
 mantle_temperature_array,
 core_temperature_array) = setup_functions.set_up(timestep,
                                                            r_planet,
                                                            core_size_factor,
                                                            reg_fraction,
                                                            max_time,
                                                            dr)

# We define an empty list of latent heat that will
# be filled as the core freezes
latent = []

core_values = core_function.IsothermalEutecticCore(
    initial_temperature=core_temp_init,
    melting_temperature=temp_core_melting,
    outer_r=r_core,
    inner_r=0,
    rho=core_density,
    cp=core_cp,
    core_latent_heat=core_latent_heat)

(mantle_conductivity,
 mantle_heatcap,
 mantle_density) = mantle_properties.set_up_mantle_properties(
    cond_constant='n',
    density_constant='n',
    heat_cap_constant='n'
)

top_mantle_bc = numerical_methods.surface_dirichlet_bc
bottom_mantle_bc = numerical_methods.cmb_dirichlet_bc

# Now we let the temperature inside the planestesimal evolve. This is the
# slowest part of the code, because it has to iterate over all radii and
# time.
# This will take a minute or two!
# The mantle property objects are passed in in the same way as in the
# example with constant thermal properties.

(mantle_temperature_array,
 core_temperature_array,
 latent,
 ) = numerical_methods.discretisation(
    core_values,
    latent,
    temp_init,
    core_temp_init,
    top_mantle_bc,
    bottom_mantle_bc,
    temp_surface,
    mantle_temperature_array,
    dr,
    core_temperature_array,
    timestep,
    r_core,
    radii,
    times,
    where_regolith,
    kappa_reg,
    mantle_conductivity,
    mantle_heatcap,
    mantle_density)

(core_frozen,
 times_frozen,
 time_core_frozen,
 fully_frozen) = analysis.core_freezing(core_temperature_array,
                                                  max_time,
                                                  times,
                                                  latent,
                                                  temp_core_melting,
                                                  timestep)

mantle_cooling_rates = analysis.cooling_rate(mantle_temperature_array,
                                                       timestep)
core_cooling_rates = analysis.cooling_rate(core_temperature_array,
                                                     timestep)

fig_w = 6
fig_h = 9

fig, axs = plt.subplots(2, 1, figsize=(fig_w, fig_h), sharey=True)
ax, ax2 = axs

# These probably belong in the data files...
timestep = 1e11
maxtime = 400 * 3.1556926e13 # TODO - move this to argument

fig, ax = load_plot_save.plot_temperature_history(
    mantle_temperature_array,
    core_temperature_array,
    timestep,
    maxtime,
    ax=ax,
    fig=fig,
    savefile=None,
    show=False,
)

fig, ax2 = load_plot_save.plot_coolingrate_history(
    mantle_cooling_rates,
    core_cooling_rates,
    timestep,
    maxtime,
    ax=ax2,
    fig=fig,
    savefile=None,
    show=False,
)


# plt.savefig('heatmap.pdf', dpi=300, bbox_inches="tight")
plt.show()