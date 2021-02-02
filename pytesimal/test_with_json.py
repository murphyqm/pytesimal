#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 15:02:05 2021.

@author: maeve
"""

import pickle
import modular_cond_cooling as mcc

import os
import inspect

import json

folder = "output_runs/auto_pytest/"  # generic run files are saved here
# by default, if tests="y", output specific to testing is saved to the folder
# "output_runs/testing_output/". HIghlevel testing data is saved to the
# folder "output_runs/default_tests/".
folder1 = "output_runs/testing_output/"

folderb = "pytesimal/auto_pytest/"
folder1b = "pytesimal/output_runs/testing_output"

if not os.path.isdir(str(folder)):
    os.makedirs(str(folder))

if not os.path.isdir(str(folder1)):
    os.makedirs(str(folder1))

if not os.path.isdir(str(folderb)):
    os.makedirs(str(folderb))

if not os.path.isdir(str(folder1b)):
    os.makedirs(str(folder1b))


def test_core_const():
    """
    Simple test that loads default json files and asserts they match output.

    Returns
    -------
    None.

    """
    run_ID = "test_python_constant"
    mcc.conductive_cooling(run_ID, folder, return_vars="n",
                           save_param_file="n", tests="y")
    vals = [1, 1000, 126228]
    folder1 = "output_runs/testing_output/"
    folder2 = "default_test_results/"
    DATA2 = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder2,
            "constant_core.json")
    with open(
            DATA2,
            'r',
            ) as fp:
        default_list = json.load(fp)
    for i in vals:
        string = "core_test_i_" \
            + str(i) \
            + "_var_" \
            + "y" \
            + ".pickle"
        DATA = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder1, string)
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

        assert [new_list] == default_list[str(i)]


def test_core_var():
    """
    Simple test that loads default json files and asserts they match output.

    Returns
    -------
    None.

    """
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
    DATA2 = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder2,
            "variable_core.json")
    with open(
            DATA2,
            'r',
            ) as fp:
        default_list = json.load(fp)
    for i in vals:
        string = "core_test_i_" \
            + str(i) \
            + "_var_" \
            + "n" \
            + ".pickle"
        DATA = os.path.join(os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe()))), folder1, string)
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

        assert [new_list] == default_list[str(i)]
