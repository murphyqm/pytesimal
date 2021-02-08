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

    def getrho(self, T=295, P=0.1):
        """Get density."""
        return self._rho

    rho = property(getrho, "density")  # maybe uneccessary?

    def getcp(self, T=295, P=0.1):
        """Get heat capacity."""
        return self._cp

    cp = property(getcp, "heat capacity")

    def getk(self, T=295, P=0.1):
        """Get conductivity."""
        return self._k

    k = property(getk, "conductivity")

    def getdkdT(self, T=295, P=0.1):
        """Get gradient of condcutivity."""
        dkdT = 0
        return dkdT

    k = property(getk, "conductivity")

    def getkappa(self):
        """Get diffusivity."""
        diffusivity = (self._k)/(self._rho * self._cp)
        return diffusivity

    kappa = property(getkappa, "diffusivity")


mantle = MantleProperties()

print(mantle.k)
print(mantle.kappa)
print(mantle.rho)


class VariableDensity(MantleProperties):
    """Make density T-dependent."""

    def getrho(self, T=295.0):
        """Get density."""

        def alpha(T=295.0):
            a = 3.304e-5 + (0.742e-8 * T) - 0.538 * (T ** -2.0)
            return a

        rho_0 = 3341.0
        T0 = 300.0
        new_rho = rho_0 - alpha(T) * rho_0 * (T - T0)
        self._rho = new_rho
        return self._rho

    rho = property(getrho, "density")  # might cut


density = VariableDensity()
new_density = density.getrho(T=250)
print(new_density)

density.rho  # again, not sure this is useful? might cut.


class VariableHeatCapacity(MantleProperties):
    """Make heat capacity T-dependent."""

    def getcp(self, T=295):
        """Get heat capacity."""
        new_heatcap = (
                995.1
                + (1343.0 * ((T) ** (-0.5)))
                - (2.887 * (10 ** 7.0) * ((T) ** (-2.0)))
                - (6.166 * (10.0 ** (-2.0)) * (T) ** (-3.0))
            )
        self._cp = new_heatcap
        return self._cp


heatcap = VariableHeatCapacity()
new_heatcap = heatcap.getcp(T=250)
print(new_heatcap)


class VariableConductivity(MantleProperties):
    """Make conductivity T-dependent."""

    def getk(self, T=295, P=0.1):
        """Get conductivity."""
        new_cond = (
                80.4205952575632
                * (
                    1.3193574749943 * T ** (-0.5)
                    + 0.977581998039333
                    - 28361.7649315602 / T ** 2.0
                    - 6.05745211527538e-5 / T ** 3.0
                )
                * (1.0 / T) ** 0.5
            )
        self._k = new_cond
        return self._k

    def getdkdT(self, T=295):
        """Get conductivity prime."""
        k_prime = (
                80.4205952575632
                * (
                    -0.659678737497148 * T ** (-1.5)
                    + 56723.5298631204 / T ** 3.0
                    + 0.000181723563458261 / T ** 4.0
                )
                * (1.0 / T) ** 0.5
                - 40.2102976287816
                * (
                    1.3193574749943 * T ** (-0.5)
                    + 0.977581998039333
                    - 28361.7649315602 / T ** 2.0
                    - 6.05745211527538e-5 / T ** 3.0
                )
                * (1.0 / T) ** 0.5
                / T
            )
        return k_prime
