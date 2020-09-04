"""
This module solves the radial 1D heat diffusion equation iteratively using the finite difference method, and produces a core cooling model

"""

import numpy as np
#import sys
#import numba
#from numba import jit

#@jit#(nopython=True)
def timestepping(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas):
    """
    Finite difference solver with constant thermal conductivity, k

    With possibility of exporting/printing temp info at a certain depth/timestep
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_10=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3.0) * core_density * core_latent_heat
    core_lh_extracted = 0.0


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # eq 2 of Bryson SI
            temperatures[j, i] = (kappas[j] * timestep * (
                    (1.0 / (radii[j] * dr))*(temperatures[j+1,i-1]-temperatures[j-1,i-1]) +
                    (1.0 / dr**2.0) * (temperatures[j+1,i-1] - 2.0*temperatures[j,i-1] + temperatures[j-1, i-1]) )) \
                    + temperatures[j, i-1]
            checkpoint1 = radii[int(len(radii)/2.0)]
#            checkpoint2 = times[int(len(times)/2)]
            if radii[j] == checkpoint1: #and times[i] == checkpoint2:
#                print(temperatures[j,i])
                temp_list_mid_mantle.append(temperatures[j,i])
            checkpoint2 = radii[int(len(radii)-(len(radii)-1))]
            if radii[j] == checkpoint2:
                temp_list_cmb_5.append(temperatures[j,i])
            checkpoint3 = radii[int(len(radii)-5)]
            if radii[j] == checkpoint3:
                temp_list_10.append(temperatures[j,i])


        #set top and bottom temperatures as fixed

        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_10,temp_list_cmb_5


#next function


def core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core):
    """
    Core cooling model
    How should this be influenced by thermally variable conductivity??
    """
        # Cool the liquid or the solid
    if (temperature_core > temp_core_melting) or (core_lh_extracted >= max_core_lh):


        temperature_core = temperature_core - (3.0*cmb_conductivity * ((temperatures[0,i]-temperatures[1,i])/dr) * timestep) \
                           / (core_density * core_cp * r_core)

    else:
        core_lh_extracted = core_lh_extracted + (4.0*np.pi*r_core**2) * cmb_conductivity * \
            ((temperatures[0,i]-temperatures[1,i])/dr) * timestep
        latent.append(core_lh_extracted) #add to the latent heat list for each timestep while core solidifies

    return latent, core_lh_extracted, temperature_core


def timestepping_variablek(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c, B, k_0):
    """
    Finite difference solver with variable k following simple equation for k and dk
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_10=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
    core_lh_extracted = 0.0


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity

            temperatures[j,i] = temperatures[j, i-1] + \
(timestep*(1.0/(p*c)) * ( dKdT(k_0[j],B) * ((temperatures[j+1, i-1] - \
           temperatures[j-1, i-1])**2.0)/(4.0 * dr**2) + \
(K(k_0[j],B,temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]) + \
(K(k_0[j],B,temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2.0*temperatures[j,i-1] + temperatures[j-1, i-1]) \
))
            checkpoint1 = radii[int(len(radii)/2.0)]
            #checkpoint1 = 150000.0
#            checkpoint2 = times[int(len(times)/2)]
            if radii[j] == checkpoint1: #and times[i] == checkpoint2:
#                print(temperatures[j,i])
                temp_list_mid_mantle.append(temperatures[j,i])
            checkpoint2 = radii[int(len(radii)-(len(radii)-1))]
            if radii[j] == checkpoint2:
                temp_list_cmb_5.append(temperatures[j,i])
            checkpoint3 = radii[int(len(radii)-5)]
            if radii[j] == checkpoint3:
                temp_list_10.append(temperatures[j,i])

        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = K(k_0[j],B,temperatures[0,i]) # this might break things
        # ask Andrew if this should be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_10,temp_list_cmb_5

def K(k0, B, T):
    K_new = k0 * (1.0 + B*T)
    return K_new

def dKdT(k0,B):
    dKdT_new = k0 * B
    return dKdT_new

def k_zhang(T):
    k = 1.216 + (2836.0/(T))
    return k

def dk_zhangdT(T):
    dkdT = -2836.0/(T**2)
    return dkdT


#def timestepping_variablek_zhang(latent,temp_init, temp_core_melting, temp_surface,
#                 cmb_conductivity, temperatures, dr, coretemp, timestep,
#                 core_density, core_cp, r_core, core_latent_heat, radii,
#                 times, kappas, p, c):
#    """
#    Finite difference solver with variable k following simple equation for k and dk
#    """
#    temp_list=[temp_init]
#    temperatures[:,0] = temp_init
#    temperature_core = temp_init
#    coretemp[:,0] = temp_init
#    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
#    core_lh_extracted = 0.0
#
#
#    for i in range(1, len(times[1:])+1):
#
#        for j in range(1, len(radii[1:-1])+1):
#
#            # equation with variable thermal conductivity
#            #getting following errors:
#            #overflow encountered in double scalars
#            #invalid value encountered in double scalars
#            #invalid value encountered in less_equal
#            #core freezes after max time
#            # it actually produces output if you remove the timestep (but obviously incorrect)
#
#            temperatures[j,i] = temperatures[j, i-1] + \
#(timestep*(1/(p*c)) * ( dk_zhangdT(temperatures[j,i-1]) * ((temperatures[j+1, i-1] - \
#           temperatures[j-1, i-1])**2)/(4 * dr**2) + \
#(k_zhang(temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]) + \
#(k_zhang(temperatures[j,i-1])/dr**2) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]) \
#))
##            checkpoint1 = radii[int(len(radii)/2)]
#            checkpoint1 = 150000.0
##            checkpoint2 = times[int(len(times)/2)]
#            if radii[j] == checkpoint1: #and times[i] == checkpoint2:
##                print(temperatures[j,i])
#                temp_list.append(temperatures[j,i])
#
#        #set top and bottom temperatures as fixed
#        temperatures[-1,i] = temp_surface
#        temperatures[0,i] = temperature_core
#        coretemp[:,i] = temperatures[0,i]
#        cmb_conductivity = k_zhang(temperatures[0,i])
#
#        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
#    return temperatures, coretemp, latent, temp_list

##############################
# Piecewise functions for k #
#############################
def k_real(T):
    a = 6.589203095220635E-6
    b = 4.485
    c = 298.0
    k_realistic = np.piecewise(T, [T<673.0, T>=673.0], [lambda x: (a * (x**2.0)),lambda x: (b*((c/x)**0.5))])
    return k_realistic

def dkdT_real(T):
    a = 6.589203095220635E-6
    b = 4.485
    c = 298.0
    dkdT_realistic = np.piecewise(T, [T<673.0, T>=673.0], [lambda x: (2*a*x), lambda x: (((-c*b)/(2.0 * (x**2)))*(c/x)**(-0.5))])
    return dkdT_realistic

# to sub in: (k_real(temperatures[j,i-1]))
# (dkdT_real(temperatures[j,i-1]))

def conductivity(x):
    y = 80.4205952575632*(1.3193574749943*x**(-0.5) + 0.977581998039333 - 28361.7649315602/x**2 - 6.05745211527538e-5/x**3)*(1/x)**0.5
    return y
def conductivity_prime(x):
    y_prime = 80.4205952575632*(-0.659678737497148*x**(-1.5) + 56723.5298631204/x**3 + 0.000181723563458261/x**4)*(1/x)**0.5 - 40.2102976287816*(1.3193574749943*x**(-0.5) + 0.977581998039333 - 28361.7649315602/x**2 - 6.05745211527538e-5/x**3)*(1/x)**0.5/x
    return y_prime

def heat_capacity_function(x):
    heat_capacity = (995.1 + (1343*((x)**(-0.5))) - (2.887*(10**7)*((x)**(-2))) - (6.166*(10**(-2))* (x)**(-3)))
    return heat_capacity

def timestepping_variablek_combo(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c):
    """
    Finite difference solver with variable k using combined heat capacity and conductivity equations
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_10=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
    core_lh_extracted = 0.0


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)

            temperatures[j,i] = temperatures[j, i-1] + \
(timestep*(1.0/(p*c)) * ( conductivity_prime(temperatures[j, i-1]) * ((temperatures[j+1, i-1] - \
           temperatures[j-1, i-1])**2.0)/(4.0 * dr**2.0) + \
(conductivity(temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]) + \
(conductivity(temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2.0*temperatures[j,i-1] + temperatures[j-1, i-1]) \
))
            checkpoint1 = radii[int(len(radii)/2.0)]
            #checkpoint1 = 150000.0
#            checkpoint2 = times[int(len(times)/2)]
            if radii[j] == checkpoint1: #and times[i] == checkpoint2:
#                print(temperatures[j,i])
                temp_list_mid_mantle.append(temperatures[j,i])
            checkpoint2 = radii[int(len(radii)-(len(radii)-1))]
            if radii[j] == checkpoint2:
                temp_list_cmb_5.append(temperatures[j,i])
            checkpoint3 = radii[int(len(radii)-5)]
            if radii[j] == checkpoint3:
                temp_list_10.append(temperatures[j,i])

        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = conductivity(temperatures[0,i])
        # should this be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_10,temp_list_cmb_5


def timestepping_variablek_sep_terms(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c, B, k_0):
    """
    Finite difference solver with variable k following simple equation for k and dk, separating terms to compare
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            A_1 = (timestep*(1.0/(p*c)))*(dKdT(k_0[j],B) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2.0))
            B_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
            C_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))
            temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(2.0*len(radii)/3.0)]
            checkpoint_shal = radii[int(len(radii)/3.0)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass


        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = K(k_0[j],B,temperatures[0,i]) # this might break things
        # ask Andrew if this should be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal


# function #5
def timestepping_variablek_sep_terms_realistic(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c):
    """
    Finite difference solver with variable k from an experimentally derived function, separating the different terms
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            A_1 = (timestep*(1.0/(p*c)))*(conductivity_prime(temperatures[j, i-1]) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2.0))
            B_1 = (timestep*(1.0/(p*c)))*((conductivity(temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
            C_1 = (timestep*(1.0/(p*c)))*((conductivity(temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))
            temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            checkpoint_shal = radii[int(len(radii)-5)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass
        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = conductivity(temperatures[0,i]) # this might break things
        # ask Andrew if this should be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal


def comp_to_analytical_timestepping(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas):
    """
    Finite difference solver with constant thermal conductivity, k

    With possibility of exporting/printing temp info at a certain depth/timestep
    """
    r_core = 0.001
    temp_list_mid_mantle=[temp_init]
    temp_list_10=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
    core_lh_extracted = 0.0


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # eq 2 of Bryson SI
            temperatures[j, i] = (kappas[j] * timestep * (
                    (1.0 / (radii[j] * dr))*(temperatures[j+1,i-1]-temperatures[j-1,i-1]) +
                    (1.0 / dr**2) * (temperatures[j+1,i-1] - 2.0*temperatures[j,i-1] + temperatures[j-1, i-1]) )) \
                    + temperatures[j, i-1]
            checkpoint1 = radii[int(len(radii)/2)]
#            checkpoint2 = times[int(len(times)/2)]
            if radii[j] == checkpoint1: #and times[i] == checkpoint2:
#                print(temperatures[j,i])
                temp_list_mid_mantle.append(temperatures[j,i])
            checkpoint2 = radii[int(len(radii)-(len(radii)-1))]
            if radii[j] == checkpoint2:
                temp_list_cmb_5.append(temperatures[j,i])
            checkpoint3 = radii[int(len(radii)-5)]
            if radii[j] == checkpoint3:
                temp_list_10.append(temperatures[j,i])


        #set top and bottom temperatures as fixed

        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperatures[0,i-1]
        coretemp[:,i] = temperatures[0,i]

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_10,temp_list_cmb_5

def comp_to_analytical_sep_terms(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c, B, k_0):
    """
    Finite difference solver with constant thermal conductivity, k

    With possibility of exporting/printing temp info at a certain depth/timestep

    attempting dT/dr = 0 at boundary

    """
    B = 0
    r_core = 0.0001
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):
        #temperatures[0,i-1] = temperatures[0,i+1] # maybe here? not sure// that didn't work

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            A_1 = (timestep*(1.0/(p*c)))*(dKdT(k_0[j],B) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2.0))
            B_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
            C_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))
            temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            checkpoint_shal = radii[int(len(radii)-5)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass


        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        #temperatures[0,i] = temperatures[0,i-1]
        temperatures[0,i] = (4.0*(temperatures[1,i]) - temperatures[2,i])/3.0
        # for above see eq 6.31 http://folk.ntnu.no/leifh/teaching/tkt4140/._main056.html
        coretemp[:,i] = temperatures[0,i]


        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal


def non_lin_zero(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c, B, k_0):
    """
    Same as separated terms with variable k, but with non-linear term set to zero
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            # non linear term
            A_1 = 0.00 #(timestep*(1.0/(p*c)))*(dKdT(k_0[j],B) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2))
            # geometric term
            B_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
            # linear term
            C_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2.0*temperatures[j,i-1] + temperatures[j-1, i-1]))
            temperatures[j,i] = temperatures[j, i-1] + B_1 + C_1

            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            checkpoint_shal = radii[int(len(radii)-5)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass


        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = K(k_0[j],B,temperatures[0,i]) # this might break things
        # ask Andrew if this should be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal

def timestepping_with_cmb(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas):
    """
    Finite difference solver with constant thermal conductivity, k

    With possibility of exporting/printing temp info at a certain depth/timestep
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_10=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
    core_lh_extracted = 0.0
    cmb_conductivity = k0_mantle


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # eq 2 of Bryson SI
            temperatures[j, i] = (kappas[j] * timestep * (
                    (1.0 / (radii[j] * dr))*(temperatures[j+1,i-1]-temperatures[j-1,i-1]) +
                    (1.0 / dr**2.0) * (temperatures[j+1,i-1] - 2.0*temperatures[j,i-1] + temperatures[j-1, i-1]) )) \
                    + temperatures[j, i-1]
            checkpoint1 = radii[int(len(radii)/2.0)]
#            checkpoint2 = times[int(len(times)/2)]
            if radii[j] == checkpoint1: #and times[i] == checkpoint2:
#                print(temperatures[j,i])
                temp_list_mid_mantle.append(temperatures[j,i])
            checkpoint2 = radii[int(len(radii)-(len(radii)-1))]
            if radii[j] == checkpoint2:
                temp_list_cmb_5.append(temperatures[j,i])
            checkpoint3 = radii[int(len(radii)-5)]
            if radii[j] == checkpoint3:
                temp_list_10.append(temperatures[j,i])


        #set top and bottom temperatures as fixed

        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_10,temp_list_cmb_5

# exploring how to include regolith layer
def timestepping_variablek_sep_terms_w_regolith(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c, B, k_0,where_regolith,kappa_reg):
    """
    Finite difference solver with variable k following simple equation for k and dk, separating terms to compare
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            if where_regolith[j] == 1:

                A_1 = (timestep*(1.0/(p*c)))*(dKdT(k_0[j],B) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2.0))
                B_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
                C_1 = (timestep*(1.0/(p*c)))*((K(k_0[j],B,temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))

                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            elif where_regolith[j] == 0:

                A_1 = 0
                B_1 = (timestep)*((kappa_reg/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
                C_1 = (timestep)*((kappa_reg/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))

                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

#                temperatures[j, i] = (kappa_reg * timestep * (
#                    (1.0 / (radii[j] * dr))*(temperatures[j+1,i-1]-temperatures[j-1,i-1]) +
#                    (1.0 / dr**2.0) * (temperatures[j+1,i-1] - 2.0*temperatures[j,i-1] + temperatures[j-1, i-1]) )) \
#                    + temperatures[j, i-1]

#            elif where_regolith[j] == 0:
#
#                A_1 = 0
#                B_1 = kappas[j] * timestep * (1.0 / (radii[j] * dr))*(temperatures[j+1,i-1]-temperatures[j-1,i-1])
#
#                C_1 = kappas[j] * timestep * (1.0 / dr**2.0) * (temperatures[j+1,i-1] - 2.0*temperatures[j,i-1] + temperatures[j-1, i-1])
#
#                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            else:
                print("Regolith setup has failed!")
                break


            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            checkpoint_shal = radii[int(len(radii)-5)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass


        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = K(k_0[j],B,temperatures[0,i])


        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal

def timestepping_variablek_sep_terms_realistic_with_regolith(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c,where_regolith,kappa_reg):
    """
    Finite difference solver with variable k from an experimentally derived function, separating the different terms
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            if where_regolith[j] == 1:

                A_1 = (timestep*(1.0/(p*c)))*(conductivity_prime(temperatures[j, i-1]) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2.0))
                B_1 = (timestep*(1.0/(p*c)))*((conductivity(temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
                C_1 = (timestep*(1.0/(p*c)))*((conductivity(temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))
                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            elif where_regolith[j] == 0:

                A_1 = 0
                B_1 = (timestep)*((kappa_reg/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
                C_1 = (timestep)*((kappa_reg/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))

                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            checkpoint_shal = radii[int(len(radii)-5)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass
        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = conductivity(temperatures[0,i]) # this might break things
        # ask Andrew if this should be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal

def adaptive_tstep_timestepping_variablek_sep_terms_realistic_with_regolith(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, c,where_regolith,kappa_reg):
    """
    Finite difference solver with variable k from an experimentally derived function, separating the different terms
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            if where_regolith[j] == 1:

                A_1 = (timestep*(1.0/(p*c)))*(conductivity_prime(temperatures[j, i-1]) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2.0))
                B_1 = (timestep*(1.0/(p*c)))*((conductivity(temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
                C_1 = (timestep*(1.0/(p*c)))*((conductivity(temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))
                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            elif where_regolith[j] == 0:

                A_1 = 0
                B_1 = (timestep)*((kappa_reg/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
                C_1 = (timestep)*((kappa_reg/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))

                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            checkpoint_shal = radii[int(len(radii)-5)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass
        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = conductivity(temperatures[0,i]) # this might break things
        # ask Andrew if this should be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal


def timestepping_variableCp_variablek_sep_terms_realistic_with_regolith(latent,temp_init, temp_core_melting, temp_surface,
                 cmb_conductivity, temperatures, dr, coretemp, timestep,
                 core_density, core_cp, r_core, core_latent_heat, radii,
                 times, kappas, p, where_regolith,kappa_reg):
    """
    Finite difference solver with variable k from an experimentally derived function, separating the different terms

    Uses variable heat capacity as well as conductivity
    """
    temp_list_mid_mantle=[temp_init]
    temp_list_shal=[temp_init]
    temp_list_cmb_5=[temp_init]
    temperatures[:,0] = temp_init
    temperature_core = temp_init
    coretemp[:,0] = temp_init
    max_core_lh = 4.0/3.0 * np.pi * (r_core**3) * core_density * core_latent_heat
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


    for i in range(1, len(times[1:])+1):

        for j in range(1, len(radii[1:-1])+1):

            # equation with variable thermal conductivity
            #getting following errors:
            #overflow encountered in double scalars
            #invalid value encountered in double scalars
            #invalid value encountered in less_equal
            #core freezes after max time
            # it actually produces output if you remove the timestep (but obviously incorrect)
            A_1 = []
            B_1 = []
            C_1 = []

            if where_regolith[j] == 1:

                A_1 = (timestep*(1.0/(p* heat_capacity_function(temperatures[j, i-1]))))*(conductivity_prime(temperatures[j, i-1]) * ((temperatures[j+1, i-1] - temperatures[j-1, i-1])**2)/(4.0 * dr**2.0))

                B_1 = (timestep*(1.0/(p*heat_capacity_function(temperatures[j, i-1]))))*((conductivity(temperatures[j,i-1])/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))

                C_1 = (timestep*(1.0/(p*heat_capacity_function(temperatures[j, i-1]))))*((conductivity(temperatures[j,i-1])/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))
                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            elif where_regolith[j] == 0:

                A_1 = 0
                B_1 = (timestep)*((kappa_reg/(radii[j]*dr)) * (temperatures[j+1, i-1] - temperatures[j-1, i-1]))
                C_1 = (timestep)*((kappa_reg/dr**2.0) * (temperatures[j+1, i-1] -2*temperatures[j,i-1] + temperatures[j-1, i-1]))

                temperatures[j,i] = temperatures[j, i-1] + A_1 + B_1 + C_1

            checkpoint_mm = radii[int(len(radii)/2.0)]
            checkpoint_cmb = radii[int(len(radii)-(len(radii)-1))]
            checkpoint_shal = radii[int(len(radii)-5)]
            if (radii[j] == checkpoint_mm):
                temp_list_mid_mantle.append(temperatures[j,i])
                A_1list.append(A_1)
                B_1list.append(B_1)
                C_1list.append(C_1)
                delt_list.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_cmb):
                temp_list_cmb_5.append(temperatures[j,i])
                A_1listcmb.append(A_1)
                B_1listcmb.append(B_1)
                C_1listcmb.append(C_1)
                delt_listcmb.append(((temperatures[j,i-1])-(temperatures[j,i])))

            elif (radii[j] == checkpoint_shal):
                temp_list_shal.append(temperatures[j,i])
                A_1listshal.append(A_1)
                B_1listshal.append(B_1)
                C_1listshal.append(C_1)
                delt_listshal.append(((temperatures[j,i-1])-(temperatures[j,i])))
            else:
                pass
        #set top and bottom temperatures as fixed
        temperatures[-1,i] = temp_surface
        temperatures[0,i] = temperature_core
        coretemp[:,i] = temperatures[0,i]
        cmb_conductivity = conductivity(temperatures[0,i]) # this might break things
        # ask Andrew if this should be i or i-1!

        latent, core_lh_extracted, temperature_core = core_cooling(latent, i, dr, temperature_core, temp_core_melting, core_lh_extracted, max_core_lh, cmb_conductivity, temperatures, timestep, core_density, core_cp, r_core)
    return temperatures, coretemp, latent, temp_list_mid_mantle,temp_list_shal,temp_list_cmb_5,A_1list,B_1list,C_1list,delt_list,A_1listcmb,B_1listcmb,C_1listcmb,delt_listcmb,A_1listshal,B_1listshal,C_1listshal,delt_listshal
