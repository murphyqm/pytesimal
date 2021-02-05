#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:05:24 2021

@author: maeve
"""

import numpy as np


class Core:
    """Core class represents and manipulates core temp and latent heat."""

    def __init__(self, temp, melt, r, rho, cp, k, maxlh, lat=0):
        """Create a new core with temperature and latent heat."""
        self.temperature = temp
        self.latent = lat
        self.melting = melt
        self.radius = r
        self.density = rho
        self.heatcap = cp
        self.cmbk = k
        self.maxlatent = maxlh
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

    def cooling(self, mantletemps, timestep, dr, i):
        """Cool core or extract latent heat."""
        if (self.temperature > self.melting) or (self.latent >= self.maxlatent):
            print(self.temperature)
            self.temperature = self.temperature - (
                3.0
                * self.cmbk
                * ((mantletemps[0, i] - mantletemps[1, i]) / dr)
                * timestep) / (self.density * self.heatcap * self.radius)
            self.templist.append(self.temperature)
        else:
            self.latent = (
                self.latent
                + (4.0 * np.pi * self.radius ** 2)
                * self.cmbk
                * ((mantletemps[0, i] - mantletemps[1, i]) / dr)
                * timestep)
            self.latentlist.append(self.latent)


"""Testing this draft Class"""

# instantiate core object

temp = 1800.0
melt = 1200.0
r = 100.0
rho = 7800.0
cp = 850.0
k = 3.0
maxlh = 270_000.0


core1 = Core(temp, melt, r, rho, cp, k, maxlh, lat=0)
print(core1)

# set up a mantle array
dt = 1
dr = 1.0

radii = np.arange(100.0, 200.0, dr)
times = np.arange(0, 100000.0, dt)

temperatures = np.zeros((radii.size, times.size))  # shape: (100, 10000)


# Give the mantle a pretend cooling history (interactive in real application):


temp_init = 1600.0

for j in range(times.size-1, 0, -1):
    for i in range(0, radii.size):
        temperatures[i, j] = temp_init
        temp_init -= 10


# make the core cool:

for i in range (0, 10000, dt):
    core1.cooling(temperatures, dt, dr, i)
    # print(core1)

