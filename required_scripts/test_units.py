#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 13:34:35 2020

@author: maeve
"""
import pickle
import modular_cond_cooling as mcc

import os
import inspect

# i=2
# folder1 = "output_runs/testing_output/"
# folder2 = "default_test_results/"
# string = "core_test_i_" \
#             + str(i) \
#             + "_var_" \
#             + "y" \
#             + ".pickle"

# DATA = os.path.join(os.path.dirname(os.path.abspath(
#     inspect.getfile(inspect.currentframe()))), folder1, string)
# print(DATA)

folder = "auto_pytest"


def test_core_const():
    run_ID = "test_python_constant"
    mcc.conductive_cooling(run_ID, folder, return_vars="n",
                           save_param_file="n", tests="y")
    vals = [1, 1000, 126228]
    folder1 = "output_runs/testing_output/"
    folder2 = "default_test_results/"
    for i in vals:
        string = "core_test_i_" \
            + str(i) \
            + "_var_" \
            + "y" \
            + ".pickle"
        DATA = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder1, string)
        DATA2 = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder2, string)
        with open(
            DATA,
            "rb",
        ) as f:
            [
                latent,
                i,
                dr,
                temperature_core,
                temp_core_melting,
                core_lh_extracted,
                max_core_lh,
                cmb_conductivity,
                timestep,
                core_density,
                core_cp,
                r_core,
                label,
            ] = pickle.load(f)
        new_list = [
                latent,
                i,
                dr,
                temperature_core,
                temp_core_melting,
                core_lh_extracted,
                max_core_lh,
                cmb_conductivity,
                timestep,
                core_density,
                core_cp,
                r_core,
                label,
            ]
        with open(
            DATA2,
            "rb",
        ) as f:
            [
                dlatent,
                di,
                ddr,
                dtemperature_core,
                dtemp_core_melting,
                dcore_lh_extracted,
                dmax_core_lh,
                dcmb_conductivity,
                dtimestep,
                dcore_density,
                dcore_cp,
                dr_core,
                dlabel,
            ] = pickle.load(f)
        default_list = [
                dlatent,
                di,
                ddr,
                dtemperature_core,
                dtemp_core_melting,
                dcore_lh_extracted,
                dmax_core_lh,
                dcmb_conductivity,
                dtimestep,
                dcore_density,
                dcore_cp,
                dr_core,
                dlabel,
            ]
        assert new_list == default_list


def test_core_var():
    run_ID = "test_python_variable"
    mcc.conductive_cooling(
        run_ID,
        folder,
        cond_constant="n",
        density_constant="n",
        heat_cap_constant="n",
        return_vars="n",
        save_param_file="n",
        tests="y"
    )
    vals = [1, 1000, 126228]
    folder1 = "output_runs/testing_output/"
    folder2 = "default_test_results/"
    for i in vals:
        string = "core_test_i_" \
            + str(i) \
            + "_var_" \
            + "n" \
            + ".pickle"
        DATA = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder1, string)
        DATA2 = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder2, string)
        with open(
            DATA,
            "rb",
        ) as f:
            [
                latent,
                i,
                dr,
                temperature_core,
                temp_core_melting,
                core_lh_extracted,
                max_core_lh,
                cmb_conductivity,
                timestep,
                core_density,
                core_cp,
                r_core,
                label,
            ] = pickle.load(f)
        new_list = [
                latent,
                i,
                dr,
                temperature_core,
                temp_core_melting,
                core_lh_extracted,
                max_core_lh,
                cmb_conductivity,
                timestep,
                core_density,
                core_cp,
                r_core,
                label,
            ]
        with open(
            DATA2,
            "rb",
        ) as f:
            [
                dlatent,
                di,
                ddr,
                dtemperature_core,
                dtemp_core_melting,
                dcore_lh_extracted,
                dmax_core_lh,
                dcmb_conductivity,
                dtimestep,
                dcore_density,
                dcore_cp,
                dr_core,
                dlabel,
            ] = pickle.load(f)
        default_list = [
                dlatent,
                di,
                ddr,
                dtemperature_core,
                dtemp_core_melting,
                dcore_lh_extracted,
                dmax_core_lh,
                dcmb_conductivity,
                dtimestep,
                dcore_density,
                dcore_cp,
                dr_core,
                dlabel,
            ]
        assert new_list == default_list
