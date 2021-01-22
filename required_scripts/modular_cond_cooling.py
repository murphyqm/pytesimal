#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 08:41:44 2020.

@author: eememq

"""

###
#########################################################
# RUN ID - MAKE SURE TO GIVE UNIQUE ID TO SAVE FIGS ETC #
#########################################################


def conductive_cooling(
    run_ID,
    folder,
    kappa=1.22100122100122e-06,
    B=0.000,
    model_type=17,
    plotting="None",
    save_array="n",
    save_csv="n",
    timestep=1e11,
    r_planet=250000.0,
    core_size_factor=0.5,
    reg_fraction=0.032,
    max_time=400,
    temp_core_melting=1200.0,
    olivine_cp=819.0,
    olivine_density=3341.0,
    return_vars="n",
    save_param_file="y",
    cmb_conductivity=3.0,
    core_cp=850.0,
    core_density=7800.0,
    temp_init=1600.0,
    temp_surface=250.0,
    core_latent_heat=270000.0,
    kappa_reg=5.0e-8,
    dr=1000.0,
    reg_percent="y",
    cond_constant="y",
    density_constant="y",
    heat_cap_constant="y",
    non_lin_term="y",
    record_timings="n",
    tests="n",
):
    """
    Conductive cooling model.

    Basic output is time for core to start freezing, time for core to end
    freezing, chosen B and k0 calculated from kappa in a filed called
    basic_output.pickle in the order:
        max_time,time_core_frozen,fully_frozen,B,k0_mantle,kappa

    mandatory arguments:

        run_ID - a unique ID to save output files under
        folder - a directory name to save output files in. If it does not
        match a current directory, a directory will be created.

    optional arguments:

        Physical Parameters
        kappa: default is 5E-7
            diffusivity that sets the conductivity or in the case of temp
            dependent conductivity, sets the k0_mantle for the equation

        B: default is 0.000
            set to a range of values between positive infinity and -0.0003 to
            change dependence on temperature


        model_type: default is 4.
            1: for constant conductivity
            2: for simple variable with linear function
            3: for more realistic conductivity case
            4: simple variable conductivity with separated components
            5: more realistic case with separated components
            7: constant conductivity approximated to analytical soln of sphere
            8: simple var conductivity with separated components but non-lin=0
            note - 6 currently does not work, was previous iteration of 7

        plotting: default is "None"
            "None": no plots produced
            "both": both temperature and cooling rate plots produced
            "temp": temperature plot
            "rate": cooling rate plot

        save_array: default is "n"
            "y": save array of points to plot later
            "n": do not save numpy array

        save_csv: default is "n"
            "y": save csv files of temperatures at variousdepths for plotting
            "n": do not save csv files. Data can be pulled from array above if
            that is set to "y".

        timestep: default is 1E11
            if Runtime overflow warnings are raised, reduce timestep to
            satisfy courant criterion

        r_planet: default is 200000 m
            given in m

        core size fraction: default is 0.5
            fraction of the total radius that is core

        reg_fraction: default is 0.0
            fraction of the total radius that is regolith. To match Bryson,
            set to 0.04

        max_time: default is 400 Myr
            This is the total time the model will run for. Suggested values
            for different radii are given below in a comment.

        save_param_file: default is "y"
            Select y if you want a text file output at the end of each run
            with parameters

        reg_percent: default is "y"
            Select "n" to define regolith as percentage of 200 km instead
    """
    import time
    import os

    start = time.time()

    compressed = "y"  # to save output arrays as compressed

    # if not os.path.isdir("output_runs"):
    #     os.mkdir("output_runs")

    if not os.path.isdir(str(folder)):
        os.mkdir(str(folder))

    meteorite_depthlist_ID = "12aug"  # Only need to change if you change list
    # of meteorites for depth calculations

    import numpy as np
    import csv

    # import pdb
    # import sys
    import pickle

    """## Defining Variables"""

    # r_planet = 200000.0 # m, usually 200000.0
    # core_size_factor = 0.5 # fraction of total radius usually 0.5
    r_core = (r_planet) * core_size_factor  # m

    if model_type == 7:
        r_core = 0.0001
    else:
        pass

    kappa = cmb_conductivity / (olivine_density * olivine_cp)
    # dr = 1000.0 # m

    # temp_init = 1600.0 # K
    # temp_surface = 250.0 # K usually 250 K
    # temp_core_melting = 1200.0 # K

    # kappa = 5E-7 # 3.0485E-11 #5E-7
    # m^2/s usually 5E-7; can be 1.515151E-6 to set cmb = 3;
    # 5.827E-7 when B= 0.001,1.3635e-06 for constant comparison case

    # kappa_reg = 5.0E-8 # m^2/s
    # reg_fraction = 0.0
    if reg_percent == "n":
        reg_thickness = (reg_fraction * 200000.0) * 1.0  # m original=0.04, *1
    else:
        reg_thickness = (reg_fraction * r_planet) * 1.0

    # core_density = 7800.0 # kg/m^3
    # olivine_density = 3300.0 # kg/m^3
    # olivine_cp = 600.0 # J/kg/K ## where did this figure come from?
    # core_cp = 850.0 # J/kg/K
    # core_latent_heat = 270000.0 # J/kg
    # cmb_conductivity = 3.0 # W/m/K

    p = olivine_density
    c = olivine_cp

    # Basic set up:
    k0_mantle = cmb_conductivity  # 0.99
    k0_reg = kappa_reg * p * c  # 0.099
    k0_core = k0_mantle  # 0.99
    # k_core = kappa * core_cp * core_density # 3.315

    # Values from Haack 1990
    # k0_mantle = 3.0
    # k0_reg = 0.2
    # k0_core =  601

    # timestep = 1E11 # sec

    # sys.exit()

    """

    # Possible sensible values
    k0_mantle = 3.000 #W/m/K
    k0_reg = 0.0300 #W/m/K
    k0_core =  30.000 #w/m/K
    """

    print(run_ID)
    # setting suitable max times for certain radii
    if r_planet >= 100000:
        max_time = 200  # Myr
    if r_planet >= 200000:
        max_time = 400
    if r_planet >= 300000:
        max_time = 600
    if r_planet >= 400000:
        max_time = 800
    if r_planet >= 500000:
        max_time = 1000
    if r_planet >= 600000:
        max_time = 1200
    if r_planet >= 650000:
        max_time = 1600

    print(max_time)
    myr = 3.1556926e13
    # sys.exit()

    max_time = max_time * myr  # sec

    """## Defining Variable Arrays"""

    # set up arrays for the core and the mantle
    radii = np.arange(r_core, r_planet, dr)
    core = np.arange(0, r_core - dr + 0.5 * dr, dr)

    # Set list of timesteps
    times = np.arange(0, max_time + 0.5 * timestep, timestep)

    if model_type == 10:  # added "9 or 1"
        # Set up thermal diffusivity array, keeping track of regolith
        kappas = np.ones_like(radii) * kappa
        where_regolith = np.ones_like(radii)
        for i, r in enumerate(radii):
            d = r_planet - r
            if d <= reg_thickness:
                kappas[i] = kappa_reg
                where_regolith[i] = 0

    else:
        kappas = np.ones_like(radii) * kappa
        where_regolith = np.ones_like(radii)
        for i, r in enumerate(radii):
            d = r_planet - r
            if d < reg_thickness:
                kappas[i] = kappa_reg
                where_regolith[i] = 0

    # Setup thermal conductivity array for mantle, regolith - core is
    # not included in the radii array
    k_0 = np.ones_like(radii) * k0_mantle
    #    for i, r in enumerate(radii):
    #        d = r_planet - r
    #    #    d_mantle = r_planet - r_core
    #        if d < reg_thickness:
    #            k_0[i] = k0_reg
    #    if d > d_mantle:
    #        k_0[i] = k0_core

    # Temperature array
    temperatures = np.zeros((radii.size, times.size))

    # Core temperature array
    coretemp = np.zeros((core.size, times.size))

    # empty list of latent heats
    latent = []
    print("Variables have been set up, importing timestepping function")

    """## Temperature Timestepping"""

    # import temp_timestepping as t_s
    # pdb.set_trace()

    if model_type == 7:
        import modular_temp_timestepping as mtt

        # same as above but with separated variables
        (
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
        ) = mtt.comp_to_analytical_sep_terms(
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
        )

    elif model_type == 17:
        import modular_temp_timestepping as mtt

        (
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
        ) = mtt.discretisation(
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
            cond_constant,
            density_constant,
            heat_cap_constant,
            non_lin_term,
            is_a_test="n",
            i_choice=126228,  # 126228
            TESTING=tests,
        )

    elif model_type == 18:
        import modular_temp_timestepping as mtt

        (
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
        ) = mtt.simple_discretisation(
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
            cond_constant,
            density_constant,
            heat_cap_constant,
            non_lin_term,
        )

    else:
        print("Please assign valid model type number")

    print("Time stepping completed, finding time of core solidification")
    """## Finding the Timing of Core Solidification"""

    import core_cooling as c_c

    (
        core_frozen,
        times_frozen,
        time_core_frozen,
        fully_frozen,
    ) = c_c.core_freezing(
        coretemp, max_time, times, latent, temp_core_melting, timestep
    )

    """## Differentiation of Temperatures"""

    # calculate rate of change of temperatures
    dT_by_dt = np.gradient(temperatures, timestep, axis=1)
    dT_by_dt_core = np.gradient(coretemp, timestep, axis=1)

    print("Saving arrays if requested")

    if (save_array == "y") and (compressed == "n"):
        np.save(
            str(folder)
            + "/"
            + str(run_ID)
            + "temperatures_array.npy",
            temperatures,
        )
        np.save(
            str(folder)
            + "/"
            + str(run_ID)
            + "coretemp_array.npy",
            coretemp,
        )
        np.save(
            str(folder)
            + "/"
            + str(run_ID)
            + "dT_by_dt_array.npy",
            dT_by_dt,
        )
        np.save(
            str(folder)
            + "/"
            + str(run_ID)
            + "dT_by_dt_core.npy",
            dT_by_dt_core,
        )

    elif (save_array == "y") and (compressed == "y"):
        np.savez_compressed(
            str(folder)
            + "/"
            + str(run_ID)
            + "_total_arrays.npz",
            temperatures=temperatures,
            coretemp=coretemp,
            dT_by_dt=dT_by_dt,
            dT_by_dt_core=dT_by_dt_core,
        )
    else:
        pass

    # file prefix: "output_runs/"+ str(folder)+"/"+str(run_ID)+

    """#Get indices of cooling rates between T = 593 and T = 800 # """

    print("Importing cooling_calc module and calculating formation depths")
    """## Calculation of Cooling Rates and Depths"""
    import cooling_calc
    import cooling_rate_data as c_r_d

    d_im = 147  # cz diameter in nm
    d_esq = 158  # cz diameter in nm
    Imilac_cooling_rate = cooling_calc.to_seconds(
        cooling_calc.cz_cooling(d_im)
    )
    Esquel_cooling_rate = cooling_calc.to_seconds(
        cooling_calc.cz_cooling(d_esq)
    )
    Brenham1_cr = cooling_calc.to_seconds(c_r_d.Brenham1)
    Glorietta_Mountain1_cr = cooling_calc.to_seconds(
        c_r_d.Glorietta_Mountain1
    )
    Seymchan1_cr = cooling_calc.to_seconds(c_r_d.Seymchan1)

    Dora_cr = cooling_calc.to_seconds(c_r_d.Dora1)
    Finmarken_cr = cooling_calc.to_seconds(c_r_d.Finmarken1)
    Giroux_cr = cooling_calc.to_seconds(c_r_d.Giroux1)
    SBend_cr = cooling_calc.to_seconds(c_r_d.South_Bend1)
    Springwater_cr = cooling_calc.to_seconds(c_r_d.Springwater1)
    Admire_cr = cooling_calc.to_seconds(c_r_d.Admire)
    Brahin_cr = cooling_calc.to_seconds(c_r_d.Brahin)
    Fukang_cr = cooling_calc.to_seconds(c_r_d.Fukang)

    import new_crit_depth as c_d

    ##########
    # DEPTHS #
    ##########

    Esquel_Depth = (
        c_d.Critical_Depth(
            Esquel_cooling_rate,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Imilac_Depth = (
        c_d.Critical_Depth(
            Imilac_cooling_rate,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Esq_timing = (
        c_d.Critical_Depth(
            Esquel_cooling_rate,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[3]
    Im_timing = (
        c_d.Critical_Depth(
            Imilac_cooling_rate,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[3]
    Esq_result = (
        c_d.Critical_Depth(
            Esquel_cooling_rate,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[1]
    Im_result = (
        c_d.Critical_Depth(
            Imilac_cooling_rate,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[1]
    with open(
        str(folder)
        + "/"
        + str(run_ID)
        + "Im_Esq_result.pickle",
        "wb",
    ) as f:
        pickle.dump([Esq_result, Im_result], f)
    print("Im: " + str(Im_result))
    print("Esq: " + str(Esq_result))

    Brenham1_Depth = (
        c_d.Critical_Depth(
            Brenham1_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    GlorM1_Depth = (
        c_d.Critical_Depth(
            Glorietta_Mountain1_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Seymchan1_Depth = (
        c_d.Critical_Depth(
            Seymchan1_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]

    Dora_Depth = (
        c_d.Critical_Depth(
            Dora_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Finmarken_Depth = (
        c_d.Critical_Depth(
            Finmarken_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Giroux_Depth = (
        c_d.Critical_Depth(
            Giroux_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    SBend_Depth = (
        c_d.Critical_Depth(
            SBend_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Springwater_Depth = (
        c_d.Critical_Depth(
            Springwater_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Admire_Depth = (
        c_d.Critical_Depth(
            Admire_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Brahin_Depth = (
        c_d.Critical_Depth(
            Brahin_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    Fukang_Depth = (
        c_d.Critical_Depth(
            Fukang_cr,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]

    # other timings #####
    if record_timings == "y":
        Brenham1_t = (
            c_d.Critical_Depth(
                Brenham1_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        GlorM1_t = (
            c_d.Critical_Depth(
                Glorietta_Mountain1_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        Seymchan1_t = (
            c_d.Critical_Depth(
                Seymchan1_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]

        Dora_t = (
            c_d.Critical_Depth(
                Dora_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        Finmarken_t = (
            c_d.Critical_Depth(
                Finmarken_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        Giroux_t = (
            c_d.Critical_Depth(
                Giroux_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        SBend_t = (
            c_d.Critical_Depth(
                SBend_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        Springwater_t = (
            c_d.Critical_Depth(
                Springwater_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        Admire_t = (
            c_d.Critical_Depth(
                Admire_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        Brahin_t = (
            c_d.Critical_Depth(
                Brahin_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]
        Fukang_t = (
            c_d.Critical_Depth(
                Fukang_cr,
                temperatures,
                dT_by_dt,
                radii,
                r_planet,
                core_size_factor,
                time_core_frozen,
                fully_frozen,
            )
        )[3]

        with open(
            str(folder) + "/" + str(run_ID) + "times.pickle",
            "wb",
        ) as f:
            pickle.dump(
                [
                    Esq_timing,
                    Im_timing,
                    Brenham1_t,
                    GlorM1_t,
                    Seymchan1_t,
                    Dora_t,
                    Finmarken_t,
                    Giroux_t,
                    SBend_t,
                    Springwater_t,
                    Admire_t,
                    Brahin_t,
                    Fukang_t,
                ],
                f,
            )
    else:
        pass

    #################################
    # Testing Olivine Cooling Rates #
    #################################
    # Miyamoto1997_low = cooling_calc.to_seconds(20000000)
    # Miyamoto1997_high = cooling_calc.to_seconds(100000000)
    # Miyamoto1997_v_low = cooling_calc.to_seconds(200000)
    Omolon1 = cooling_calc.to_seconds(20)
    Omolon2 = cooling_calc.to_seconds(40)

    # om1 depth - was Miyamoto1997_low
    ol_depth_low = (
        c_d.Critical_Depth_ol(
            Omolon1,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]

    # om1 timing - was Miyamoto1997_high
    ol_depth_high = (
        c_d.Critical_Depth_ol(
            Omolon1,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[3]
    # Om 2 depth, was Miyamoto1997_v_low
    ol_depth_v_low = (
        c_d.Critical_Depth_ol(
            Omolon2,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[0]
    # Om 2 timing, was Esquel_cooling_rate
    Esquel_Depth_test = (
        c_d.Critical_Depth_ol(
            Omolon2,
            temperatures,
            dT_by_dt,
            radii,
            r_planet,
            core_size_factor,
            time_core_frozen,
            fully_frozen,
        )
    )[3]

    print("saving depths")
    if save_array == "y" or record_timings == "y":
        with open(
            str(folder)
            + "/"
            + str(run_ID)
            + "depths.pickle",
            "wb",
        ) as f:
            pickle.dump(
                [
                    Esquel_Depth,
                    Imilac_Depth,
                    Brenham1_Depth,
                    GlorM1_Depth,
                    Seymchan1_Depth,
                    Dora_Depth,
                    Finmarken_Depth,
                    Giroux_Depth,
                    SBend_Depth,
                    Springwater_Depth,
                    Admire_Depth,
                    Brahin_Depth,
                    Fukang_Depth,
                    ol_depth_low,
                    ol_depth_high,
                    ol_depth_v_low,
                    Esquel_Depth_test,
                    Imilac_cooling_rate,
                    Esquel_cooling_rate,
                ],
                f,
            )
            with open(
                str(folder)
                + "/"
                + str(run_ID)
                + "input_params.pickle",
                "wb",
            ) as f:
                pickle.dump(
                    [
                        r_core,
                        max_time,
                        time_core_frozen,
                        fully_frozen,
                        r_planet,
                        dr,
                        core_size_factor,
                        reg_fraction,
                    ],
                    f,
                )
    else:
        pass

    """## Plotting of Temperatures and Cooling Rates"""

    if plotting == "both":
        print("Beginning plotting both")
        import temp_plotting_formatted

        temp_plotting_formatted.temperature_plot(
            temperatures,
            coretemp,
            Esquel_Depth,
            Imilac_Depth,
            Brenham1_Depth,
            Seymchan1_Depth,
            GlorM1_Depth,
            Admire_Depth,
            Brahin_Depth,
            Fukang_Depth,
            r_core,
            max_time,
            time_core_frozen,
            fully_frozen,
            r_planet,
            run_ID,
            folder=folder,
        )

        temp_plotting_formatted.cooling_rate_plot(
            dT_by_dt,
            dT_by_dt_core,
            Imilac_cooling_rate,
            Esquel_cooling_rate,
            Esquel_Depth,
            Imilac_Depth,
            max_time,
            time_core_frozen,
            fully_frozen,
            r_planet,
            r_core,
            temperatures,
            coretemp,
            run_ID,
            folder=folder,
        )

    elif plotting == "temp":
        print("Beginning plotting temp")
        import temp_plotting_formatted

        temp_plotting_formatted.temperature_plot(
            temperatures,
            coretemp,
            Esquel_Depth,
            Imilac_Depth,
            Brenham1_Depth,
            Seymchan1_Depth,
            GlorM1_Depth,
            Admire_Depth,
            Brahin_Depth,
            Fukang_Depth,
            r_core,
            max_time,
            time_core_frozen,
            fully_frozen,
            r_planet,
            run_ID,
            folder=folder,
            timestep=timestep,
        )

    elif plotting == "rate":
        print("Beginning plotting cooling rate")
        import temp_plotting_formatted

        temp_plotting_formatted.cooling_rate_plot(
            dT_by_dt,
            dT_by_dt_core,
            Imilac_cooling_rate,
            Esquel_cooling_rate,
            Esquel_Depth,
            Imilac_Depth,
            max_time,
            time_core_frozen,
            fully_frozen,
            r_planet,
            r_core,
            temperatures,
            coretemp,
            run_ID,
            folder=folder,
        )

    elif plotting == "None":
        print("No plotting requested")
        pass

    else:
        pass

    # Saving temperature list for a certain r
    # #### Currently commenting out this entire section to test npy sizes
    #

    if save_csv == "y":
        print("Saving csv files")

        with open(
            str(folder)
            + "/temp_list_mid_mantle_"
            + str(run_ID)
            + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(temp_list_mid_mantle)

        with open(
            str(folder)
            + "/temp_list_cmb_5_"
            + str(run_ID)
            + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(temp_list_cmb_5)

        # temp_list_shal may have to be replaced with temp_list_10

        if model_type == 7 or model_type == 17 or model_type == 18:
            with open(
                str(folder)
                + "/temp_list_10_"
                + str(run_ID)
                + ".csv",
                "w",
            ) as f:
                writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
                writer.writerow(temp_list_shal)

        else:
            with open(
                str(folder)
                + "/temp_list_10_"
                + str(run_ID)
                + ".csv",
                "w",
            ) as f:
                writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
                writer.writerow(temp_list_shal)

    else:
        pass

    if (save_csv == "y") and (
        model_type == 5 or 4 or 7 or 8 or 9 or 10 or 11 or 17 or 18
    ):
        print("saving time output to csv")
        with open(
            str(folder)
            + "/time_output_"
            + str(run_ID)
            + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(times)
    else:
        pass

    if model_type == 5:
        with open(
            str(folder) + "/A_1_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(A_1list)

        with open(
            str(folder) + "/B_1_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(B_1list)

        with open(
            str(folder) + "/C_1_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(C_1list)

        with open(
            str(folder) + "/delt_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(delt_list)

        # CMB:
        with open(
            str(folder) + "/A_1_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(A_1listcmb)

        with open(
            str(folder) + "/B_1_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(B_1listcmb)

        with open(
            str(folder) + "/C_1_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(C_1listcmb)

        with open(
            str(folder) + "/delt_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(delt_listcmb)

        # shallow:

        with open(
            str(folder) + "/A_1_shal" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(A_1listshal)

        with open(
            str(folder) + "/B_1_shal" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(B_1listshal)

        with open(
            str(folder) + "/C_1_shal" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(C_1listshal)

        with open(
            str(folder)
            + "/delt_shal"
            + str(run_ID)
            + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(delt_listshal)

    elif (save_csv == "y") and (
        model_type == 4 or 7 or 8 or 9 or 10 or 11 or 17 or 18
    ):
        with open(
            str(folder) + "/A_1_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(A_1list)

        with open(
            str(folder) + "/B_1_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(B_1list)

        with open(
            str(folder) + "/C_1_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(C_1list)

        with open(
            str(folder) + "/delt_mm" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(delt_list)

        # CMB:
        with open(
            str(folder) + "/A_1_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(A_1listcmb)

        with open(
            str(folder) + "/B_1_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(B_1listcmb)

        with open(
            str(folder) + "/C_1_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(C_1listcmb)

        with open(
            str(folder) + "/delt_cmb" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(delt_listcmb)

        # shallow:

        with open(
            str(folder) + "/A_1_shal" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(A_1listshal)

        with open(
            str(folder) + "/B_1_shal" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(B_1listshal)

        with open(
            str(folder) + "/C_1_shal" + str(run_ID) + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(C_1listshal)

        with open(
            str(folder)
            + "/delt_shal"
            + str(run_ID)
            + ".csv",
            "w",
        ) as f:
            writer = csv.writer(f, delimiter="\n", quoting=csv.QUOTE_NONE)
            writer.writerow(delt_listshal)
    elif model_type == 1:
        pass
    else:
        pass

    ###################

    if save_array == "y":
        with open(
            str(folder)
            + "/"
            + str(run_ID)
            + "other_vars.pickle",
            "wb",
        ) as f:
            pickle.dump(
                [
                    r_core,
                    max_time,
                    time_core_frozen,
                    fully_frozen,
                    r_planet,
                    dr,
                ],
                f,
            )
        with open(
            str(folder)
            + "/"
            + str(run_ID)
            + "basic_output.pickle",
            "wb",
        ) as f:
            pickle.dump(
                [
                    max_time,
                    time_core_frozen,
                    fully_frozen,
                    B,
                    k0_mantle,
                    kappa,
                    Esquel_Depth,
                    Imilac_Depth,
                    Esq_timing,
                    Im_timing,
                ],
                f,
            )

    else:
        with open(
            str(folder)
            + "/"
            + str(run_ID)
            + "basic_output.pickle",
            "wb",
        ) as f:
            pickle.dump(
                [
                    max_time,
                    time_core_frozen,
                    fully_frozen,
                    B,
                    k0_mantle,
                    kappa,
                    Esquel_Depth,
                    Imilac_Depth,
                    Esq_timing,
                    Im_timing,
                ],
                f,
            )
    print("Saving basic pickles")

    #    time_check1 = dt_new(k0_mantle,B,temp_init,p,c,dr)
    #    time_check2 = dt_new(k0_mantle,B,temp_surface,p,c,dr)
    #    print("Actual timestep:", timestep, "\n", "Courant criterion at CMB:",
    # time_check1, "\n", "Courant criterion at surface:", time_check2, "\n")
    print("k0_mantle:", k0_mantle, "\nk0_reg:", k0_reg, "\nk0_core:", k0_core)

    end = time.time()
    print("Time taken:", end - start, "seconds")

    if save_param_file == "y":
        print("Saving final parameters file... nearly there!")
        f = open(
            str(folder) + "/params_" + str(run_ID) + ".txt",
            "w",
        )
        f.write(
            "PARAMETERS \n##############################"
            + "\nrun_ID = "
            + str(run_ID)
            + "\nmodel_type = "
            + str(model_type)
            + "\nmeteorite_depthlist_ID = "
            + str(meteorite_depthlist_ID)
            + "\nr_planet = "
            + str(r_planet)
            + "\ncore_size_factor = "
            + str(core_size_factor)
            + "\nr_core = "
            + str(r_core)
            + "\ndr = "
            + str(dr)
            + "\ntemp_init = "
            + str(temp_init)
            + "\ntemp_surface = "
            + str(temp_surface)
            + "\ntemp_core_melting = "
            + str(temp_core_melting)
            + "\nkappa = "
            + str(kappa)
            + "\nkappa_reg = "
            + str(kappa_reg)
            + "\nreg_thickness = "
            + str(reg_thickness)
            + "\ncore_density = "
            + str(core_density)
            + "\nolivine_density = "
            + str(olivine_density)
            + "\nolivine_cp = "
            + str(olivine_cp)
            + "\ncore_cp = "
            + str(core_cp)
            + "\ncore_latent_heat = "
            + str(core_latent_heat)
            + "\ncmb_conductivity = "
            + str(cmb_conductivity)
            + "\np = "
            + str(p)
            + "\nc = "
            + str(c)
            + "\nB = "
            + str(B)
            + "\nk0_mantle = "
            + str(k0_mantle)
            + "\nk0_reg = "
            + str(k0_reg)
            + "\nk0_core =  "
            + str(k0_core)
            + "\ntimestep = "
            + str(timestep)
            + "\ntime taken (seconds) = "
            + str(end - start)
            + "\ncore begins to freeze = "
            + str(((time_core_frozen) / myr))
            + "\ncore frozen = "
            + str(fully_frozen / myr)
            + "\nEsquel depth = "
            + str(Esquel_Depth)
            + " at "
            + str(Esq_timing)
            + "\nImilac depth = "
            + str(Imilac_Depth)
            + " at "
            + str(Im_timing)
        )
        f.close()
    else:
        pass

    print("Done ", str(run_ID) + "! On to the next job...")
    print(
        "\ncore begins to freeze = "
        + str(((time_core_frozen) / myr))
        + "\nEsquel depth = "
        + str(Esquel_Depth)
        + " at "
        + str(Esq_timing)
        + "\nImilac depth = "
        + str(Imilac_Depth)
        + " at "
        + str(Im_timing)
        + "\ncore frozen = "
        + str((fully_frozen) / myr)
    )

    if return_vars == "y":
        begins_to_freeze = time_core_frozen
        finished_freezing = fully_frozen
        return (
            begins_to_freeze,
            finished_freezing,
            Esquel_Depth,
            Esq_timing,
            Imilac_Depth,
            Im_timing,
        )
    else:
        pass
