#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 13:37:58 2021

@author: maeve
"""


class MantleProperties:
    """Mantle properties class."""

    def __init__(self):
        """Initialise mantle properties."""
        self._rho = 3341.0
        self._cp = 819.0
        self._k = 3.0

    def getrho(self):
        """Get density."""
        return self._rho

    rho = property(getrho, "density")

    def getcp(self):
        """Get heat capacity."""
        return self._cp

    cp = property(getcp, "heat capacity")

    def getk(self):
        """Get condcutivity."""
        return self._k

    k = property(getk, "conductivity")

    def getkappa(self):
        """Get diffusivity."""
        diffusivity = (self._k)/(self._rho * self._cp)
        return diffusivity

    kappa = property(getkappa, "diffusivity")


mantle = MantleProperties()

print(mantle.k)
print(mantle.kappa)