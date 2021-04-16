#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:05:24 2021

@author: maeve

New core object that allows cooling via either mantle temperatures or heat
extracted across CMB.


"""

import numpy as np
import cProfile
import timeit

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
        """Return temperature history as 1D array."""
        # temp_array = np.asarray(self.templist)
        for i in range(1, len(self.templist[1:])):
        # for i in range(1, coretemp_array[0].size):
            coretemp_array[:, i] = self.templist[i]
        return coretemp_array


class EnergyExtractedAcrossCMB:
    """Calculate the energy extracted across the cmb in one timestep given the temperature of the mantle."""
    def __init__(self, outer_r, timestep, radius_step):
        self.radius = outer_r
        self.dt = timestep
        self.dr = radius_step
        self.area = 4 * np.pi * self.radius**2

    def __str__(self):
        """Return string."""
        return """Calculate the energy extracted across the core mantle boundary given the temperature of the mantle."""

    def energy_extracted(self, mantle_temperatures, i, k):
        """Calculate energy extracted in one timestep"""
        energy = -self.area * k * (
                (mantle_temperatures[0, i] - mantle_temperatures[1, i])
                / self.dr) * self.dt
        return energy

    def power(self, mantle_temperatures, i, k):
        """Calculate heat (power) extracted in one timestep"""
        heat = -self.area * k * (
                (mantle_temperatures[0, i] - mantle_temperatures[1, i])
                / self.dr)
        return heat



"""Testing this draft Class - just while developing, have formal tests also"""

# # instantiate core object
#
# temp = 2000.0
# melt = 1200.0
# r = 100.0
# rho = 7800.0
# cp = 850.0
# k = 5.0
# maxlh = 4_000_000_000_000_000.0
#
# core1 = IsothermalEutecticCore(temp, melt, r, 0, rho, cp, maxlh, lat=0)
# core2 = IsothermalEutecticCore(temp, melt, r, 0, rho, cp, maxlh, lat=0)
# print(core1)
#
# # set up a mantle array
# dt = 1
# dr = 1.0
#
# max_t = 35000.0
#
# radii = np.arange(100.0, 200.0, dr)
# times = np.arange(0, max_t, dt)
#
# temperatures = np.zeros((radii.size, times.size))  # shape: (100, 10000)
# temperatures2 = np.zeros((radii.size, times.size))  # shape: (100, 10000)
#
# # Give the mantle a pretend cooling history (interactive in real application):
#
#
# temp_init = 2000.0
# dT = max_t / 50000.0
# print(dT)
#
# for j in range(0, times.size):
#     for i in range(radii.size - 1, 0, -1):
#         temperatures[i, j] = temp_init
#         temperatures2[i, j] = temp_init
#         temp_init = temp_init - dT
#         # print(temp_init)
#
# print(temperatures[-1, :])
#
# # make the core cool:
#
# for i in range(0, times.size, dt):
#     core1.cooling(temperatures, dt, dr, i, k)
#     print(core1)
#     temperatures[-1, i] = core1.boundary_temperature  # getting this right is
# # an issue for the mantle, not really the problem of the core object
#
# print(temperatures[-1, :])
#
# # making it do it with the extract heat version
#
# # first need to set up core energy budget
# cmb_energy = EnergyExtractedAcrossCMB(r, dt, dr)
#
# for i in range(0, times.size, dt):
#     E = cmb_energy.energy_extracted(temperatures2, i, k)
#     core2.extract_energy(E)
#     print(core2)
#     temperatures2[-1, i] = core2.boundary_temperature
#
# np.testing.assert_array_almost_equal_nulp(temperatures[-1, :], temperatures2[-1, :])
#
# # make these into functions to help profile them:
#
#
# def core_cool_old():
#     for i in range(0, times.size, dt):
#         core1.cooling(temperatures, dt, dr, i, k)
#         print(core1)
#         temperatures[-1, i] = core1.boundary_temperature
#     return temperatures
#
#
# def core_cool_new():
#     cmb_energy1 = EnergyExtractedAcrossCMB(r, dt, dr)
#
#     for i in range(0, times.size, dt):
#         E1 = cmb_energy1.energy_extracted(temperatures2, i, k)
#         core2.extract_energy(E1)
#         print(core2)
#         temperatures2[-1, i] = core2.boundary_temperature
#
#
# # resetting the initial conditions
#
# temperatures = np.zeros((radii.size, times.size))  # shape: (100, 10000)
# temperatures2 = np.zeros((radii.size, times.size))  # shape: (100, 10000)
#
# # Give the mantle a pretend cooling history (interactive in real application):
#
#
# temp_init = 2000.0
# dT = max_t / 50000.0
# print(dT)
#
# for j in range(0, times.size):
#     for i in range(radii.size - 1, 0, -1):
#         temperatures[i, j] = temp_init
#         temperatures2[i, j] = temp_init
#         temp_init = temp_init - dT
#         # print(temp_init)
#
# # %timeit core_cool_old()
# # cProfile.run("core_cool_old()")

"""
core_cool_old:

1.56 s ± 19.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
1.52 s ± 28.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

core_cool_new:

1.53 s ± 40.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
1.55 s ± 20.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
"""