#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:05:24 2021

@author: maeve

Potentially use the property function to protect core temp variable?
https://docs.python.org/3/library/functions.html#property
"""

import numpy as np


class Core:
    """Core class represents and manipulates core temp and latent heat."""

    def __init__(self, temp, melt, r, rho, cp, maxlh, lat=0):
        """Create a new core with temperature and latent heat."""
        self.temperature = temp
        self.latent = lat
        self.melting = melt
        self.radius = r
        self.density = rho
        self.heatcap = cp
        self.maxlatent = maxlh  # change this to accept core lh and then calc
        self.templist = []
        self.latentlist = []

    def __str__(self):
        """Return string."""
        return"Core at {0} K. Latent heat extracted: {1}".format(
            self.temperature, self.latent)

    def cool(self):
        """Test cooling method."""
        self.temperature -= 100.0
        self.latent += 10.0

    def cooling(self, mantletemps, timestep, dr, i, cmbk):
        """Cool core or extract latent heat."""
        if (self.temperature > self.melting) or (self.latent >= self.maxlatent):
            # print(self.temperature)
            self.temperature = self.temperature - (
                3.0
                * cmbk
                * ((mantletemps[0, i] - mantletemps[1, i]) / dr)
                * timestep) / (self.density * self.heatcap * self.radius)
            self.templist.append(self.temperature)
        else:
            self.latent = (
                self.latent
                + (4.0 * np.pi * self.radius ** 2)
                * cmbk
                * ((mantletemps[0, i] - mantletemps[1, i]) / dr)
                * timestep)
            self.latentlist.append(self.latent)
            print("Freezing!\n***\n***\n***")


"""Testing this draft Class"""

"""
# instantiate core object

temp = 2000.0
melt = 1200.0
r = 100.0
rho = 7800.0
cp = 850.0
k = 5.0
maxlh = 4_000_000_000_000_000.0


core1 = Core(temp, melt, r, rho, cp, maxlh, lat=0)
print(core1)

# set up a mantle array
dt = 1
dr = 1.0

max_t = 35000.0

radii = np.arange(100.0, 200.0, dr)
times = np.arange(0, max_t, dt)

temperatures = np.zeros((radii.size, times.size))  # shape: (100, 10000)


# Give the mantle a pretend cooling history (interactive in real application):


temp_init = 2000.0
dT = max_t/50000.0
print(dT)

for j in range(0, times.size):
    for i in range(radii.size-1, 0, -1):
        temperatures[i, j] = temp_init
        temp_init = temp_init - dT
        # print(temp_init)


# make the core cool:

for i in range(0, times.size, dt):
    core1.cooling(temperatures, dt, dr, i, k)
    print(core1)
"""
