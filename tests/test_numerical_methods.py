#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22/04/2021
by murphyqm

"""
import numpy as np
import pytest
from context import numerical_methods



def test_diffusivity():
	k = 3.5
	heat_cap = 600
	rho = 3341
	diffusivity = numerical_methods.calculate_diffusivity(k, heat_cap, rho)
	assert diffusivity == pytest.approx(1.7459842362566098e-06)


def test_stability():
	diffusivity = 1.8e-6
	timestep = 1e11
	dr = 1000.0
	result = numerical_methods.check_stability(diffusivity, timestep, dr)
	assert result

def test_stability2():
	diffusivity = 8e-6
	timestep = 1e11
	dr = 1000.0
	result = numerical_methods.check_stability(diffusivity, timestep, dr)
	opposite = not(result)
	assert opposite

def test_diric_surface():
	temperatures = np.zeros((3,3))
	temp_surface = 1
	i = 2
	temperatures = numerical_methods.surface_dirichlet_bc(
		temperatures,
		temp_surface,
		i)
	result = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,1.]])
	np.testing.assert_array_almost_equal_nulp(temperatures,result)

def test_diric_cmb():
	temperatures = np.zeros((3,3))
	temp_surface = 1
	i = 2
	temperatures = numerical_methods.cmb_dirichlet_bc(
		temperatures,
		temp_surface,
		i)
	result = np.array([[0.,0.,1.],[0.,0.,0.],[0.,0.,0.]])
	np.testing.assert_array_almost_equal_nulp(temperatures,result)

def test_neumann_cmb():
	temperatures = np.array([[3.,3.,3.],[2.,2.,2.],[1.,1.,0.]])
	temp_surface = 1
	i = 2
	temperatures = numerical_methods.cmb_neumann_bc(
		temperatures,
		temp_surface,
		i)
	result = np.array([[3.,3., 2.6666666666666665],[2.,2.,2.],[1.,1.,0.]])
	np.testing.assert_array_almost_equal_nulp(temperatures,result)

# def test_energy_extracted():
# 	mantle_temperatures = np.array([[3.,3.,3.],[2.,2.,2.],[1.,1.,0.]])
# 	energy_object = numerical_methods.EnergyExtractedAcrossCMB(10.0, 1.0, 1.0)
# 	print(energy_object.power(mantle_temperatures, i, k))