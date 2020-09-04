#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting of Temperatures and Cooling Rates

Two functions which return plots of 1) temperatures through time, varying with depth, and 2) cooling rate through time, varying with depth
"""

import numpy as np
import matplotlib.pyplot as plt
from pylab import cm
import matplotlib.colors as clr
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as plticker
import matplotlib.lines as mlines
import matplotlib
import matplotlib.font_manager as font_manager

import os.path
from os import path


"""## Setting up colourmaps, font paths etc. ##"""
# for work pc
#fontpath = '/nfs/see-fs-02_users/eememq/Downloads/Lato/Lato-Regular.ttf'

# for laptop
#fontpath = 'C:/Users/maeve/Downloads/Lato/Lato-Regular.ttf'

# turning this off, don't think we need to change the fonts and it's causing problems
# if path.exists('/nfs/see-fs-02_users/eememq/Downloads/Lato/Lato-Regular.ttf'):
#     print("On work pc")
#     fontpath = '/nfs/see-fs-02_users/eememq/Downloads/Lato/Lato-Regular.ttf'
# elif path.exists('C:/Users/maeve/Downloads/Lato/Lato-Regular.ttf'):
#     print("On laptop")
#     fontpath = 'C:/Users/maeve/Downloads/Lato/Lato-Regular.ttf'
# else:
#     print("not recognised workspace - please add fontpath")
    
# print(fontpath)

# prop = font_manager.FontProperties(fname=fontpath)
# matplotlib.rcParams['font.family'] = prop.get_name()

# If font can't be found:
# import matplotlib
#
#matplotlib.font_manager._rebuild()
#
#smooth cmap
custom_cmapy = clr.LinearSegmentedColormap.from_list('custom red/yellow', ['#143642','#C41230','#EC9A29'])
custom_cmap_20 = clr.LinearSegmentedColormap.from_list('custom red/yellow', ['#143642','#C41230','#EC9A29'], N=20)
custom_cmapx = custom_cmap_20 
cmaplist = [custom_cmapx(i) for i in range(custom_cmapx.N)]
# segmented cmap
#custom_cmapy = custom_cmapx.from_list('Custom cmap', cmaplist, custom_cmapx.N)

bw_cmap = cm.get_cmap('binary', 20) #greyscale colourmap to allow comparison of different parameters

import matplotlib.font_manager as font_manager

# Set the font dictionaries (for plot title and axis titles)
title_font = {'size':'16', 'color':'black', 'weight':'normal', 'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'size':'14'}

font_prop = font_manager.FontProperties(size=14)


myr = 3.1556926E13
#t_step = 2.0E11
#def million_years(x, pos):
#    "Converting from timesteps to myrs"
#    return int((x * t_step)/ myr)


def million_years(x, pos):
    "Converting from timesteps to myrs"
    value = (x * 1.0E11)/ myr
    value_rounded = round(value,-2)
    value_int = int(value_rounded)
    return value_int


class nf(float):
    def __repr__(self):
        s = f'{self:.1f}'
        return f'{self:.0f}' if s[-1] == '0' else s
    
def my_func(x, pos):
    return int(x * myr*-1)

def temperature_plot(temperatures, coretemp, Esquel_Depth, Imilac_Depth,Brenham1_Depth,Seymchan1_Depth,GlorM1_Depth,Admire_Depth, Brahin_Depth,Fukang_Depth, r_core, max_time, time_core_frozen, fully_frozen, r_planet,run_ID,save="y",timestep = 1E11,location='lower left'):
    """"
    function docstring
    Returns a heat map of depth vs time, with the colormap showing variation in temperature
    """
    myr = 3.1556926E13
    fig, ax = plt.subplots(figsize=(12,6))
    
    
    # Set the tick labels font
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14)
    formatter = FuncFormatter(million_years)
    ax.xaxis.set_major_formatter(formatter)
    im = ax.imshow(np.concatenate((temperatures[-1:0:-1,:],coretemp[-1:0:-1,:]),axis=0), aspect='auto', cmap=custom_cmapy) #used 'magma' #custom_cmap
    ticker_step = (100 * myr)/timestep
    loc = plticker.MultipleLocator(base=ticker_step) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel("Depth (km)")
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)

    #levels = [100, 200, 300, 400, 500, 593, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500] #contour lines - can look a little crowded
    lines = [100, 200, 300, 400, 500, 593, 700, 800, 1000, 1200, 1400,1500] #contour lines

    #cont_temps = plt.contour(np.concatenate((temperatures[-1:0:-1,:],coretemp[-1:0:-1,:]),axis=0), levels, colors=['r','r','r','w','r','w','r','r','r','r','r','r','r','r','r'])
    cont_temps = plt.contour(np.concatenate((temperatures[-1:0:-1,:],coretemp[-1:0:-1,:]),axis=0), lines, colors=['r','r','r','w','r','w','#143642','#143642','#143642','#143642','#143642','#143642','#143642'], linestyles=':')
    cont_temps.levels = [nf(val) for val in cont_temps.levels]
    fmt = '%r'
    plt.clabel(cont_temps,cont_temps.levels, fmt=fmt, fontsize=12, inline=1)
    #plt.subplots_adjust(top=0.8)
    #plot lines and text labels
    #plot Depth lines 
    if Esquel_Depth == 0 or Esquel_Depth == (r_core/1000) or Esquel_Depth is None:
        pass
    else:
        ax.plot([0,max_time/(timestep)],[Esquel_Depth, Esquel_Depth], lw=2, c='#0F8B8D', linestyle='--', label="Esquel")
        #plt.text((max_time/(10**11)/1.05),Esquel_Depth + 5,'Esquel', color= '#0F8B8D')

    if Imilac_Depth == 0 or Imilac_Depth == (r_core/1000) or Imilac_Depth is None:
        pass
    else:
        ax.plot([0,max_time/(timestep)],[Imilac_Depth,Imilac_Depth], lw=2, c='#0F8B8D', linestyle='-', label="Imilac")
        #plt.text((max_time/(10**11)/1.05),Imilac_Depth-2,'Imilac', color='#0F8B8D')            
    esq_line = mlines.Line2D([], [], color='#0F8B8D', linestyle='--',lw=2, label='Esquel formation depth')
    imi_line = mlines.Line2D([], [], color='#0F8B8D', linestyle='-',lw=2, label='Imilac formation depth')
    wid_line = mlines.Line2D([], [], color='w', linestyle=':',lw=2, label='Widmanstätten temperatures')                         
    plt.legend(handles=[imi_line, esq_line,wid_line],loc=location, fancybox=True, framealpha=0.3, fontsize=14) #shadow=True)
      
#    if Brenham1_Depth == 0 or Brenham1_Depth == (r_core/1000) or Brenham1_Depth is None:
#        pass
#    else:
#        ax.plot([0,max_time/(10**11)/2],[Brenham1_Depth,Brenham1_Depth], lw=2, c='#0F8B8D', linestyle='-')
#        plt.text((max_time/(10**11)/2.1),Brenham1_Depth-1,'Brenham', color='#0F8B8D')
#    if Seymchan1_Depth == 0 or Seymchan1_Depth == (r_core/1000) or Seymchan1_Depth is None:
#        pass
#    else:
#        ax.plot([0,max_time/(10**11)/2],[Seymchan1_Depth,Seymchan1_Depth], lw=2, c='#0F8B8D', linestyle='-')
#        plt.text((max_time/(10**11)/2.1),Seymchan1_Depth-1,'Seymchan', color='#0F8B8D')
#    if GlorM1_Depth == 0 or GlorM1_Depth == (r_core/1000) or GlorM1_Depth is None:
#        pass
#    else:
#        ax.plot([0,max_time/(10**11)/2],[GlorM1_Depth,GlorM1_Depth], lw=2, c='#0F8B8D', linestyle='-')
#        plt.text((max_time/(10**11)/2.1),GlorM1_Depth-1,'Glorietta Mountain', color='#0F8B8D')
#    if Admire_Depth == 0 or Admire_Depth == (r_core/1000) or Admire_Depth is None:
#        pass
#    else:
#        ax.plot([0,max_time/(10**11)/2],[Admire_Depth,Admire_Depth], lw=2, c='#0F8B8D', linestyle='-')
#        plt.text((max_time/(10**11)/2.1),Admire_Depth-1,'Admire', color='#0F8B8D')
#
#    if Brahin_Depth == 0 or Brahin_Depth == (r_core/1000) or Brahin_Depth is None:
#        pass
#    else:
#        ax.plot([0,max_time/(10**11)/2],[Brahin_Depth,Brahin_Depth], lw=2, c='#0F8B8D', linestyle='-')
#        plt.text((max_time/(10**11)/2.1),Brahin_Depth-1,'Brahin', color='#0F8B8D')
#
#    if Fukang_Depth == 0 or Fukang_Depth == (r_core/1000) or Fukang_Depth is None:
#        pass
#    else:
#        ax.plot([0,max_time/(10**11)/2],[Fukang_Depth,Fukang_Depth], lw=2, c='#0F8B8D', linestyle='-')
#        plt.text((max_time/(10**11)/2.1),Fukang_Depth-1,'Fukang', color='#0F8B8D')

    #plot core lines if frozen before max time 
    if time_core_frozen==0 or fully_frozen==0:
        ax.plot([0,max_time/(timestep)],[(r_planet/1000)-(r_core/1000),(r_planet/1000)-(r_core/1000)], lw=3, c="w", linestyle='-', alpha=0.4)
        plt.text(25,(r_planet/1000)-(r_core/1000),'CMB', color='w', alpha=0.5, fontsize=16)
        pass
    else:
        #core begins to freeze line
        ax.plot([time_core_frozen/(timestep),time_core_frozen/(timestep)],[((r_planet)/1000)-3,(r_core/1000)], lw=3, c="w",linestyle= '--', alpha=0.5)
        #core finishes freezing
        ax.plot([fully_frozen/(timestep),fully_frozen/(timestep)],[((r_planet)/1000)-3,(r_core/1000)], lw=3, c="w",linestyle= '--', alpha=0.5)
        #Core location
        ax.plot([0,max_time/(timestep)],[(r_planet/1000)-(r_core/1000),(r_planet/1000)-(r_core/1000)], lw=3, c="w", linestyle='-',alpha=0.4)
        plt.text(25,110,'CMB', color='w', alpha=0.5, fontsize=16)
        #Add text labelling period of core solidification
        middle_of_core_solidification = (((fully_frozen+time_core_frozen)/2))/(timestep)-4700
        plt.text(middle_of_core_solidification,((r_planet/1000) -15),'Core \nFreezes', color='w',fontsize=14,alpha=0.5)



    plt.title('Planetesimal temperatures through time', fontsize=18, pad=12)


    cb = fig.colorbar(im)
    cb.set_label('Temperature (K)', fontsize=14)
    cb.ax.tick_params(labelsize=14)
    if save == "y":
        plt.savefig('output_runs/temperature_' + str(run_ID) + '.pdf', format='pdf',bbox_inches='tight')
    else:
        pass
    return(plt.show())

# COOLING RATE

def cooling_rate_plot(dT_by_dt, dT_by_dt_core, Imilac_cooling_rate, Esquel_cooling_rate, Esquel_Depth, Imilac_Depth, max_time, time_core_frozen, fully_frozen, r_planet, r_core, temperatures, coretemp,run_ID,save="y",timestep = 1.0E11,location='lower left'):
    """
    Returns a plot of depth vs time, with colour varying with cooling rate
    """
    myr = 3.1556926E13
    fig, ax = plt.subplots(figsize=(12,6))

    im = ax.imshow(np.concatenate((dT_by_dt[-1:0:-1,:],dT_by_dt_core[-1:0:-1,:]),axis=0), aspect='auto',vmin=-1E-12 ,cmap=custom_cmapy) #'tab20b_r' #custom_cmapy
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14)
    formatter = FuncFormatter(million_years)
    ax.xaxis.set_major_formatter(formatter)
    
    ticker_step = (100 *myr)/timestep
    loc = plticker.MultipleLocator(base=ticker_step) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    
    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel("Depth (km)")
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)

    #Plot Imilac Cooling Rate Contour
    lines = [-(Imilac_cooling_rate)]
    cont_Im = plt.contour(np.concatenate((dT_by_dt[-1:0:-1,:],dT_by_dt_core[-1:0:-1,:]),axis=0), lines, colors='#143642', linestyles='-')
    #plt.clabel(cont_Im, fontsize=10, inline=1, lw=3)

    #Plot Esquel Cooling Rate Contour
    lines= [-(Esquel_cooling_rate)]
    cont_Esq = plt.contour(np.concatenate((dT_by_dt[-1:0:-1,:],dT_by_dt_core[-1:0:-1,:]),axis=0), lines, colors='#143642',linestyles='--')
    #plt.clabel(cont_Esq, fontsize=10, inline=1, lw=3)

    #Plot 593K contour
    lines=[593]
    cont593 = plt.contour(np.concatenate((temperatures[-1:0:-1,:],coretemp[-1:0:-1,:]),axis=0), lines, colors='w', linestyles=':')
    #plt.clabel(cont593, fontsize=10, inline=1)
    cont593.levels = [nf(val) for val in cont593.levels]
    fmt = '%r'
    plt.clabel(cont593,cont593.levels, fmt=fmt, fontsize=12, inline=1)

    #Plot 800K contour
    lines=[800]
    cont800 = plt.contour(np.concatenate((temperatures[-1:0:-1,:],coretemp[-1:0:-1,:]),axis=0), lines, colors='w',linestyles=':')
    cont800.levels = [nf(val) for val in cont800.levels]
    fmt = '%r'
    plt.clabel(cont800,cont800.levels, fmt=fmt, fontsize=12, inline=1)

    #plot lines and text labels
    #plot Depth lines if in mantle
    if Esquel_Depth == 0 or Esquel_Depth == (r_core/1000) or Esquel_Depth is None:
        pass
    else:
        ax.plot([0,max_time/(timestep)],[Esquel_Depth-0.5, Esquel_Depth-0.5], lw=2, c='#0F8B8D', linestyle='--')
        #plt.text((max_time/(10**11)/1.1),Esquel_Depth-1,'Esquel', color= '#0F8B8D')

    if Imilac_Depth == 0 or Imilac_Depth == (r_core/1000) or Imilac_Depth is None:
        pass
    else:
        ax.plot([0,max_time/(timestep)],[Imilac_Depth-0.5,Imilac_Depth-0.5], lw=2, c='#0F8B8D', linestyle='-')
        #plt.text((max_time/(10**11)/1.1),Imilac_Depth-1,'Imilac', color='#143642')
    esq_cr_cont = mlines.Line2D([], [], color='#143642', linestyle='--',lw=2, label='Esquel cooling rate')
    imi_cr_cont = mlines.Line2D([], [], color='#143642', linestyle='-',lw=2, label='Imilac cooling rate')
    esq_line = mlines.Line2D([], [], color='#0F8B8D', linestyle='--',lw=2, label='Esquel formation depth')
    imi_line = mlines.Line2D([], [], color='#0F8B8D', linestyle='-',lw=2, label='Imilac formation depth')
    wid_line = mlines.Line2D([], [], color='w', linestyle=':',lw=2, label='Widmanstätten temperatures')
                         
    plt.legend(handles=[imi_line,imi_cr_cont, esq_line,esq_cr_cont,wid_line],loc=location, fancybox=True, framealpha=0.3, fontsize=14) #shadow=True)
    #plot core lines if frozen before max time
    if time_core_frozen==0 or fully_frozen==0:
        ax.plot([0,max_time/(timestep)],[(r_planet/1000)-(r_core/1000),(r_planet/1000)-(r_core/1000)], lw=3, c="w", linestyle='-', alpha=0.4)
        plt.text(25,110,'CMB', color='w', alpha=0.5, fontsize=16)
        pass

    else:
        #core begins to freeze line
        ax.plot([time_core_frozen/(timestep),time_core_frozen/(timestep)],[((r_planet)/1000)-3,(r_core/1000)], lw=3, c="w",linestyle= '--', alpha=0.5)
        #core finishes freezing
        ax.plot([fully_frozen/(timestep),fully_frozen/(timestep)],[((r_planet)/1000)-3,(r_core/1000)], lw=3, c="w",linestyle= '--', alpha=0.5)
        #Core location
        ax.plot([0,max_time/(timestep)],[(r_planet/1000)-(r_core/1000),(r_planet/1000)-(r_core/1000)], lw=3, c="w", linestyle='-',alpha=0.4)
        plt.text(25,110,'CMB', color='w', alpha=0.5, fontsize=16)
        #Add text labelling period of core solidification
        middle_of_core_solidification = (((fully_frozen+time_core_frozen)/2))/(timestep)-4700
        plt.text(middle_of_core_solidification,((r_planet/1000) -15),'Core \nFreezes', color='w',fontsize=14,alpha=0.5)


    plt.title('Planetesimal cooling rates through time', fontsize=18, pad=12)
    fmt1 = plticker.FuncFormatter(my_func)
    cb = fig.colorbar(im, format=fmt1, extend='min')
    cb.set_label('Cooling Rate (K/Myr)', fontsize=14)
    cb.ax.tick_params(labelsize=14)
    cb.ax.invert_yaxis() 
    if save =="y":
        plt.savefig('output_runs/cooling_rate_' + str(run_ID) + '.pdf', format='pdf', bbox_inches='tight')
    else:
        pass
    plt.show()
  
    
############################################################################
############################################################################
############################################################################
############################################################################
# _______ ______  _____ _______ _____ _   _  _____ 
#|__   __|  ____|/ ____|__   __|_   _| \ | |/ ____|
#   | |  | |__  | (___    | |    | | |  \| | |  __ 
#   | |  |  __|  \___ \   | |    | | | . ` | | |_ |
#   | |  | |____ ____) |  | |   _| |_| |\  | |__| |
#   |_|  |______|_____/   |_|  |_____|_| \_|\_____|
#
############################################################################
############################################################################
############################################################################
############################################################################
# currently working on plotting curvature stuff
#
#def dT_by_dr_plot(dT_by_dr, dT_by_dr_core, max_time, time_core_frozen, fully_frozen, r_planet, r_core, temperatures, coretemp,run_ID):
#    """
#    Returns a plot of depth vs time, with colour varying with cooling rate
#    """
#    fig, ax = plt.subplots(figsize=(12,6))
#
#    im = ax.imshow(np.concatenate((dT_by_dr[-1:0:-1,:],dT_by_dr_core[-1:0:-1,:]),axis=0), aspect='auto',vmin=-1E-12 ,cmap='binary') #'tab20b_r' #custom_cmapy ,vmin=-1E-12
#    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
#        label.set_fontsize(14)
#    formatter = FuncFormatter(million_years)
#    ax.xaxis.set_major_formatter(formatter)
#    
#    ticker_step = (100 * 1000000 * 365 * 24 * 3600)/1E11
#    loc = plticker.MultipleLocator(base=ticker_step) # this locator puts ticks at regular intervals
#    ax.xaxis.set_major_locator(loc)
#    
#    ax.set_xlabel("Time (Myr)")
#    ax.set_ylabel("Depth (km)")
#    ax.xaxis.label.set_size(14)
#    ax.yaxis.label.set_size(14)
#                         
#
#    #plot core lines if frozen before max time
#    if time_core_frozen==0 or fully_frozen==0:
#        ax.plot([0,max_time/(10**11)],[(r_planet/1000)-(r_core/1000),(r_planet/1000)-(r_core/1000)], lw=3, c="w", linestyle='-', alpha=0.4)
#        plt.text(25,110,'CMB', color='w', alpha=0.5, fontsize=16)
#        pass
#
#    else:
#        #core begins to freeze line
#        ax.plot([time_core_frozen/(10**11),time_core_frozen/(10**11)],[((r_planet)/1000)-3,(r_core/1000)], lw=3, c="w",linestyle= '--', alpha=0.5)
#        #core finishes freezing
#        ax.plot([fully_frozen/(10**11),fully_frozen/(10**11)],[((r_planet)/1000)-3,(r_core/1000)], lw=3, c="w",linestyle= '--', alpha=0.5)
#        #Core location
#        ax.plot([0,max_time/(10**11)],[(r_planet/1000)-(r_core/1000),(r_planet/1000)-(r_core/1000)], lw=3, c="w", linestyle='-',alpha=0.4)
#        plt.text(25,110,'CMB', color='w', alpha=0.5, fontsize=16)
#        #Add text labelling period of core solidification
#        middle_of_core_solidification = (((fully_frozen+time_core_frozen)/2))/(10**11)-4700
#        plt.text(middle_of_core_solidification,((r_planet/1000) -15),'Core \nFreezes', color='w',fontsize=14,alpha=0.5)
#
#
#    plt.title('dT/dr', fontsize=18, pad=12)
#    fmt1 = plticker.FuncFormatter(my_func)
#    cb = fig.colorbar(im, format=fmt1, extend='min')
#    cb.set_label('dT/dr', fontsize=14)
#    cb.ax.tick_params(labelsize=14)
#    cb.ax.invert_yaxis() 
#    #plt.savefig('output_runs/cooling_rate_' + str(run_ID) + '.pdf', format='pdf', bbox_inches='tight')
#    plt.show()
#
#def dTbydr_testing(dT_by_dr, dT_by_dr_core, max_time, time_core_frozen, fully_frozen, r_planet, r_core, temperatures, coretemp,run_ID):
#    """
#    Returns a plot of depth vs time, with colour varying with cooling rate
#    """
#    fig, ax = plt.subplots(figsize=(20,10))
#
#    im = ax.imshow(np.concatenate((dT_by_dr[-1:0:-1,:],dT_by_dr_core[-1:0:-1,:]),axis=0), aspect='auto',vmin=-1E-12 ,cmap='binary') #'tab20b_r' #custom_cmapy
#
#    ax.set_xlabel("Time")
#    ax.set_ylabel("Depth (km)")
#
#
#    #plot core lines if frozen before max time
#    if time_core_frozen==0 or fully_frozen==0:
#        pass
#
#    else:
#        #core begins to freeze line
#        ax.plot([time_core_frozen/(10**11),time_core_frozen/(10**11)],[((r_planet)/1000)-3,0], lw=1, c="k",linestyle= '--')
#        #core finishes freezing
#        ax.plot([fully_frozen/(10**11),fully_frozen/(10**11)],[((r_planet)/1000)-3,0], lw=1, c="k",linestyle= '--')
#        #Core location
#        ax.plot([0,max_time/(10**11)/2],[(r_planet/1000)-(r_core/1000),(r_planet/1000)-(r_core/1000)], lw=1, c="k", linestyle='--')
#        #Add text labelling period of core solidification
#        middle_of_core_solidification = (((fully_frozen+time_core_frozen)/2))/(10**11)-4700
#        plt.text(middle_of_core_solidification,4,'Period of Core Solidification', color='w')
#
#
#
#    plt.title('dT/dr')
#
#    cb = fig.colorbar(im)
#    cb.set_label('dT/dr')
#    #plt.savefig('cooling_rate_' + str(run_ID) + '.pdf', format='pdf', dpi=1000)
#    plt.show()