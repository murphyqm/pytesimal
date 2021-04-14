#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13/04/2021
by murphyqm

"""
import json


def make_default_param_file():
    default_variables = {'run_ID': 'example_default',
                         'folder': 'example_default',
                         'timestep': 1e11,
                         'r_planet': 250000.0,
                         'core_size_factor': 0.5,
                         'reg_fraction': 0.032,
                         'max_time': 400,
                         'temp_core_melting': 1200.0,
                         'olivine_cp': 819.0,
                         'olivine_density': 3341.0,
                         'cmb_conductivity': 3.0,
                         'core_cp': 850.0,
                         'core_density': 7800.0,
                         'temp_init': 1600.0,
                         'temp_surface': 250.0,
                         'core_temp_init': 1600.0,
                         'core_latent_heat': 270000.0,
                         'kappa_reg': 5.0e-8,
                         'dr': 1000.0,
                         'cond_constant': "y",
                         'density_constant': "y",
                         'heat_cap_constant': "y", }

    with open('example_input_file_with_default_parameters.txt',
              'w') as file:
        json.dump(default_variables, file, indent=4)


def load_params_from_file(filename='example_input_file_with_default_parameters.txt'):
    with open(filename) as json_file:
        data = json.load(json_file)
        run_ID = data['run_ID']
        folder = data['folder']
        timestep = data['timestep']
        r_planet = data['r_planet']
        core_size_factor = data['core_size_factor']
        reg_fraction = data['reg_fraction']
        max_time = data['max_time']
        temp_core_melting = data['temp_core_melting']
        olivine_cp = data['olivine_cp']
        olivine_density = data['olivine_density']
        cmb_conductivity = data['cmb_conductivity']
        core_cp = data['core_cp']
        core_density = data['core_density']
        temp_init = data['temp_init']
        temp_surface = data['temp_surface']
        core_temp_init = data['core_temp_init']
        core_latent_heat = data['core_latent_heat']
        kappa_reg = data['kappa_reg']
        dr = data['dr']
        cond_constant = data['cond_constant']
        density_constant = data['density_constant']
        heat_cap_constant = data['heat_cap_constant']
        return (run_ID, folder, timestep, r_planet, core_size_factor,
                reg_fraction, max_time, temp_core_melting, olivine_cp,
                olivine_density, cmb_conductivity, core_cp, core_density,
                temp_init, temp_surface, core_temp_init, core_latent_heat,
                kappa_reg, dr, cond_constant, density_constant,
                heat_cap_constant)


make_default_param_file()