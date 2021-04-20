#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modifying mantle timestepping function to take new core object and calculate energy extracted
Created on Thu Apr 8 16:24:52 2021.

@author: maeve

to do: need to move temp array set up outside of the discretisation function.
"""

import numpy as np


def surface_dirichlet_bc(temperatures, temp_surface, i):
    temperatures[-1, i] = temp_surface
    return temperatures


def cmb_dirichlet_bc(temperatures, core_boundary_temperature, i):
    temperatures[0, i] = core_boundary_temperature
    return temperatures


def cmb_neumann_bc(temperatures, core_boundary_temperature, i):
    temperatures[0, i] = (4.0 * (temperatures[1, i]) - temperatures[2, i]) / 3.0
    # eq. 6.31 http://folk.ntnu.no/leifh/teaching/tkt4140/._main056.html


class EnergyExtractedAcrossCMB:
    """Calculate the energy extracted across the cmb in one timestep given the temperature of the mantle."""

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
            temperatures, core_boundary_temperature, i)

        # Allow core to cool
        cmb_conductivity = cond.getk(temperatures[0, i])
        power = cmb_energy.power(temperatures, i, cmb_conductivity)
        core_values.extract_heat(power, timestep)
        latent = core_values.latentlist
        core_boundary_temperature = core_values.temperature
    coretemp_array = core_values.temperature_array_3D(coretemp_array)
    return (
        temperatures,
        coretemp_array,
        latent,
    )
