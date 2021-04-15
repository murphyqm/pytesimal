#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14/04/2021
by murphyqm

"""

from context import draft_analysis
import pytest

def test_cloudy_zone():
	d_im = 147  # cz diameter in nm
	d_esq = 158  # cz diameter in nm
	im_cr = draft_analysis.cooling_rate_cloudyzone_diameter(d_im)
	esq_cr = draft_analysis.cooling_rate_cloudyzone_diameter(d_esq)
	assert im_cr == pytest.approx(3.9512517443065804)
	assert esq_cr == pytest.approx(3.2051578229316235)

def test_tetrataenite_bandwidth():
	width = 100
	cooling_rate = draft_analysis.cooling_rate_tetra_width(width)
	assert cooling_rate == pytest.approx(365.22828714149324)

def test_cooling_rate_to_seconds():
	im_cr = 3.95
	esq_cr = 3.21
	im_cr_s = draft_analysis.cooling_rate_to_seconds(im_cr)
	esq_cr_s = draft_analysis.cooling_rate_to_seconds(esq_cr)
	assert im_cr_s == pytest.approx(1.2517062023088055e-13)
	assert esq_cr_s == pytest.approx(1.0172093441547507e-13)

# def test_depth_and_timing(temperature_timestepping):

def test_core_freezing1(temperature_timestepping):
	myr = 3.1556926e13
	max_time = 400 * myr
	data = temperature_timestepping
	(core_frozen,
	 times_frozen,
	 time_core_frozen,
	 fully_frozen) = draft_analysis.core_freezing(
		coretemp = data["core_temperature_array"],
		max_time = max_time,
		times = data["times"],
		latent = data["latent"],
		temp_core_melting = data["temp_core_melting"],
		timestep=1E11
	)
	# assert core_frozen == 10
	# # assert times_frozen == 10
	assert time_core_frozen == 5411100000000000.0
	assert fully_frozen == 7637200000000000.0

# def test_core_freezing2(temperature_timestepping):
# 	myr = 3.1556926e13
# 	max_time = 400 * myr
# 	data = temperature_timestepping
# 	(core_frozen,
# 	 times_frozen,
# 	 time_core_frozen,
# 	 fully_frozen) = draft_analysis.core_freezing(
# 		coretemp = data["core_temperature_array"],
# 		max_time = max_time,
# 		times = data["times"],
# 		latent = data["latent"],
# 		temp_core_melting = data["temp_core_melting"],
# 		timestep=1E11
# 	)
# 	# assert core_frozen == 10
# 	assert times_frozen == 10
# 	# assert time_core_frozen == 0.0
# 	# assert fully_frozen == 5
#
# def test_core_freezing3(temperature_timestepping):
# 	myr = 3.1556926e13
# 	max_time = 400 * myr
# 	data = temperature_timestepping
# 	(core_frozen,
# 	 times_frozen,
# 	 time_core_frozen,
# 	 fully_frozen) = draft_analysis.core_freezing(
# 		coretemp = data["core_temperature_array"],
# 		max_time = max_time,
# 		times = data["times"],
# 		latent = data["latent"],
# 		temp_core_melting = data["temp_core_melting"],
# 		timestep=1E11
# 	)
# 	# assert core_frozen == 10
# 	# assert times_frozen == 10
# 	assert time_core_frozen == 0.0
# 	assert fully_frozen == 0.0