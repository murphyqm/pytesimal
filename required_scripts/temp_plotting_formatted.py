#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting of Temperatures and Cooling Rates.

Two functions which return plots of 1) temperatures through time, varying with
depth, and 2) cooling rate through time, varying with depth
"""

import numpy as np
import matplotlib.pyplot as plt
from pylab import cm
import matplotlib.colors as clr
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as plticker
import matplotlib.lines as mlines
import matplotlib.font_manager as font_manager

# import os.path
# from os import path


"""## Setting up colourmaps ##"""

# need to tidy this - lots of these aren't used/uneccessary
# also think tstep is hardcoded - need to fix
# look at more recent modular plotting functions and build similar with this
# low on to-do list
custom_cmapy = clr.LinearSegmentedColormap.from_list(
    "custom red/yellow", ["#143642", "#C41230", "#EC9A29"]
)
custom_cmap_20 = clr.LinearSegmentedColormap.from_list(
    "custom red/yellow", ["#143642", "#C41230", "#EC9A29"], N=20
)
custom_cmapx = custom_cmap_20
cmaplist = [custom_cmapx(i) for i in range(custom_cmapx.N)]
# segmented cmap
# custom_cmapy =custom_cmapx.from_list('Custom cmap', cmaplist, custom_cmapx.N)

bw_cmap = cm.get_cmap(
    "binary", 20
)  # greyscale colourmap to allow comparison of different parameters


# Set the font dictionaries (for plot title and axis titles)
title_font = {
    "size": "16",
    "color": "black",
    "weight": "normal",
    "verticalalignment": "bottom",
}  # Bottom vertical alignment for more space
axis_font = {"size": "14"}

font_prop = font_manager.FontProperties(size=14)


myr = 3.1556926e13


def million_years(x, pos):
    """Convert from timesteps to myrs."""
    value = (x * 1.0e11) / myr
    value_rounded = round(value, -2)
    value_int = int(value_rounded)
    return value_int


class nf(float):
    """Format floats."""

    def __repr__(self):
        """Magic method."""
        s = f"{self:.1f}"
        return f"{self:.0f}" if s[-1] == "0" else s


def my_func(x, pos):
    """Fix Myr format."""
    return int(x * myr * -1)


def temperature_plot(
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
    folder="output_runs",
    save="y",
    timestep=1e11,
    location="lower left",
):
    """
    Temperature heatmap.

    Returns a heat map of depth vs time, with the colormap showing variation in
    temperature
    """
    myr = 3.1556926e13
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set the tick labels font
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(14)
    formatter = FuncFormatter(million_years)
    ax.xaxis.set_major_formatter(formatter)
    im = ax.imshow(
        np.concatenate(
            (temperatures[-1:0:-1, :], coretemp[-1:0:-1, :]), axis=0
        ),
        aspect="auto",
        cmap=custom_cmapy,
    )  # used 'magma' #custom_cmap
    ticker_step = (100 * myr) / timestep
    loc = plticker.MultipleLocator(
        base=ticker_step
    )  # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel("Depth (km)")
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)

    # levels = [100, 200, 300, 400, 500, 593, 700, 800, 900, 1000, 1100, 1200,
    # 1300, 1400, 1500] #contour lines - can look a little crowded
    lines = [
        100,
        200,
        300,
        400,
        500,
        593,
        700,
        800,
        1000,
        1200,
        1400,
        1500,
    ]  # contour lines

    # cont_temps = plt.contour(np.concatenate((temperatures[-1:0:-1,:],
    # coretemp[-1:0:-1,:]),axis=0), levels, colors=['r','r','r','w','r','w',
    # 'r','r','r','r','r','r','r','r','r'])
    cont_temps = plt.contour(
        np.concatenate(
            (temperatures[-1:0:-1, :], coretemp[-1:0:-1, :]), axis=0
        ),
        lines,
        colors=[
            "r",
            "r",
            "r",
            "w",
            "r",
            "w",
            "#143642",
            "#143642",
            "#143642",
            "#143642",
            "#143642",
            "#143642",
            "#143642",
        ],
        linestyles=":",
    )
    cont_temps.levels = [nf(val) for val in cont_temps.levels]
    fmt = "%r"
    plt.clabel(cont_temps, cont_temps.levels, fmt=fmt, fontsize=12, inline=1)
    # plt.subplots_adjust(top=0.8)
    # plot lines and text labels
    # plot Depth lines
    if (
        Esquel_Depth == 0
        or Esquel_Depth == (r_core / 1000)
        or Esquel_Depth is None
    ):
        pass
    else:
        ax.plot(
            [0, max_time / (timestep)],
            [Esquel_Depth, Esquel_Depth],
            lw=2,
            c="#0F8B8D",
            linestyle="--",
            label="Esquel",
        )
        # plt.text((max_time/(10**11)/1.05),Esquel_Depth + 5,'Esquel',
        # color= '#0F8B8D')

    if (
        Imilac_Depth == 0
        or Imilac_Depth == (r_core / 1000)
        or Imilac_Depth is None
    ):
        pass
    else:
        ax.plot(
            [0, max_time / (timestep)],
            [Imilac_Depth, Imilac_Depth],
            lw=2,
            c="#0F8B8D",
            linestyle="-",
            label="Imilac",
        )
        # plt.text((max_time/(10**11)/1.05),Imilac_Depth-2,'Imilac',
        # color='#0F8B8D')
    esq_line = mlines.Line2D(
        [],
        [],
        color="#0F8B8D",
        linestyle="--",
        lw=2,
        label="Esquel formation depth",
    )
    imi_line = mlines.Line2D(
        [],
        [],
        color="#0F8B8D",
        linestyle="-",
        lw=2,
        label="Imilac formation depth",
    )
    wid_line = mlines.Line2D(
        [],
        [],
        color="w",
        linestyle=":",
        lw=2,
        label="Widmanstätten temperatures",
    )
    plt.legend(
        handles=[imi_line, esq_line, wid_line],
        loc=location,
        fancybox=True,
        framealpha=0.3,
        fontsize=14,
    )  # shadow=True)

    # plot core lines if frozen before max time
    if time_core_frozen == 0 or fully_frozen == 0:
        ax.plot(
            [0, max_time / (timestep)],
            [
                (r_planet / 1000) - (r_core / 1000),
                (r_planet / 1000) - (r_core / 1000),
            ],
            lw=3,
            c="w",
            linestyle="-",
            alpha=0.4,
        )
        plt.text(
            25,
            (r_planet / 1000) - (r_core / 1000),
            "CMB",
            color="w",
            alpha=0.5,
            fontsize=16,
        )
        pass
    else:
        # core begins to freeze line
        ax.plot(
            [time_core_frozen / (timestep), time_core_frozen / (timestep)],
            [((r_planet) / 1000) - 3, (r_core / 1000)],
            lw=3,
            c="w",
            linestyle="--",
            alpha=0.5,
        )
        # core finishes freezing
        ax.plot(
            [fully_frozen / (timestep), fully_frozen / (timestep)],
            [((r_planet) / 1000) - 3, (r_core / 1000)],
            lw=3,
            c="w",
            linestyle="--",
            alpha=0.5,
        )
        # Core location
        ax.plot(
            [0, max_time / (timestep)],
            [
                (r_planet / 1000) - (r_core / 1000),
                (r_planet / 1000) - (r_core / 1000),
            ],
            lw=3,
            c="w",
            linestyle="-",
            alpha=0.4,
        )
        plt.text(25, 110, "CMB", color="w", alpha=0.5, fontsize=16)
        # Add text labelling period of core solidification
        middle_of_core_solidification = (
            ((fully_frozen + time_core_frozen) / 2)
        ) / (timestep) - 4700
        plt.text(
            middle_of_core_solidification,
            ((r_planet / 1000) - 15),
            "Core \nFreezes",
            color="w",
            fontsize=14,
            alpha=0.5,
        )

    plt.title("Planetesimal temperatures through time", fontsize=18, pad=12)

    cb = fig.colorbar(im)
    cb.set_label("Temperature (K)", fontsize=14)
    cb.ax.tick_params(labelsize=14)
    if save == "y":
        plt.savefig(
            str(folder) + "/temperature_" + str(run_ID) + ".pdf",
            format="pdf",
            bbox_inches="tight",
        )
    else:
        pass
    return plt.show()


# COOLING RATE


def cooling_rate_plot(
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
    folder="output_runs",
    save="y",
    timestep=1.0e11,
    location="lower left",
):
    """Return plot of depth vs time, with colour varying with cooling rate."""
    myr = 3.1556926e13
    fig, ax = plt.subplots(figsize=(12, 6))

    im = ax.imshow(
        np.concatenate(
            (dT_by_dt[-1:0:-1, :], dT_by_dt_core[-1:0:-1, :]), axis=0
        ),
        aspect="auto",
        vmin=-1e-12,
        cmap=custom_cmapy,
    )  # 'tab20b_r' #custom_cmapy
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(14)
    formatter = FuncFormatter(million_years)
    ax.xaxis.set_major_formatter(formatter)

    ticker_step = (100 * myr) / timestep
    loc = plticker.MultipleLocator(
        base=ticker_step
    )  # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)

    ax.set_xlabel("Time (Myr)")
    ax.set_ylabel("Depth (km)")
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)

    # Plot Imilac Cooling Rate Contour
    lines = [-(Imilac_cooling_rate)]
    cont_Im = plt.contour(
        np.concatenate(
            (dT_by_dt[-1:0:-1, :], dT_by_dt_core[-1:0:-1, :]), axis=0
        ),
        lines,
        colors="#143642",
        linestyles="-",
    )
    print(str(cont_Im))
    # plt.clabel(cont_Im, fontsize=10, inline=1, lw=3)

    # Plot Esquel Cooling Rate Contour
    lines = [-(Esquel_cooling_rate)]
    cont_Esq = plt.contour(
        np.concatenate(
            (dT_by_dt[-1:0:-1, :], dT_by_dt_core[-1:0:-1, :]), axis=0
        ),
        lines,
        colors="#143642",
        linestyles="--",
    )
    print(str(cont_Esq))
    # plt.clabel(cont_Esq, fontsize=10, inline=1, lw=3)

    # Plot 593K contour
    lines = [593]
    cont593 = plt.contour(
        np.concatenate(
            (temperatures[-1:0:-1, :], coretemp[-1:0:-1, :]), axis=0
        ),
        lines,
        colors="w",
        linestyles=":",
    )
    # plt.clabel(cont593, fontsize=10, inline=1)
    cont593.levels = [nf(val) for val in cont593.levels]
    fmt = "%r"
    plt.clabel(cont593, cont593.levels, fmt=fmt, fontsize=12, inline=1)

    # Plot 800K contour
    lines = [800]
    cont800 = plt.contour(
        np.concatenate(
            (temperatures[-1:0:-1, :], coretemp[-1:0:-1, :]), axis=0
        ),
        lines,
        colors="w",
        linestyles=":",
    )
    cont800.levels = [nf(val) for val in cont800.levels]
    fmt = "%r"
    plt.clabel(cont800, cont800.levels, fmt=fmt, fontsize=12, inline=1)

    # plot lines and text labels
    # plot Depth lines if in mantle
    if (
        Esquel_Depth == 0
        or Esquel_Depth == (r_core / 1000)
        or Esquel_Depth is None
    ):
        pass
    else:
        ax.plot(
            [0, max_time / (timestep)],
            [Esquel_Depth - 0.5, Esquel_Depth - 0.5],
            lw=2,
            c="#0F8B8D",
            linestyle="--",
        )
        # plt.text((max_time/(10**11)/1.1),Esquel_Depth-1,'Esquel',
        # color= '#0F8B8D')

    if (
        Imilac_Depth == 0
        or Imilac_Depth == (r_core / 1000)
        or Imilac_Depth is None
    ):
        pass
    else:
        ax.plot(
            [0, max_time / (timestep)],
            [Imilac_Depth - 0.5, Imilac_Depth - 0.5],
            lw=2,
            c="#0F8B8D",
            linestyle="-",
        )
        # plt.text((max_time/(10**11)/1.1),Imilac_Depth-1,'Imilac',
        # color='#143642')
    esq_cr_cont = mlines.Line2D(
        [],
        [],
        color="#143642",
        linestyle="--",
        lw=2,
        label="Esquel cooling rate",
    )
    imi_cr_cont = mlines.Line2D(
        [],
        [],
        color="#143642",
        linestyle="-",
        lw=2,
        label="Imilac cooling rate",
    )
    esq_line = mlines.Line2D(
        [],
        [],
        color="#0F8B8D",
        linestyle="--",
        lw=2,
        label="Esquel formation depth",
    )
    imi_line = mlines.Line2D(
        [],
        [],
        color="#0F8B8D",
        linestyle="-",
        lw=2,
        label="Imilac formation depth",
    )
    wid_line = mlines.Line2D(
        [],
        [],
        color="w",
        linestyle=":",
        lw=2,
        label="Widmanstätten temperatures",
    )

    plt.legend(
        handles=[imi_line, imi_cr_cont, esq_line, esq_cr_cont, wid_line],
        loc=location,
        fancybox=True,
        framealpha=0.3,
        fontsize=14,
    )  # shadow=True)
    # plot core lines if frozen before max time
    if time_core_frozen == 0 or fully_frozen == 0:
        ax.plot(
            [0, max_time / (timestep)],
            [
                (r_planet / 1000) - (r_core / 1000),
                (r_planet / 1000) - (r_core / 1000),
            ],
            lw=3,
            c="w",
            linestyle="-",
            alpha=0.4,
        )
        plt.text(25, 110, "CMB", color="w", alpha=0.5, fontsize=16)
        pass

    else:
        # core begins to freeze line
        ax.plot(
            [time_core_frozen / (timestep), time_core_frozen / (timestep)],
            [((r_planet) / 1000) - 3, (r_core / 1000)],
            lw=3,
            c="w",
            linestyle="--",
            alpha=0.5,
        )
        # core finishes freezing
        ax.plot(
            [fully_frozen / (timestep), fully_frozen / (timestep)],
            [((r_planet) / 1000) - 3, (r_core / 1000)],
            lw=3,
            c="w",
            linestyle="--",
            alpha=0.5,
        )
        # Core location
        ax.plot(
            [0, max_time / (timestep)],
            [
                (r_planet / 1000) - (r_core / 1000),
                (r_planet / 1000) - (r_core / 1000),
            ],
            lw=3,
            c="w",
            linestyle="-",
            alpha=0.4,
        )
        plt.text(25, 110, "CMB", color="w", alpha=0.5, fontsize=16)
        # Add text labelling period of core solidification
        middle_of_core_solidification = (
            ((fully_frozen + time_core_frozen) / 2)
        ) / (timestep) - 4700
        plt.text(
            middle_of_core_solidification,
            ((r_planet / 1000) - 15),
            "Core \nFreezes",
            color="w",
            fontsize=14,
            alpha=0.5,
        )

    plt.title("Planetesimal cooling rates through time", fontsize=18, pad=12)
    fmt1 = plticker.FuncFormatter(my_func)
    cb = fig.colorbar(im, format=fmt1, extend="min")
    cb.set_label("Cooling Rate (K/Myr)", fontsize=14)
    cb.ax.tick_params(labelsize=14)
    cb.ax.invert_yaxis()
    if save == "y":
        plt.savefig(
            str(folder) + "/cooling_rate_" + str(run_ID) + ".pdf",
            format="pdf",
            bbox_inches="tight",
        )
    else:
        pass
    plt.show()
