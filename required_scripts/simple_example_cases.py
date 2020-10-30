#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:26:11 2020.

@author: maeve
"""
import pickle
import modular_cond_cooling as mcc

# Tests to check tidying comments and variable names doesn't throw errors


folder = "setting_up_tests_oct_2020_2"


# run_ID = "simple_test_22oct20_c"
# (
#     begins_to_freeze,
#     finished_freezing,
#     Esquel_Depth,
#     Esq_timing,
#     Imilac_Depth,
#     Im_timing,
# ) = mcc.conductive_cooling(run_ID, folder, return_vars="y",
#                            save_param_file="n")

# run_ID = "simple_test_22oct20_v"
# (
#     vbegins_to_freeze,
#     vfinished_freezing,
#     vEsquel_Depth,
#     vEsq_timing,
#     vImilac_Depth,
#     vIm_timing,
# ) = mcc.conductive_cooling(
#     run_ID,
#     folder,
#     cond_constant="n",
#     density_constant="n",
#     heat_cap_constant="n",
#     return_vars="y",
#     save_param_file="n",
# )

# print("Constant!")
# print("")
# print(
#     begins_to_freeze,
#     finished_freezing,
#     Esquel_Depth,
#     Esq_timing,
#     Imilac_Depth,
#     Im_timing,
# )
# print("")
# print("***")
# print("Variable!")
# print("")
# print(
#     vbegins_to_freeze,
#     vfinished_freezing,
#     vEsquel_Depth,
#     vEsq_timing,
#     vImilac_Depth,
#     vIm_timing,
# )


# with open(
#     "output_runs/"
#     + "core_test01_variable"
#     + ".pickle",
#     "rb",
# ) as f:
#     [
#         latent,
#         i,
#         dr,
#         temperature_core,
#         temp_core_melting,
#         core_lh_extracted,
#         max_core_lh,
#         cmb_conductivity,
#         temperatures,
#         timestep,
#         core_density,
#         core_cp,
#         r_core,
#         label,
#     ] = pickle.load(f)

# print(latent,
#       i,
#       dr,
#       temperature_core,
#       temp_core_melting,
#       core_lh_extracted,
#       max_core_lh,
#       cmb_conductivity,
#       temperatures,
#       timestep,
#       core_density,
#       core_cp,
#       r_core,
#       label,)
