#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define mantle properties as constant or temperature-dependent.

Set mantle conductivity, density and heat capacity as constant values or
define them as functions of temperature. The `MantleProperties` class has
methods which define constant values for mantle properties, which can then
individually be overridden by the `VariableConductivity`, `VariableDensity` and
`VariableHeatCapacity` subclasses. The `VariableConductivity` subclass also
contains a method to calculate the derivative of the conductivity with respect
to time.

The functions used for variable properties are based on experimental results
and mineral physics theory, discussed in
`Murphy Quinlan et al. (2021) <https://doi.org/10.1029/2020JE006726>`_ and the
references therein.
"""


class MantleProperties:
    """
    Mantle properties class to define thermal properties of mantle material.

    The value of conductivity, heat capacity or density can be called using the
    `get` methods, and can be changed using the `set` methods. They can be
    overridden with temperature-dependent functions using subclasses for each
    individual property.

    Temperature and pressure are optional arguments for the `get` methods;
    these are not used when the values are temperature-independent but
    allow for easy insertion of temperature or pressure dependent functions
    into pre-existing code with minimal changes.

    Attributes
    ----------
    rho : float, default 3341.0
        The density of the mantle material (constant)
    cp : float, default 819.0
        The heat capacity of mantle material (constant)
    k : float, default 3.0
        The conductivity of mantle material (constant)
    """

    def __init__(self, rho=3341.0, cp=819.0, k=3.0):
        """Initialise mantle properties."""
        self._rho = rho
        self._cp = cp
        self._k = k

    def __str__(self):
        """Return string."""
        return "Mantle rho: {0}; mantle cp: {1}; mantle k: {2}".format(
            self._rho, self._cp, self._k
        )

    def getrho(self, T=295, P=0.1):
        """Get density."""
        return self._rho

    def setrho(self, value):
        """Set density."""
        self._rho = value

    def getcp(self, T=295, P=0.1):
        """Get heat capacity."""
        return self._cp

    def setcp(self, value):
        """Set heat capacity."""
        self._cp = value

    def getk(self, T=295, P=0.1):
        """Get conductivity."""
        return self._k

    def setk(self, value):
        """Set conductivity."""
        self._k = value

    def getdkdT(self, T=295, P=0.1):
        """Get gradient of conductivity."""
        dkdT = 0  # zero when conductivity is a constant in temperature
        return dkdT

    def getkappa(self):
        """Get diffusivity."""
        diffusivity = (self._k) / (self._rho * self._cp)
        return diffusivity


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

    # rho = property(getrho, "density")  # might cut


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
        """Get derivative of conductivity with respect to temperature."""
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


def set_up_mantle_properties(
    cond_constant="y",
    density_constant="y",
    heat_cap_constant="y",
    mantle_density=3341.0,
    mantle_heat_capacity=819.0,
    mantle_conductivity=3.0,
):
    """
    Define mantle properties quickly

    A quick set-up function that can read parameters and flags from loaded
    parameter files to set up mantle properties.

    Parameters
    ----------
    cond_constant : str, default 'y'
        Flag to define if conductivity is constant in temperature or not.
        Default `'y'` results in constant conductivity, while any other string
        produces variable conductivity.
    density_constant : str, default 'y'
        Flag to define if density is constant in temperature or not.
        Default `'y'` results in constant density, while any other string
        produces variable density.
    heat_cap_constant : str, default 'y'
        Flag to define if heat capacity is constant in temperature or not.
        Default `'y'` results in constant heat capacity, while any other string
        produces variable heat capacity.
    mantle_density : float, default 3341.0
        Constant value for mantle density
    mantle_heat_capacity : float, default 819.0
        Constant value for mantle heat capacity
    mantle_conductivity : float
        Constant value for mantle conductivity

    Returns
    -------
    conductivity : object
        Conductivity object, with constant or temperature dependent value
    heat_capacity : object
        Heat capacity object, with constant or temperature dependent value
    density : object
        Density object, with constant or temperature dependent value

    """
    if cond_constant == "y":
        conductivity = MantleProperties(k=mantle_conductivity)

    else:
        conductivity = VariableConductivity()

    if heat_cap_constant == "y":

        heat_capacity = MantleProperties(cp=mantle_heat_capacity)

    else:
        heat_capacity = VariableHeatCapacity()

    if density_constant == "y":
        density = MantleProperties(rho=mantle_density)

    else:
        density = VariableDensity()

    return conductivity, heat_capacity, density
