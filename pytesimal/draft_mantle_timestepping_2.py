#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modifying mantle timestepping function to take new core object and calculate energy extracted
Created on Thu Apr 8 16:24:52 2021.

@author: maeve

to do: need to move temp array set up outside of the discretisation function.
"""
# import os
import numpy as np
# import pickle
# import inspect
# import sys
import draft_core_functions_2
import draft_mantle_properties

class MantleBCDirichlet:
    def __init__(self):
        pass

def discretisation(
    latent,
    temp_init,
    core_temp_init,
    temp_core_melting,
    temp_surface,
    cmb_conductivity,
    p,
    c,
    temperatures,
    dr,
    coretemp_array,
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

    temp_list_mid_mantle = [temp_init]  # TODO - make this all possibly variable
    temp_list_shal = [temp_init]
    temp_list_cmb_5 = [temp_init]
    temperatures[:, 0] = temp_init # this can be an array or a scalar
    core_boundary_temperature = core_temp_init
    coretemp_array[:, 0] = core_temp_init
    max_core_lh = (
        4.0 / 3.0 * np.pi * (r_core ** 3) * core_density * core_latent_heat
    )
    # core_lh_extracted = 0.0
    # instantiate core object and energy extracted
    cmb_energy = draft_core_functions_2.EnergyExtractedAcrossCMB(r_core, timestep, dr)
    core_values = draft_core_functions_2.IsothermalEutecticCore(temp=core_temp_init, melt=temp_core_melting,
                                                                outer_r=r_core, inner_r=0, rho=core_density, cp=core_cp,
                                                                core_latent_heat=core_latent_heat)

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

            checkpoint_mm = radii[int(len(radii) / 2.0)]  # TODO just let checkpoints be fed in manually
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
        temperatures[-1, i] = temp_surface  # TODO: should these be bundled in some sort of boundary condition object
        temperatures[0, i] = core_boundary_temperature
        # coretemp_array[:, i] = temperatures[0, i] # can this be moved to the core object instead
        cmb_conductivity = cond.getk(
            temperatures[0, i]
        )
        # energy = cmb_energy.energy_extracted(temperatures, i, cmb_conductivity)
        power = cmb_energy.power(temperatures, i, cmb_conductivity)
        # core_values.cooling(temperatures, timestep, dr, i, cmb_conductivity)
        # core_values.extract_energy(energy)
        core_values.extract_heat(power, timestep)
        latent = core_values.latentlist
        # core_lh_extracted = core_values.latent
        core_boundary_temperature = core_values.temperature
        # latent, core_lh_extracted, core_boundary_temperature = core_cooling(
        # # latent is now core.latentlist
        # # core_lh_extracted is now core.latent
        # # core_boundary_temperature = core.temperature
        #     latent,
        #     i,
        #     dr,
        #     core_boundary_temperature,
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
    coretemp_array = core_values.temperature_array_3D(coretemp_array)
    return (
        temperatures,
        coretemp_array,
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
