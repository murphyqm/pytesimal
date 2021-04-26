#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forward-Time Central-Space (FTCS) discretisation for the mantle.

Set up boundary conditions, calculate the heat extracted across the core-mantle
boundary in a timestep, and numerically discretise the conductive cooling of
the mantle of a planetesimal. This module also contains functions to calculate
the thermal diffusivity of a material form the thermal conductivity, heat
capacity and the density, and to check whether the diffusivity, timestep and
radial discretisation meet Von Neumann stability criteria.
"""

import numpy as np


def calculate_diffusivity(conductivity, heat_capacity, density):
    """
    Calculate diffusivity from conductivity, heat capacity and density.

    Returns a value for diffusivity at a certain temperature, given float
    values for conductivity, heat capacity and density.

    Parameters
    ----------
    conductivity : float
        Thermal conductivity of the material
    heat_capacity : float
        Heat capacity of the material
    density : float
        Density of the material

    Returns
    -------
    diffusivity : float

    """
    diffusivity = conductivity / (density * heat_capacity)
    return diffusivity


def check_stability(max_diffusivity, timestep, dr):
    """
    Check adherence to Von Neumann stability criteria.

    Use the maximum diffusivity of the system to return the most restrictive
    criteria. Diffusivity can be calculated using the `calculate_diffusivity`
    function, with max diffusivity where conductivity is maximised and
    density and heat capacity are minimised.

    Parameters
    ----------
    max_diffusivity : float
        The highest diffusivity of the system to impose the most restrictive
        conditions
    timestep : float
        The timestep used for the numerical scheme
    dr : float
        The radial step used for the numerical scheme

    Returns
    -------
    result : bool
        Boolean, True if parameters pass stability criteria and false if they
        fail.

    """
    criterion = (max_diffusivity * timestep) / (dr ** 2)
    if criterion <= 0.5:
        print("Von Neumann stability criteria met")
        return True
    if criterion > 0.5:
        print("Reduce timestep to meet Von Neumann stability criteria")
        return False


def surface_dirichlet_bc(temperatures, temp_surface, i):
    """
    Set a fixed temperature boundary condition at the planetesimal's surface.

    Parameters
    ----------
    temperatures : numpy.ndarray
        Numpy array of mantle temperatures to apply condition to
    temp_surface : float
        The temperature at the surface boundary
    i : int
        Index along time axis where condition is to be set

    Returns
    -------
    temperatures : numpy.ndarray
        Temperature array with condition applied

    """
    temperatures[-1, i] = temp_surface
    return temperatures


def cmb_dirichlet_bc(temperatures, core_boundary_temperature, i):
    """
    Set a fixed temperature boundary condition at the base of the mantle.

    Parameters
    ----------
    temperatures : numpy.ndarray
        Numpy array of mantle temperatures to apply condition to
    core_boundary_temperature : float
        The temperature at the core mantle boundary
    i : int
        Index along time axis where condition is to be set

    Returns
    -------
    temperatures : numpy.ndarray
        Temperature array with condition applied
    """
    temperatures[0, i] = core_boundary_temperature
    return temperatures


def cmb_neumann_bc(temperatures, core_boundary_temperature, i):
    """
    Set a fixed flux boundary condition at the base of the mantle

    Note that core radius must be set to zero for this to approximate the
    analytical solution of a conductively cooling sphere or to model an
    undifferentiated meteorite parent body.

    Parameters
    ----------
    temperatures : numpy.ndarray
        Numpy array of mantle temperatures to apply condition to
    core_boundary_temperature : float
        The temperature at the core mantle boundary; this is not used by this
        boundary condition but inclusion allows functions to be easily swapped
    i : int
        Index along time axis where condition is to be set

    Returns
    -------
    temperatures : numpy.ndarray
        Temperature array with condition applied
    """
    temperatures[0, i] = (
        4.0 * (temperatures[1, i]) - temperatures[2, i]
    ) / 3.0
    # eq. 6.31 http://folk.ntnu.no/leifh/teaching/tkt4140/._main056.html
    return temperatures


class EnergyExtractedAcrossCMB:
    """
    Class to calculate the energy extracted across the cmb in one timestep.

    Attributes
    ----------
    outer_r : float
        Core radius
    timestep : float
        Time over which heat is extracted
    radius_step : float
        Radial step for numerical discretisation
    """

    def __init__(self, outer_r, timestep, radius_step):
        self.radius = outer_r
        self.dt = timestep
        self.dr = radius_step
        self.area = 4 * np.pi * self.radius ** 2

    def __str__(self):
        """Return string."""
        return """Calculate the energy extracted across the core mantle boundary given the temperature of the mantle."""

    def energy_extracted(self, mantle_temperatures, i, k):
        """Calculate energy extracted in one timestep"""
        energy = (
            -self.area
            * k
            * (
                (mantle_temperatures[0, i] - mantle_temperatures[1, i])
                / self.dr
            )
            * self.dt
        )
        return energy

    def power(self, mantle_temperatures, i, k):
        """Calculate heat (power) extracted in one timestep"""
        heat = (
            -self.area
            * k
            * (
                (mantle_temperatures[0, i] - mantle_temperatures[1, i])
                / self.dr
            )
        )
        return heat


def discretisation(
    core_values,
    latent,
    temp_init,
    core_temp_init,
    top_mantle_bc,
    bottom_mantle_bc,
    # temp_core_melting,
    temp_surface,
    temperatures,
    dr,
    coretemp_array,
    timestep,
    # core_density,
    # core_cp,
    r_core,
    # core_latent_heat,
    radii,
    times,
    where_regolith,
    kappa_reg,
    cond,
    heatcap,
    dens,
    non_lin_term="y",
):
    """
    Finite difference solver with variable k.

    Uses variable heat capacity, conductivity, density as required.

    Uses diffusivity for regolith layer.

    Parameters
    ----------
    core_values : object
        Core object
    latent : list
        Empty list (unless coupling two models) of latent heat extracted from
        the core
    temp_init : float, numpy.ndarray
        The initial temperature of the mantle with float implying initial
        homogeneous temperature distribution
    core_temp_init : float, numpy.ndarray
        Initial temperature of the core; current core object is isothermal so
        only accepts float but more complex core models could track the
        temperature distribution in the core
    top_mantle_bc : function
        Calleable function that defines the boundary condition at the
        planetesimal surface
    bottom_mantle_bc : function
        Calleable function that defines the boundary condition at the base of
        the planetesimal mantle
    temp_surface : float
        Temperature at the surface of the planetesimal
    temperatures : numpy.ndarray
        Numpy array to fill with mantle temperatures
    dr : float
        Radial step for numerical discretisation
    coretemp_array : numpy.ndarray
        Numpy array to fill with core temperatures
    timestep : float
        Timestep for numerical discretisation
    r_core : float
        Radius of the core in m
    radii : numpy.ndarray
        Numpy array of radii values in the mantle, with spacing defined by `dr`
    times : numpy.ndarray
        Numpy array of time values in s, up to the maximum time, with spacing
        controlled by `timestep`
    where_regolith : numpy.ndarray
        Boolean array recording presence of regolith
    kappa_reg : float
        Constant diffusivity of the regolith
    cond : function, method
        Function or method that defines the mantle conductivity
    heatcap : function, method
        Function or method that defines the mantle heat capacity
    dens : function, method
        Function or method that defines the mantle density
    non_lin_term : str, default `'y'`
        Flag to switch off the non-linear term when temperature-dependent
        conductivity is being used


    Returns
    -------

    """

    temperatures[:, 0] = temp_init  # this can be an array or a scalar
    core_boundary_temperature = core_temp_init
    coretemp_array[:, 0] = core_temp_init
    cmb_energy = EnergyExtractedAcrossCMB(r_core, timestep, dr)

    for i in range(1, len(times[1:]) + 1):

        for j in range(1, len(radii[1:-1]) + 1):

            A_1 = []
            B_1 = []
            C_1 = []

            if where_regolith[j] == 1:
                # check for non-linear term
                if non_lin_term == "y":
                    A_1 = (
                        timestep
                        * (
                            1.0
                            / (
                                dens.getrho(temperatures[j, i - 1])
                                * heatcap.getcp(temperatures[j, i - 1])
                            )
                        )
                    ) * (
                        cond.getdkdT(temperatures[j, i - 1])
                        * (
                            (
                                temperatures[j + 1, i - 1]
                                - temperatures[j - 1, i - 1]
                            )
                            ** 2
                        )
                        / (4.0 * dr ** 2.0)
                    )
                else:
                    A_1 = 0

                B_1 = (
                    timestep
                    * (
                        1.0
                        / (
                            dens.getrho(temperatures[j, i - 1])
                            * heatcap.getcp(temperatures[j, i - 1])
                        )
                    )
                ) * (
                    (cond.getk(temperatures[j, i - 1]) / (radii[j] * dr))
                    * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
                )

                C_1 = (
                    timestep
                    * (
                        1.0
                        / (
                            dens.getrho(temperatures[j, i - 1])
                            * heatcap.getcp(temperatures[j, i - 1])
                        )
                    )
                ) * (
                    (cond.getk(temperatures[j, i - 1]) / dr ** 2.0)
                    * (
                        temperatures[j + 1, i - 1]
                        - 2 * temperatures[j, i - 1]
                        + temperatures[j - 1, i - 1]
                    )
                )
                temperatures[j, i] = temperatures[j, i - 1] + A_1 + B_1 + C_1

            elif where_regolith[j] == 0:

                A_1 = 0  # non-linear term
                B_1 = (timestep) * (
                    (kappa_reg / (radii[j] * dr))
                    * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
                )
                C_1 = (timestep) * (
                    (kappa_reg / dr ** 2.0)
                    * (
                        temperatures[j + 1, i - 1]
                        - 2 * temperatures[j, i - 1]
                        + temperatures[j - 1, i - 1]
                    )
                )

                temperatures[j, i] = temperatures[j, i - 1] + A_1 + B_1 + C_1

        # top boundary condition
        temperatures = top_mantle_bc(temperatures, temp_surface, i)

        # bottom boundary condition
        temperatures = bottom_mantle_bc(
            temperatures, core_boundary_temperature, i
        )

        # Allow core to cool
        cmb_conductivity = cond.getk(temperatures[0, i])
        power = cmb_energy.power(temperatures, i, cmb_conductivity)
        core_values.extract_heat(power, timestep)
        latent = core_values.latentlist
        core_boundary_temperature = core_values.temperature
    coretemp_array = core_values.temperature_array_2D(coretemp_array)
    return (
        temperatures,
        coretemp_array,
        latent,
    )
