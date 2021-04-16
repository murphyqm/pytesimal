#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:05:24 2021

@author: maeve

New core object that allows cooling via either mantle temperatures or heat
extracted across CMB.

"""

import numpy as np


class IsothermalEutecticCore:
    """Core class represents and manipulates core temp and latent heat."""

    def __init__(self, temp, melt, outer_r, inner_r, rho, cp, core_latent_heat, lat=0):
        """Create a new core with temperature and latent heat."""
        self.temperature = temp
        self.latent = lat
        self.melting = melt
        self.radius = outer_r
        self.inner_radius = inner_r
        self.density = rho
        self.heatcap = cp
        self.maxlatent = (
                            4.0 / 3.0 * np.pi
                            * (self.radius ** 3)
                            * self.density
                            * core_latent_heat)
        self.templist = [self.temperature, self.temperature]  # TODO explain this
        self.latentlist = []
        self.boundary_temperature = temp

    def __str__(self):
        """Return string."""
        return "Core at {0} K. Latent heat extracted: {1}".format(
            self.temperature, self.latent)

    def cooling(self, mantletemps, timestep, dr, i, cmbk):
        """Cool core or extract latent heat. Old version."""
        if (self.temperature > self.melting) or (self.latent >= self.maxlatent):
            # print(self.temperature)
            self.temperature = self.temperature - (
                    3.0
                    * cmbk
                    * ((mantletemps[0, i] - mantletemps[1, i]) / dr)
                    * timestep) / (self.density * self.heatcap * self.radius)
            self.templist.append(self.temperature)
            self.boundary_temperature = self.temperature
        else:
            self.latent = (
                    self.latent
                    + (4.0 * np.pi * self.radius ** 2)
                    * cmbk
                    * ((mantletemps[0, i] - mantletemps[1, i]) / dr)
                    * timestep)
            self.latentlist.append(self.latent)
            self.templist.append(self.temperature)
            print("Freezing!\n***\n***\n***")

    def extract_energy(self, energy_removed):
        """E (J) extracted"""
        volume_of_core = (4.0 / 3.0) * np.pi * self.radius ** 3
        if (self.temperature > self.melting) or (self.latent >= self.maxlatent):
            delta_T = - energy_removed / (self.density * self.heatcap * volume_of_core)
            self.temperature = self.temperature - delta_T
            self.templist.append(self.temperature)
            self.boundary_temperature = self.temperature
        else:
            self.latent = self.latent - energy_removed
            self.templist.append(self.temperature)
            self.latentlist.append(self.latent)

    def extract_heat(self, power, timestep):
        """Heat extracted (power) in W over one timestep"""
        volume_of_core = (4.0 / 3.0) * np.pi * self.radius ** 3
        if (self.temperature > self.melting) or (self.latent >= self.maxlatent):
            delta_T = - (power * timestep) / (self.density * self.heatcap * volume_of_core)
            self.temperature = self.temperature - delta_T
            self.templist.append(self.temperature)
            self.boundary_temperature = self.temperature
        else:
            self.latent = self.latent - (power * timestep)
            self.latentlist.append(self.latent)
            self.templist.append(self.temperature)

    def temperature_array_1D(self):
        """Return temperature history as 1D array."""
        temp_array = np.asarray(self.templist)
        return temp_array

    def temperature_array_3D(self, coretemp_array):
        """Return temperature history as 3D array."""
        # temp_array = np.asarray(self.templist)
        for i in range(1, len(self.templist[1:])):
        # for i in range(1, coretemp_array[0].size):
            coretemp_array[:, i] = self.templist[i]
        return coretemp_array


