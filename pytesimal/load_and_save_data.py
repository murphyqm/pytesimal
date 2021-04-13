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
                         'reg_percent': "y",
                         'cond_constant': "y",
                         'density_constant': "y",
                         'heat_cap_constant': "y", }

    with open('example_input_file_with_default_parameters.txt',
              'w') as file:
        json.dump(default_variables, file, indent=4)


def load_params_from_file(filename='example_input_file_with_default_parameters.txt'):

    with open(filename) as json_file:
        data = json.load(json_file)
    return data

make_default_param_file()
data = load_params_from_file('example_input_file_with_default_parameters.txt')

print(data)

# r_planet = data["r_planet"]
# print(r_planet)

"""

latent,
            temp_init,
            core_temp_init,
            temp_core_melting,
            temp_surface,
            temperatures,
            dr,
            coretemp,
            timestep,
            core_density,
            core_cp,
            r_core,
            core_latent_heat,
            radii,
            times,
            where_regolith,
            kappa_reg,
            cond_constant=cond_constant,
            density_constant=density_constant,
            heat_cap_constant=heat_cap_constant,
            non_lin_term=non_lin_term,
            mantle_density=p,
            mantle_heat_capacity=c,
            mantle_conductivity=cmb_conductivity

"""
