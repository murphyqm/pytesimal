#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mantle properties test

Created on Tue Feb  9 12:15:12 2021

@author: maeve
"""
from context import mantle_properties as mp

# import numpy as np
import pytest

# import matplotlib.pyplot as plt

# # informal test first: plotting the mantle properties:
# # The functions reproduce the figure from the old functions

# T = np.arange(200, 1801)

# cp = mantle.VariableHeatCapacity()
# rho = mantle.VariableDensity()
# k = mantle.VariableConductivity()

# cp_range = cp.getcp(T)
# rho_range = rho.getrho(T)
# k_range = k.getk(T)
# vol_heat_cap = (cp_range * rho_range)/3341.0

# # plt.plot(T, vol_heat_cap)
# plt.plot(T, k_range)
# plt.show()


def test_mantleprop_defaults():
    mantle = mp.MantleProperties()
    assert mantle.getrho() == 3341.0
    assert mantle.getcp() == 819.0
    assert mantle.getk() == 3.0
    assert mantle.getkappa() == pytest.approx(1.0963794262207911e-06)


def test_mantleprop_constant():
    mantle = mp.MantleProperties()
    mantle.setrho(500.0)
    assert mantle.getrho() == 500.0
    mantle.setcp(900.0)
    assert mantle.getcp() == 900.0
    mantle.setk(100.0)
    assert mantle.getk() == 100.0
    assert mantle.getkappa() == pytest.approx(0.00022222222222222223)


def test_variable_k():
    cond = mp.VariableConductivity()
    assert cond.getk(350, 0.1) == pytest.approx(3.510201158262625)
    assert cond.getk(1800, 0.1) == pytest.approx(1.8953911889912938)
    assert cond.getk(161.96, 0.1) == pytest.approx(0.00015313048512481455)
    assert cond.getdkdT(350) == pytest.approx(0.00023947115323349165)
    assert cond.getdkdT(1800) == pytest.approx(-0.0005244351242307716)
    assert cond.getdkdT(161.96) == pytest.approx(0.0823500186171907)


def test_variablecp():
    cp = mp.VariableHeatCapacity()
    assert cp.getcp(350) == pytest.approx(831.212900188484)
    assert cp.getcp(1800) == pytest.approx(1017.8443197439468)
    assert cp.getcp(161.96) == pytest.approx(0.024666741910952507)


def test_variablerho():
    rho = mp.VariableDensity()
    print(rho.getrho(161.96))
    assert rho.getrho(350) == pytest.approx(3335.7804954765306)
    assert rho.getrho(1800) == pytest.approx(3109.3186024814813)
    assert rho.getrho(161.96) == pytest.approx(3347.3329416632596)
