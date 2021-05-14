#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create and track the temperature in the planetesimal core.

This module allows the user to track the temperature of a simple isothermal
eutectic core and calculate the change in temperature in the core over a
timestep based on the heat extracted across the core-mantle boundary.

The class `IsothermalEutecticCore` allows a core object to be instantiated.
This core object keeps track of its temperature as it cools, and this
temperature history can be called at any time in the form of a 1D timeseries
or cast across the core radius (as the core is isothermal).

Classes:
    IsothermalEutecticCore

Notes
-----

The core object can be replaced with a more complex core that interacts with
the mantle in the same way (by extracting energy in Watts across the CMB over
a timestep and providing a resulting boundary temperature).

"""

import numpy as np


class IsothermalEutecticCore:
    """
    Core class  to represent and manipulate core temperature and latent heat.

    Attributes
    ----------
    initial_temperature : float
        Initial uniform temperature of the core
    melting_temperature : float
        Temperature at which core crystallisation initiates
    outer_r : float
        Outer core radius
    inner_r : float
        Inner core radius, not used by this simple implementation of the core
        (set to zero), but included so that more complex core models can be
        coupled to the mantle discretisation function
    rho : float
        Core density
    cp : float
        Core heat capacity
    core_latent_heat : float
        Latent heat of crystallisation of the core, used to calculate time for
        core to solidify fully
    lat : float, optional
        Tracks latent heat of core, always initially zero in current
        implementation but included for forward compatibility with a coupled
        model where core has already cooled by some degree

    """

    def __init__(
        self,
        initial_temperature,
        melting_temperature,
        outer_r,
        inner_r,
        rho,
        cp,
        core_latent_heat,
        lat=0,
    ):
        """Create a new core with temperature and latent heat."""
        self.temperature = initial_temperature
        self.latent = lat
        self.melting = melting_temperature
        self.radius = outer_r
        self.inner_radius = inner_r
        self.density = rho
        self.heatcap = cp
        self.maxlatent = (
            4.0
            / 3.0
            * np.pi
            * (self.radius ** 3)
            * self.density
            * core_latent_heat
        )
        self.templist = [
            self.temperature,
            self.temperature,
        ]  # core temp not evaluated at first time-step so initial temp used
        self.latentlist = []
        self.boundary_temperature = initial_temperature

    def __str__(self):
        """Return string."""
        return "Core at {0} K. Latent heat extracted: {1}".format(
            self.temperature, self.latent
        )

    def extract_heat(self, power, timestep):
        """
        Extract heat (in W) across the core-mantle boundary

        Given power (W) and timestep (s), update the `boundary_temperature` and
        `temperature` to reflect the associated cooling. If `temperature` is
        equal or less than the melting temperature of the core material, then
        the core begins to freeze and `temperature` does not change. Instead,
        latent heat is tracked (`latent`). Once `latent` is greater or equal
        to the maximum latent heat of the core, the core is fully frozen and
        begins to cool again as before.

        Parameters
        ----------
        power : float
            Heat extracted across the CMB in Watts
        timestep : float
            The time over which the heat is extracted (in s)

        """
        volume_of_core = (4.0 / 3.0) * np.pi * self.radius ** 3
        if (self.temperature > self.melting) or (
            self.latent >= self.maxlatent
        ):
            delta_T = -(power * timestep) / (
                self.density * self.heatcap * volume_of_core
            )
            self.temperature = self.temperature - delta_T
            self.templist.append(self.temperature)
            self.boundary_temperature = self.temperature
        else:
            self.latent = self.latent - (power * timestep)
            self.latentlist.append(self.latent)
            self.templist.append(self.temperature)

    def temperature_array_1D(self):
        """
        Return a time-series of core boundary temperatures

        Returns
        -------
        temp_array : numpy.ndarray
            Time series of `boundary_temperature`

        """
        temp_array = np.asarray(self.templist)
        return temp_array

    def temperature_array_2D(self, coretemp_array):
        """
        Cast the core boundary temperatures to an array of radii in time

        Parameters
        ----------
        coretemp_array : numpy.ndarray
            Array of zeros to be filled wth core temperature history

        Returns
        -------
        coretemp_array : numpy.ndarray
            Array of core temperature history

        """
        for i in range(1, len(self.templist[1:])):
            coretemp_array[:, i] = self.templist[i]
        return coretemp_array
