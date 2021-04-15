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


class MantleBC: # TODO maybe instead include this in the setup function?
    def __init__(self):
        pass

    def dirichlet(self, temperatures, temp_surface, core_boundary_temperature, i): # TODO maybe this should just be a function
        temperatures[-1, i] = temp_surface
        temperatures[0, i] = core_boundary_temperature


def discretisation(
    latent,
    temp_init,
    core_temp_init,
    temp_core_melting,
    temp_surface,
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
    where_regolith,
    kappa_reg,
    cond_constant="y",
    density_constant="y",
    heat_cap_constant="y",
    non_lin_term="y",
    mantle_density=3341.0,
    mantle_heat_capacity=819.0,
    mantle_conductivity=3.0
):
    """
    Finite difference solver with variable k.

    Uses variable heat capacity, conductivity, density as required.

    Uses diffusivity for regolith layer.
    """
    # putting in some bug tests
    print("***/n***/n***/n")
    print("Testing modular conductivity!")
    print("Constant conductivity: ")
    print(cond_constant)
    print("Constant density: ")
    print(density_constant)
    print("Constant heat capacity: ")
    print(heat_cap_constant)
    # checking on temperature dependent properties

    if cond_constant == "y":
        cond = draft_mantle_properties.MantleProperties(k=mantle_conductivity)

    else:
        cond = draft_mantle_properties.VariableConductivity()

    if heat_cap_constant == "y":

        heatcap = draft_mantle_properties.MantleProperties(cp=mantle_heat_capacity)

    else:
        heatcap = draft_mantle_properties.VariableHeatCapacity()

    if density_constant == "y":
        dens = draft_mantle_properties.MantleProperties(rho=mantle_density)

    else:
        dens = draft_mantle_properties.VariableDensity()

    temp_list_mid_mantle = [temp_init]  # TODO - make this all possibly variable
    temp_list_shal = [temp_init]
    temp_list_cmb_5 = [temp_init]
    temperatures[:, 0] = temp_init # this can be an array or a scalar
    core_boundary_temperature = core_temp_init
    coretemp_array[:, 0] = core_temp_init
    # instantiate boundary conditions
    boundary_conds = MantleBC()
    # instantiate core object and energy extracted
    cmb_energy = draft_core_functions_2.EnergyExtractedAcrossCMB(r_core, timestep, dr)
    core_values = draft_core_functions_2.IsothermalEutecticCore(temp=core_temp_init, melt=temp_core_melting,
                                                                outer_r=r_core, inner_r=0, rho=core_density, cp=core_cp,
                                                                core_latent_heat=core_latent_heat)

    A_1list = [] # TODO make all these customisable
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
        boundary_conds.dirichlet(temperatures,
                                 temp_surface,
                                 core_boundary_temperature,
                                 i)
        # temperatures[-1, i] = temp_surface
        # temperatures[0, i] = core_boundary_temperature
        cmb_conductivity = cond.getk(temperatures[0, i])
        power = cmb_energy.power(temperatures, i, cmb_conductivity)
        core_values.extract_heat(power, timestep)
        latent = core_values.latentlist
        core_boundary_temperature = core_values.temperature
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


# not sure if I can use numba.jit on the following - complication with
# # objects/methods...
# def iteration(
#     temp_surface,
#     temperatures,
#     dr,
#     timestep,
#     radii,
#     times,
#     where_regolith,
#     kappa_reg,
#     temp_list_mid_mantle,
#     temp_list_shal,
#     temp_list_cmb_5,
#     A_1list,
#     B_1list,
#     C_1list,
#     delt_list,
#     A_1listcmb,
#     B_1listcmb,
#     C_1listcmb,
#     delt_listcmb,
#     A_1listshal,
#     B_1listshal,
#     C_1listshal,
#     delt_listshal,
#     cond,
#     dens,
#     heatcap,
#     boundary_conds,
#     cmb_energy,
#     core_values,
#     non_lin_term="y",
# ):
#     for i in range(1, len(times[1:]) + 1):
#
#         for j in range(1, len(radii[1:-1]) + 1):
#
#             A_1 = []
#             B_1 = []
#             C_1 = []
#
#             if where_regolith[j] == 1:
#                 # check for non-linear term
#                 if non_lin_term == "y":
#                     A_1 = (
#                         timestep
#                         * (
#                             1.0
#                             / (
#                                 dens.getrho(temperatures[j, i - 1])
#                                 * heatcap.getcp(temperatures[j, i - 1])
#                             )
#                         )
#                     ) * (
#                         cond.getdkdT(temperatures[j, i - 1])
#                         * (
#                             (
#                                 temperatures[j + 1, i - 1]
#                                 - temperatures[j - 1, i - 1]
#                             )
#                             ** 2
#                         )
#                         / (4.0 * dr ** 2.0)
#                     )
#                 else:
#                     A_1 = 0
#
#                 B_1 = (
#                     timestep
#                     * (
#                         1.0
#                         / (
#                             dens.getrho(temperatures[j, i - 1])
#                             * heatcap.getcp(temperatures[j, i - 1])
#                         )
#                     )
#                 ) * (
#                     (cond.getk(temperatures[j, i - 1]) / (radii[j] * dr))
#                     * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
#                 )
#
#                 C_1 = (
#                     timestep
#                     * (
#                         1.0
#                         / (
#                             dens.getrho(temperatures[j, i - 1])
#                             * heatcap.getcp(temperatures[j, i - 1])
#                         )
#                     )
#                 ) * (
#                     (cond.getk(temperatures[j, i - 1]) / dr ** 2.0)
#                     * (
#                         temperatures[j + 1, i - 1]
#                         - 2 * temperatures[j, i - 1]
#                         + temperatures[j - 1, i - 1]
#                     )
#                 )
#                 temperatures[j, i] = temperatures[j, i - 1] + A_1 + B_1 + C_1
#
#             elif where_regolith[j] == 0:
#
#                 A_1 = 0  # non-linear term
#                 B_1 = (timestep) * (
#                     (kappa_reg / (radii[j] * dr))
#                     * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
#                 )
#                 C_1 = (timestep) * (
#                     (kappa_reg / dr ** 2.0)
#                     * (
#                         temperatures[j + 1, i - 1]
#                         - 2 * temperatures[j, i - 1]
#                         + temperatures[j - 1, i - 1]
#                     )
#                 )
#
#                 temperatures[j, i] = temperatures[j, i - 1] + A_1 + B_1 + C_1
#
#             checkpoint_mm = radii[int(len(radii) / 2.0)]  # TODO just let checkpoints be fed in manually
#             checkpoint_cmb = radii[int(2.0 * len(radii) / 3.0)]
#             checkpoint_shal = radii[int(len(radii) / 3.0)]
#             if radii[j] == checkpoint_mm:
#                 temp_list_mid_mantle.append(temperatures[j, i])
#                 A_1list.append(A_1)
#                 B_1list.append(B_1)
#                 C_1list.append(C_1)
#                 delt_list.append(
#                     ((temperatures[j, i - 1]) - (temperatures[j, i]))
#                 )
#
#             elif radii[j] == checkpoint_cmb:
#                 temp_list_cmb_5.append(temperatures[j, i])
#                 A_1listcmb.append(A_1)
#                 B_1listcmb.append(B_1)
#                 C_1listcmb.append(C_1)
#                 delt_listcmb.append(
#                     ((temperatures[j, i - 1]) - (temperatures[j, i]))
#                 )
#
#             elif radii[j] == checkpoint_shal:
#                 temp_list_shal.append(temperatures[j, i])
#                 A_1listshal.append(A_1)
#                 B_1listshal.append(B_1)
#                 C_1listshal.append(C_1)
#                 delt_listshal.append(
#                     ((temperatures[j, i - 1]) - (temperatures[j, i]))
#                 )
#             else:
#                 pass
#
#         # set top and bottom temperatures as fixed
#         boundary_conds.dirichlet(temperatures,
#                                  temp_surface,
#                                  core_boundary_temperature,
#                                  i)
#         # temperatures[-1, i] = temp_surface
#         # temperatures[0, i] = core_boundary_temperature
#         cmb_conductivity = cond.getk(temperatures[0, i])
#         power = cmb_energy.power(temperatures, i, cmb_conductivity)
#         core_values.extract_heat(power, timestep)
#         latent = core_values.latentlist
#         core_boundary_temperature = core_values.temperature