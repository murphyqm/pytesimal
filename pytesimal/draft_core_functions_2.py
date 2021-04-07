#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:05:24 2021

@author: maeve

Potentially use the property function to protect core temp variable?
https://docs.python.org/3/library/functions.html#property
"""

import numpy as np

"""
To do:
    - [x] have the core object return a boundary temperature
    - [x] have the core keep track of its own temps and cast these to an array
            - done, have 1D array because if obj doesn't take dr, can't make
            2D array
    - [ ] move latent heat calcs out of core object
    - [ ] don't take mantletemps or dr as arguments
    - [ ] build function to calculate heat extracted in the mantle

"""


class IsothermalEutecticCore:
    """Core class represents and manipulates core temp and latent heat."""

    def __init__(self, temp, melt, outer_r, inner_r, rho, cp, maxlh, lat=0):
        """Create a new core with temperature and latent heat."""
        self.temperature = temp
        self.latent = lat
        self.melting = melt
        self.radius = outer_r
        self.inner_radius = inner_r
        self.density = rho
        self.heatcap = cp
        self.maxlatent = maxlh  # change this to accept core lh and then calc
        self.templist = []
        self.latentlist = []
        self.boundary_temperature = temp

    def __str__(self):
        """Return string."""
        return"Core at {0} K. Latent heat extracted: {1}".format(
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
            print("Freezing!\n***\n***\n***")

    def extract_energy(self, energy_removed):
        """To replace cooling method above."""
        volume_of_core = (4.0/3.0) * np.pi * self.radius**3
        delta_T = - energy_removed/(self.density * self.heatcap * volume_of_core)
        self.temperature = self.temperature + delta_T
        # TODO need to figure out is delta T sign is correct
        self.boundary_temperature = self.temperature # TODO keep track of freezing

    def temperature_array_1D(self):
        """Return temperature history as 1D array."""
        temp_array = np.asarray(self.templist)
        return temp_array  # Can't cast to 3D array unless I take dr as an arg


class EnergyExtractedAcrossCMB:
    """Calculate the energy extracted across the core mantle boundary given the temperature of the mantle."""
    def __init__(self, outer_r, timestep, dr):
        self.radius = outer_r
        self.dt = timestep
        self.dr = dr
        self.area = 4 * np.pi * self.radius

    def __str__(self):
        """Return string."""
        return """Calculate the energy extracted across the core mantle boundary given the temperature of the mantle."""

    def energy_extracted(self, mantle_temperatures, i, k):
        energy = -self.area * k * ((mantle_temperatures[0, i] - mantle_temperatures[1, i]) / self.dr)
        return energy


"""Testing this draft Class"""


# instantiate core object

temp = 2000.0
melt = 1200.0
r = 100.0
rho = 7800.0
cp = 850.0
k = 5.0
maxlh = 4_000_000_000_000_000.0


core1 = IsothermalEutecticCore(temp, melt, r, 0, rho, cp, maxlh, lat=0)
core2 = IsothermalEutecticCore(temp, melt, r, 0, rho, cp, maxlh, lat=0)
print(core1)

# set up a mantle array
dt = 1
dr = 1.0

max_t = 35000.0

radii = np.arange(100.0, 200.0, dr)
times = np.arange(0, max_t, dt)

temperatures = np.zeros((radii.size, times.size))  # shape: (100, 10000)
temperatures2 = np.zeros((radii.size, times.size))  # shape: (100, 10000)


# Give the mantle a pretend cooling history (interactive in real application):


temp_init = 2000.0
dT = max_t/50000.0
print(dT)

for j in range(0, times.size):
    for i in range(radii.size-1, 0, -1):
        temperatures[i, j] = temp_init
        temperatures2[i, j] = temp_init
        temp_init = temp_init - dT
        # print(temp_init)

print(temperatures[-1, :])

# make the core cool:

for i in range(0, times.size, dt):
    core1.cooling(temperatures, dt, dr, i, k)
    print(core1)
    temperatures[-1, i] = core1.boundary_temperature  # getting this right is
# an issue for the mantle, not really the problem of the core object

print(temperatures[-1, :])

# making it do it with the extract heat version

# first need to set up core energy budget
cmb_energy = EnergyExtractedAcrossCMB(r, dt, dr)

for i in range(0, times.size, dt):
    E = cmb_energy.energy_extracted(temperatures2, i, k)
    core2.extract_energy(E)
    print(core2)
    temperatures2[-1, i] = core2.boundary_temperature


assert temperatures[-1, :].all() == temperatures2[-1, :].all()  # TODO figure out why this assert statement isn't working

np.testing.assert_array_almost_equal(temperatures[-1, :], temperatures2[-1, :])  # ok, this one works