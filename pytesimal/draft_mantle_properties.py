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

    def setrho(self, value):
        """Set density."""
        self._rho = value

    rho = property(getrho, setrho, "I am the density.")

    def getcp(self):
        """Get heat capacity."""
        return self._cp

    def setcp(self, value):
        """Set heat capacity."""
        self._cp = value

    cp = property(getcp, setcp, "I am the heat capacity.")

    def getk(self):
        """Get condcutivity."""
        return self._k

    def setk(self, value):
        """Set conductivity."""
        self._k = value

    k = property(getk, setk, "I am the conductivity.")
