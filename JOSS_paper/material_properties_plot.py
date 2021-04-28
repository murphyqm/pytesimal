#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure of T-dependent properties for JOSS paper

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.lines as mlines
from context import mantle_properties


temperatures = np.arange(250.0,1601.0, 10.0)

(vmantle_conductivity,
 vmantle_heatcap,
 vmantle_density) = mantle_properties.set_up_mantle_properties(
    cond_constant='n',
    density_constant='n',
    heat_cap_constant='n'
)

(cmantle_conductivity,
 cmantle_heatcap,
 cmantle_density) = mantle_properties.set_up_mantle_properties(
    cond_constant='y',
    density_constant='y',
    heat_cap_constant='y'
)

# font
hfont = {'fontname':'Lato'}

# Colour palette
# from colorbrewer 2.0, 5-class PuOr
constant_k = '#e66101'
var_k = '#fdb863'
constant_pcp = '#5e3c99'
var_cpc = '#b2abd2'
grey = '#636363'

x = temperatures
y_kv = vmantle_conductivity.getk(temperatures)
y_kc = cmantle_conductivity.getk(temperatures)

y_cpv = vmantle_heatcap.getcp(temperatures)*vmantle_density.getrho(temperatures)
y_cpc = cmantle_heatcap.getcp(temperatures)*cmantle_density.getrho(temperatures)

# plotting figure
plt.rcParams["figure.figsize"] = (6,4)

ax = plt.gca()
ax.plot(x, y_kv, color=constant_k, linewidth=3, alpha=0.9)
ax.plot((x[0],x[-1]), (y_kc, y_kc), color=constant_k, linestyle='dashed', alpha=0.7, linewidth=3)

ax2 = ax.twinx()
ax2.plot(x, y_cpv, color=constant_pcp, linewidth=3, alpha=0.9)
ax2.plot((x[0],x[-1]), (y_cpc, y_cpc), color=constant_pcp, linestyle='dashed', alpha=0.7, linewidth=3)

# ax2.spines['right'].set_color(constant_pcp)
ax2.yaxis.label.set_color(constant_pcp)
ax2.tick_params(axis='y', colors=constant_pcp)
ax2.set_ylabel("Volumetric Heat Capacity (J m$^{-3}$ K$^{-1})$", **hfont)

#a x2.spines['left'].set_color(constant_k)
ax.yaxis.label.set_color(constant_k)
ax.tick_params(axis='y', colors=constant_k)
ax.set_ylabel("Conductivity (W m$^{-1}$ K$^{-1}$)", **hfont)

# make scientific notation prettier
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1,1))
ax2.yaxis.set_major_formatter(formatter)

# setting proxy artists for legend
solid_line = mlines.Line2D([], [], color=grey, label='$T$ dependent', linewidth=3)
dashed_line = mlines.Line2D([], [], color=grey, linestyle='dashed', alpha=0.7, label='Constant', linewidth=3)
plt.legend(handles=[solid_line, dashed_line], prop={'family':'Lato'})

ax.set_xlabel("Temperature (K)", **hfont)
ax.set_title("Constant and $T$-dependent material properties", **hfont)

plt.savefig('material_properties.pdf',)