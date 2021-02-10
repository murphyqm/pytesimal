#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:24:52 2021

@author: maeve
"""
import os
import numpy as np
import pickle
import inspect
import sys
import draft_core_functions
import draft_mantle_properties

def discretisation(
    latent,
    temp_init,
    temp_core_melting,
    temp_surface,
    cmb_conductivity,
    p,
    c,
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
    kappas,
    where_regolith,
    kappa_reg,
    cond_constant="y",
    density_constant="y",
    heat_cap_constant="y",
    non_lin_term="y",
    is_a_test="n",
    i_choice=126228,  # 126228
    TESTING="n",
):
    """
    Finite difference solver with variable k.

    Uses variable heat capacity, conductivity, density as required.

    Uses diffusivity for regolith layer.
    """
    # putting in some bug tests
    print("***/n***/n***/n")
    print("Testing modular conductivity!")
    print("Consant conductivity: ")
    print(cond_constant)
    print("Constant density: ")
    print(density_constant)
    print("Constant heat capacity: ")
    print(heat_cap_constant)
    # checking on temperature dependent properties

    if cond_constant == "y":
        cond = draft_mantle_properties.MantleProperties()

    else:
        cond = draft_mantle_properties.VariableConductivity()

    if heat_cap_constant == "y":

        heatcap = draft_mantle_properties.MantleProperties()

    else:
        heatcap = draft_mantle_properties.VariableHeatCapacity()

    if density_constant == "y":
        dens = draft_mantle_properties.MantleProperties()

    else:
        dens = draft_mantle_properties.VariableDensity()


    temp_list_mid_mantle = [temp_init]
    temp_list_shal = [temp_init]
    temp_list_cmb_5 = [temp_init]
    temperatures[:, 0] = temp_init
    temperature_core = temp_init
    coretemp[:, 0] = temp_init
    max_core_lh = (
        4.0 / 3.0 * np.pi * (r_core ** 3) * core_density * core_latent_heat
    )
    # core_lh_extracted = 0.0
    # instantiate core object
    core_values = draft_core_functions.Core(temp_init, temp_core_melting,
                                            r_core, core_density, core_cp,
                                            max_core_lh)

    A_1list = []
    B_1list = []
    C_1list = []
    delt_list = []

    A_1listcmb = []
    B_1listcmb = []
    C_1listcmb = []
    delt_listcmb = []

    A_1listshal = []
    B_1listshal = []
    C_1listshal = []
    delt_listshal = []

    for i in range(1, len(times[1:]) + 1):

        for j in range(1, len(radii[1:-1]) + 1):

            A_1 = []
            B_1 = []
            C_1 = []

            if where_regolith[j] == 1:
                # check for non-linear term
                if non_lin_term == "y":
                    A_1 = (
                        timestep
                        * (
                            1.0
                            / (
                                dens.getrho(temperatures[j, i - 1])
                                * heatcap.getcp(temperatures[j, i - 1])
                            )
                        )
                    ) * (
                        cond.getdkdT(temperatures[j, i - 1])
                        * (
                            (
                                temperatures[j + 1, i - 1]
                                - temperatures[j - 1, i - 1]
                            )
                            ** 2
                        )
                        / (4.0 * dr ** 2.0)
                    )
                else:
                    A_1 = 0

                B_1 = (
                    timestep
                    * (
                        1.0
                        / (
                            dens.getrho(temperatures[j, i - 1])
                            * heatcap.getcp(temperatures[j, i - 1])
                        )
                    )
                ) * (
                    (cond.getk(temperatures[j, i - 1]) / (radii[j] * dr))
                    * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
                )

                C_1 = (
                    timestep
                    * (
                        1.0
                        / (
                            dens.getrho(temperatures[j, i - 1])
                            * heatcap.getcp(temperatures[j, i - 1])
                        )
                    )
                ) * (
                    (cond.getk(temperatures[j, i - 1]) / dr ** 2.0)
                    * (
                        temperatures[j + 1, i - 1]
                        - 2 * temperatures[j, i - 1]
                        + temperatures[j - 1, i - 1]
                    )
                )
                temperatures[j, i] = temperatures[j, i - 1] + A_1 + B_1 + C_1

            elif where_regolith[j] == 0:

                A_1 = 0  # non-linear term
                B_1 = (timestep) * (
                    (kappa_reg / (radii[j] * dr))
                    * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
                )
                C_1 = (timestep) * (
                    (kappa_reg / dr ** 2.0)
                    * (
                        temperatures[j + 1, i - 1]
                        - 2 * temperatures[j, i - 1]
                        + temperatures[j - 1, i - 1]
                    )
                )

                temperatures[j, i] = temperatures[j, i - 1] + A_1 + B_1 + C_1
            # old checkpoints
            #            checkpoint_mm = radii[int(len(radii)/2.0)]
            #            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            #            checkpoint_shal = radii[int(len(radii)-5)]
            # new checkpoints
            checkpoint_mm = radii[int(len(radii) / 2.0)]
            checkpoint_cmb = radii[int(2.0 * len(radii) / 3.0)]
            checkpoint_shal = radii[int(len(radii) / 3.0)]
            if radii[j] == checkpoint_mm:
                temp_list_mid_mantle.append(temperatures[j, i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(
                    ((temperatures[j, i - 1]) - (temperatures[j, i]))
                )

            elif radii[j] == checkpoint_cmb:
                temp_list_cmb_5.append(temperatures[j, i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(
                    ((temperatures[j, i - 1]) - (temperatures[j, i]))
                )

            elif radii[j] == checkpoint_shal:
                temp_list_shal.append(temperatures[j, i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(
                    ((temperatures[j, i - 1]) - (temperatures[j, i]))
                )
            else:
                pass

        # set top and bottom temperatures as fixed
        temperatures[-1, i] = temp_surface
        temperatures[0, i] = temperature_core
        coretemp[:, i] = temperatures[0, i]
        cmb_conductivity = cond.getk(
            temperatures[0, i]
        )
        core_values.cooling(temperatures, timestep, dr, i, cmb_conductivity)
        latent = core_values.latentlist
        # core_lh_extracted = core_values.latent
        temperature_core = core_values.temperature
        # latent, core_lh_extracted, temperature_core = core_cooling(
        # # latent is now core.latentlist
        # # core_lh_extracted is now core.latent
        # # temperature_core = core.temperature
        #     latent,
        #     i,
        #     dr,
        #     temperature_core,
        #     temp_core_melting,
        #     core_lh_extracted,
        #     max_core_lh,
        #     cmb_conductivity,
        #     temperatures,
        #     timestep,
        #     core_density,
        #     core_cp,
        #     r_core,
        # )
    return (
        temperatures,
        coretemp,
        latent,
        temp_list_mid_mantle,
        temp_list_shal,
        temp_list_cmb_5,
        A_1list,
        B_1list,
        C_1list,
        delt_list,
        A_1listcmb,
        B_1listcmb,
        C_1listcmb,
        delt_listcmb,
        A_1listshal,
        B_1listshal,
        C_1listshal,
        delt_listshal,
    )