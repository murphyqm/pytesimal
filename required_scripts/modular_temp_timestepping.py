"""Isothermal core cooling and FTCS discretisation for mantle."""

import numpy as np

# import sys


# Background info on functions used:

# Conductivity
# constructed, from Su 2018 (Cp) and Xu et al., 2004

# def conductivity(x):
#    y = (80.4205952575632*(1.3193574749943*x**(-0.5) + 0.977581998039333 -
# 28361.7649315602/x**2 - 6.05745211527538e-5/x**3)*(1/x)**0.5)
#    return y
# def conductivity_prime(x):
#    y_prime = (80.4205952575632*(-0.659678737497148*x**(-1.5) +
# 56723.5298631204/x**3 + 0.000181723563458261/x**4)*(1/x)**0.5 -
# 40.2102976287816*(1.3193574749943*x**(-0.5) + 0.977581998039333 -
# 28361.7649315602/x**2 - 6.05745211527538e-5/x**3)*(1/x)**0.5/x)
#    return y_prime

# Density with temperature
# From Su, 2018

# def alpha(T):
#    """
#    Function for the thermal expansion coefficient from Su et al., 2018
#    """
#    alpha = 3.304E-5 + (0.742E-8 * T) -0.538 *(T**-2)
#    return alpha
#
# def rho(T, rho_0=3000.0,T0=295.0):
#    """
#    Function for temperature dependent density, defined above and using beta
# from Su et al., 2018
#
#    Defaults for reference rho and T chosen from Bryson et al., 2015 with T0
# set to room temperature
#    """
#    rho = rho_0 - alpha(T)*rho_0*(T-T0)
#    return rho

# Heat capacity
# Su et al., 2018

# def heat_cap(T):
#    cp =  (995.1 + (1343*((T)**(-0.5))) - (2.887*(10**7)*((T)**(-2))) -
# (6.166*(10**(-2))* (T)**(-3)))
#    return cp

# for the basic case: OLD VERSION, OUTDATED
# def K(k0, B, T):
#     K_new = k0 * (1.0 + B*T)
#     return K_new

# def dKdT(k0,B):
#     dKdT_new = k0 * B
#     return dKdT_new


def core_cooling(
    latent,
    i,
    dr,
    temperature_core,
    temp_core_melting,
    core_lh_extracted,
    max_core_lh,
    cmb_conductivity,
    temperatures,
    timestep,
    core_density,
    core_cp,
    r_core,
):
    """Core cooling model."""
    # Cool the liquid or the solid
    if (temperature_core > temp_core_melting) or (
        core_lh_extracted >= max_core_lh
    ):

        temperature_core = temperature_core - (
            3.0
            * cmb_conductivity
            * ((temperatures[0, i] - temperatures[1, i]) / dr)
            * timestep
        ) / (core_density * core_cp * r_core)

    else:
        core_lh_extracted = (
            core_lh_extracted
            + (4.0 * np.pi * r_core ** 2)
            * cmb_conductivity
            * ((temperatures[0, i] - temperatures[1, i]) / dr)
            * timestep
        )
        latent.append(
            core_lh_extracted
        )  # add to the latent heat list for each tstep while core solidifies

    return latent, core_lh_extracted, temperature_core


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
):
    """
    Finite difference solver with variable k.

    Uses variable heat capacity, conductivity, density as required.

    Uses diffusivity for regolith layer.

    ## will change to record 1/3 and 2/3rds down into mantle... at some point
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

    # testing some values
    # print("cond:")
    # print(conductivity(300))
    # print("dens:")
    # print(rho(300))
    # print("heat cap:")
    # print(heat_cap(300))

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
        )  # this might break things
        # ask Andrew if this should be i or i-1!
        # print(A_1,B_1,C_1)

        latent, core_lh_extracted, temperature_core = core_cooling(
            latent,
            i,
            dr,
            temperature_core,
            temp_core_melting,
            core_lh_extracted,
            max_core_lh,
            cmb_conductivity,
            temperatures,
            timestep,
            core_density,
            core_cp,
            r_core,
        )
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


# simple discretisation for simple variable case

def simple_discretisation(
    latent,
    temp_init,
    temp_core_melting,
    temp_surface,
    cmb_conductivity,
    p,
    c,
    B,
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
    cond_constant="n",
    density_constant="y",
    heat_cap_constant="y",
    non_lin_term="y",
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
    k0 = cmb_conductivity
    cond_constant = "n"  # this must be variable, can be supressed with B =0
    if cond_constant == "y":

        def conductivity(x):
            y = cmb_conductivity
            return y

        def conductivity_prime(x):
            y_prime = 0
            return y_prime

    else:
        # this is the original conductivity function
        # def conductivity(x):
        #     y = k0 * (1.0 + B*x)
        #     return y
        # def conductivity_prime(x):
        #     y_prime = k0 * B
        #     return y_prime
        # this is the new one!
        def conductivity(x):
            y = k0 + (B * x)
            return y

        def conductivity_prime(x):
            y_prime = B
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
            Calculate coef of thermal expansion.

            Function for the thermal expansion coefficient from Su et al., 2018
            """
            alpha = 3.304e-5 + (0.742e-8 * T) - 0.538 * (T ** -2.0)
            return alpha

        def rho(T, rho_0=3341.0, T0=300.0):
            """
            Calculate temperature dependent density.

            Defined above and using beta from Su et al., 2018

            Defaults for reference rho and T chosen from Bryson et al., 2015
            with T0 set to room temperature
            """
            rho = rho_0 - alpha(T) * rho_0 * (T - T0)
            return rho

    # testing some values
    # print("cond:")
    # print(conductivity(300))
    # print("dens:")
    # print(rho(300))
    # print("heat cap:")
    # print(heat_cap(300))

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
        )  # this might break things

        latent, core_lh_extracted, temperature_core = core_cooling(
            latent,
            i,
            dr,
            temperature_core,
            temp_core_melting,
            core_lh_extracted,
            max_core_lh,
            cmb_conductivity,
            temperatures,
            timestep,
            core_density,
            core_cp,
            r_core,
        )
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


def comp_to_analytical_sep_terms(
    latent,
    temp_init,
    temp_core_melting,
    temp_surface,
    cmb_conductivity,
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
    p,
    c,
    B,
    k_0,
):
    """
    Finite difference solver with constant thermal conductivity, k.

    With possibility of exporting/printing temp info at a certain depth/tstep

    attempting dT/dr = 0 at boundary

    """
    B = 0
    r_core = 0.0001
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

    def K(k0, B, x):
        y = k0 + (B * x)
        return y

    def dKdT(k0, B):
        y_prime = B
        return y_prime

    for i in range(1, len(times[1:]) + 1):

        for j in range(1, len(radii[1:-1]) + 1):

            A_1 = []
            B_1 = []
            C_1 = []

            A_1 = 0  # (timestep*(1.0/(p*c)))*(dKdT(k_0[j],B) * (
            # (temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(
            # 4.0 * dr**2.0))
            B_1 = (timestep * (1.0 / (p * c))) * (
                (K(k_0[j], B, temperatures[j, i - 1]) / (radii[j] * dr))
                * (temperatures[j + 1, i - 1] - temperatures[j - 1, i - 1])
            )
            C_1 = (timestep * (1.0 / (p * c))) * (
                (K(k_0[j], B, temperatures[j, i - 1]) / dr ** 2.0)
                * (
                    temperatures[j + 1, i - 1]
                    - 2 * temperatures[j, i - 1]
                    + temperatures[j - 1, i - 1]
                )
            )
            temperatures[j, i] = temperatures[j, i - 1] + A_1 + B_1 + C_1

            checkpoint_mm = radii[int(len(radii) / 2.0)]
            checkpoint_cmb = radii[int(len(radii) - (len(radii) - 1))]
            checkpoint_shal = radii[int(len(radii) - 5)]
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
        # temperatures[0,i] = temperatures[0,i-1]
        temperatures[0, i] = (
            4.0 * (temperatures[1, i]) - temperatures[2, i]
        ) / 3.0
        # for above see eq 6.31
        # http://folk.ntnu.no/leifh/teaching/tkt4140/._main056.html
        coretemp[:, i] = temperatures[0, i]

        latent, core_lh_extracted, temperature_core = core_cooling(
            latent,
            i,
            dr,
            temperature_core,
            temp_core_melting,
            core_lh_extracted,
            max_core_lh,
            cmb_conductivity,
            temperatures,
            timestep,
            core_density,
            core_cp,
            r_core,
        )
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
