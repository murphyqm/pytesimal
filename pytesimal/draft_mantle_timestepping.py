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

        def conductivity(x):
            y = cmb_conductivity
            return y

        def conductivity_prime(x):
            y_prime = 0
            return y_prime

    else:

        def conductivity(x):
            y = (
                80.4205952575632
                * (
                    1.3193574749943 * x ** (-0.5)
                    + 0.977581998039333
                    - 28361.7649315602 / x ** 2.0
                    - 6.05745211527538e-5 / x ** 3.0
                )
                * (1.0 / x) ** 0.5
            )
            return y

        def conductivity_prime(x):
            y_prime = (
                80.4205952575632
                * (
                    -0.659678737497148 * x ** (-1.5)
                    + 56723.5298631204 / x ** 3.0
                    + 0.000181723563458261 / x ** 4.0
                )
                * (1.0 / x) ** 0.5
                - 40.2102976287816
                * (
                    1.3193574749943 * x ** (-0.5)
                    + 0.977581998039333
                    - 28361.7649315602 / x ** 2.0
                    - 6.05745211527538e-5 / x ** 3.0
                )
                * (1.0 / x) ** 0.5
                / x
            )
            return y_prime

    if heat_cap_constant == "y":

        def heat_cap(T):
            cp = c
            return cp

    else:

        def heat_cap(T):
            cp = (
                995.1
                + (1343.0 * ((T) ** (-0.5)))
                - (2.887 * (10 ** 7.0) * ((T) ** (-2.0)))
                - (6.166 * (10.0 ** (-2.0)) * (T) ** (-3.0))
            )
            return cp

    if density_constant == "y":

        def rho(T):
            rho = p
            return rho

    else:

        def alpha(T):
            """
            Calculate the thermal expansion coefficient.

            Function from Su et al., 2018
            """
            alpha = 3.304e-5 + (0.742e-8 * T) - 0.538 * (T ** -2.0)
            return alpha

        def rho(T, rho_0=3341.0, T0=300.0):
            """
            Calculate temperature dependent density.

            Function for beta from Su et al., 2018. Defaults for reference rho
            and T chosen from Bryson et al., 2015 with T0 set to room temp
            """
            rho = rho_0 - alpha(T) * rho_0 * (T - T0)
            return rho

    temp_list_mid_mantle = [temp_init]
    temp_list_shal = [temp_init]
    temp_list_cmb_5 = [temp_init]
    temperatures[:, 0] = temp_init
    temperature_core = temp_init
    coretemp[:, 0] = temp_init
    max_core_lh = (
        4.0 / 3.0 * np.pi * (r_core ** 3) * core_density * core_latent_heat
    )
    core_lh_extracted = 0.0
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
                                rho(temperatures[j, i - 1])
                                * heat_cap(temperatures[j, i - 1])
                            )
                        )
                    ) * (
                        conductivity_prime(temperatures[j, i - 1])
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
                            rho(temperatures[j, i - 1])
                            * heat_cap(temperatures[j, i - 1])
                        )
                    )
                ) * (
                    (conductivity(temperatures[j, i - 1]) / (radii[j] * dr))
                    * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
                )

                C_1 = (
                    timestep
                    * (
                        1.0
                        / (
                            rho(temperatures[j, i - 1])
                            * heat_cap(temperatures[j, i - 1])
                        )
                    )
                ) * (
                    (conductivity(temperatures[j, i - 1]) / dr ** 2.0)
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
        cmb_conductivity = conductivity(
            temperatures[0, i]
        )
        if is_a_test == "y" and i == i_choice:
            # for edge case: i = 126228
            label = "Variable: " + str(cond_constant) + ", i = " + str(i)
            with open(
                "output_runs/default_tests/"
                + "core_test_i_"
                + str(i)
                + "_var_"
                + str(cond_constant)
                + ".pickle",
                "wb",
            ) as f:
                pickle.dump(
                    [
                        latent,
                        i,
                        dr,
                        temperature_core,
                        temp_core_melting,
                        core_lh_extracted,
                        max_core_lh,
                        cmb_conductivity,
                        # temperatures,
                        timestep,
                        core_density,
                        core_cp,
                        r_core,
                        label,
                    ],
                    f,
                )
                sys.exit()
        else:
            pass
        if TESTING == "n":
            pass
        else:
            if i == 1 or i == 1000 or i == 126228:
                label = "Variable: " \
                    + str(cond_constant) \
                    + ", i = " + str(i)
                string = "core_test_i_" \
                    + str(i) \
                    + "_var_" \
                    + str(cond_constant) \
                    + ".pickle"
                folder1 = "output_runs/testing_output/"
                DATA = os.path.join(os.path.dirname(os.path.abspath(
                    inspect.getfile(inspect.currentframe()))), folder1, string)
                with open(
                    DATA,
                    "wb",
                ) as f:
                    pickle.dump(
                        [
                            latent,
                            i,
                            dr,
                            temperature_core,
                            temp_core_melting,
                            core_lh_extracted,
                            max_core_lh,
                            cmb_conductivity,
                            # temperatures,
                            timestep,
                            core_density,
                            core_cp,
                            r_core,
                            label,
                        ],
                        f,
                    )
        core_values.cooling(temperatures, timestep, dr, i, cmb_conductivity)
        latent = core_values.latentlist
        core_lh_extracted = core_values.latent
        temperature_core = core_values.temperature
        # latent, core_lh_extracted, temperature_core = core_cooling(
        ## latent is now core.latentlist
        ## core_lh_extracted is now core.latent
        ## temperature_core = core.temperature
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