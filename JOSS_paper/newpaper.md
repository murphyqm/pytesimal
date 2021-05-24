---
title: 'Pytesimal: A Python package for modelling small planetary bodies'
tags:
  - Python
  - astronomy
  - planetary science
  - planetesimal
  - conductive cooling
authors:
  - name: Maeve Murphy Quinlan^[corresponding author]
    orcid: 0000-0003-2958-1008
    affiliation: 1
  - name: Andrew M. Walker
    orcid: 0000-0003-3121-3255
    affiliation: "1, 2"
  - name: Peter Selves
    orcid: 0000-0002-2763-1684
    affiliation: 3
  - name: Liam S. E. Teggin
    orcid: 0000-0003-0814-8766
    affiliation: 1

affiliations:
 - name: School of Earth and Environment, University of Leeds, Leeds, UK
   index: 1
 - name: Dept. of Earth Sciences, University of Oxford, Oxford, UK
   index: 2
 - name: School of Physics and Astronomy, University of Leicester
   index: 3
date: 29 April 2021
bibliography: paper.bib
   
---

# Summary

Planetesimals are small bodies that existed in the protoplanetary disk, some of which coalesced to form the planets, while others were broken into fragments and are sampled by the meteorite record.
The thermal evolution of these early-Solar System bodies is key to understanding the geological context and significance of meteorite samples and the thermal processing that they record.
Numerical methods are frequently used to model the interiors of meteorite parent bodies and then compare the results with evidence in meteorite samples [@Bryson2015; @Elkins-Tanton2011; @Haack1990; @MurphyQuinlan2021; @Nichols2016; @Sahijpal2021]. While the field of research spans different parent body compositions and different processes, many models share an underlying conductive cooling framework.

The `Pytesimal` package focuses on the conductive cooling of differentiated planetesimals, with the ability to alter the model set-up to also investigate primitive bodies that have not segregated a core. It provides an extensible toolkit for modelling the temperature and cooling rate distribution inside meteorite parent bodies in 1D, with the option of including temperature-dependent material properties. The code returns time-series Numpy arrays of temperatures and cooling rates across all radii for the core and mantle, which can be saved in binary compressed `.npz` format along with a `.json` file containing metadata and parameter values to allow processing at a later time.

![Cartoon sketch of model set-up. EDITED COLOUR PALETTE \label{fig:model}](model_setups_edited_colours.pdf)

**Key functionality includes:**

* Forward-Time Central-Space (FTCS) numerical solver for the 1D conduction equation for the mantle of a planetesimal
* Extensible boundary condition functions; current implementation includes a fixed temperature condition which can be applied to either the top or bottom boundary of the discretised region/mantle, and a fixed flux boundary condition that can be applied at the bottom boundary when the core is removed
* Vonn Neumann stability testing to ensure the combination of timestep, diffusivity and radial step will not result in numerical instabilities
* Simple isothermal eutectic core model
* Parameter file generator that populates an easy to read `.json` file with default parameters which can then be edited to suit the specific mdoel set up
* Heatmap plotting functions to visualise data
* Functions to calculate the depth of formation and timing of paleomagnetic recording in pallasite meteorites [based on equations and theory from @Bryson2015 and @Yang2010, used in @MurphyQuinlan2021]


# Statement of Need

`Pytesimal` was designed to be used by meteoriticists and other small body researchers, to quickly develop models of planetesimals and investigate the thermal history of meteorite parent bodies without having to rebuild the same basic architecture each time. While meteorite parent body modelling is an active field in small-body planetary science, there is a lack of open source, well-documented software specifically aimed at modelling the interiors of  planetesimal-scale bodies, especially if temperature-dependent material properties are desired. It can be difficult and time-consuming to recreate results from the literature without the availability of source code, making it challenging to build upon previous results and discoveries. Codes designed for Earth and other large planetary bodies, such as `ASPECT` [@KHB12] are often too complex for the simple, poorly constrained problems faced in meteoritics. `Pytesimal` is designed to be modular to allow future contributions and developments to be included. The package has been used in the scientific literature [@MurphyQuinlan2021] to demonstrate the importance of including temperature-dependent conductivity, heat capacity and density in models of the pallasite parent body. Examples recreating the results of @MurphyQuinlan2021 and @Bryson2015 are available in the documentation. The package is available for download from the Python Package Index (https://pypi.org/project/pytesimal/) and the source code is archived to Zenodo with the linked DOI @pytesimal.


# old paper

# Statement of need

~~`Pytesimal` is a Python package for modelling the thermal evolution of planetesimals and other small planetary bodies.~~ *<- REPEATING MYSELF - but not sure whether to keep this line and instead get rid of last line of Summary section...* Meteorite parent body modelling is an active field in small-body planetary science. There are two broad categories of models: those focusing on the accretion and differentiation of planetesimals, and those investigating the later conductive cooling of parent bodies [@Bryson2015; @Elkins-Tanton2011; @Haack1990; @MurphyQuinlan2021; @Nichols2016; @Sahijpal2021]. `Pytesimal` models the later conductive-cooling stage.

`Pytesimal` will enable groups to develop models of planetesimals and investigate the thermal history of meteorite parent bodies without having to rebuild the same basic architecture each time. `Pytesimal` provides a framework for modelling the conductive cooling of planetesimals, and is designed to be modular to allow future contributions and developments to be included. `Pytesimal` also includes plotting functionality to visualise the results of model runs, and a number of specialised tools designed to investigate pallasite meteorites specifically.

# Method

The `Pytesimal` package focuses on the conductive cooling of differentiated planetesimals, with the ability to alter the model set-up to also investigate primitive bodies that have not segregated a core. The basic 1D set-up includes a conductively cooling discretised region which can include a low-diffusivity megaregolith layer, and an isothermal convecting core. The core can be removed to closer approximate primitive meteorite parent bodies, with a zero flux boundary condition applied across the centre to ensure symmetry (\autoref{fig:model}).

![Cartoon sketch of model set-up. CHANGED COLOUR PROFILE TO CMYK \label{fig:model}](model_setups_CMYK.pdf)



The 1D conductive cooling of the discretised region is controlled by the heat equation:

\begin{equation}
\frac{\partial T}{\partial t} \rho C=
\frac{1}{r^2} \frac{\partial}{\partial r}\left(k r^2 \frac{\partial T}{\partial r} \right) =
\overbrace{\frac{dk}{dT}\left(\frac{\partial T}{\partial r} \right) ^2} ^{\text{non-linear term}}+
\underbrace{\frac{2k}{r} \frac{\partial T}{\partial r}}_{\text{geometric term}} +
\overbrace{k \frac{\partial ^2 T}{\partial r^2}}^{\text{linear term}},
\label{eq:non_lin_heat}
\end{equation}

where $T$ is the temperature, $r$ is the radial value, $t$ is time, and $k$, $\rho$ and $C$ are the conductivity, density and heat capacity respectively. `Pytesimal` provides the capability to use temperature-dependent conductivity, heat capacity and density, with functions suitable for an olivine mantle included. These $T$-dependent material properties of olivine (\autoref{fig:matprops}) are based on experimental results and mineral physics theory from @Fei2013, @Robie1982, @Su2018, @Suzuki1975, @Xu2004, with more information in @MurphyQuinlan2021.

![Conductivity ($k$) and volumetric heat capacity ($\rho C$) in olivine.\label{fig:matprops}](material_properties.pdf){ width=80% }

The `numerical_methods` module uses the explicit Forward-Time Central-Space (FTCS) scheme which is conditionally stable and must satisfy Von Neumann stability criteria in 1D:
$\frac{\kappa \delta t}{\delta r ^{2}} \leq \frac{1}{2}$, where $\kappa$ is the thermal diffusivity of the material, $\delta t$ is the timestep of the numerical scheme, and $\delta r$ is the radial step [@Crank1947]. `Pytesimal.numerical_methods` includes functions to calculate the diffusivity from $k$, $\rho$ and $C$, and to check whether the chosen timestep will result in instabilities.

Boundary conditions for the top and bottom of the discretised region are passed into `numerical_methods.discretisation` as callable objects to allow for user-defined functions to be incorporated. Two different boundary conditions are currently provided, illustrated in \autoref{fig:matprops}: a fixed temperature condition which can be applied to either the top or bottom boundary of the discretised region, and a zero flux boundary condition that can be applied at the bottom boundary when the core is removed.

The core interacts with the mantle through heat extracted across the core-mantle boundary over one timestep in the form of power (P, in Watts). The heat extracted in one timestep ($P_{\mathrm{CMB}}$) is calculated:

\begin{equation}
P_{\mathrm{CMB}} = - {A}_{\mathrm{c}} k_{\mathrm{m}} \frac{\partial T}{\partial r}\bigg\vert _{r = r_\mathrm{c}}
\end{equation}

where $A_\mathrm{c}$ is the core surface area, $r_\mathrm{c}$ is the core radius, and $k_\mathrm{m}$ is the thermal conductivity at the base of the mantle or discretised region. From this, the core boundary temperature is then updated by $\Delta T$:

\begin{equation}
\Delta T = - \frac{P_{\mathrm{CMB}}}{\rho_{\mathrm{c}} C_{\mathrm{c}} V_{\mathrm{c}}} \delta t
\end{equation}

where $\rho_{\mathrm{c}}$ and $C_{\mathrm{c}}$ are the density and heat capacity of the core, and $V_{\mathrm{c}}$ is the volume of the core. Once the core reaches its freezing temperature, the temperature is held constant. Latent heat is extracted until the total latent heat associated with core crystallisation has been removed. This simple eutectic core model ignores inner core formation and treats the liquid and solid fraction as identical, but is implemented in a way that allows the `IsothermalEutecticCore` object to be replaced with a more complex core model where applicable.

`Pytesimal` also contains the functionality to quickly plot results, which allows for both on-the-go data visualisation and for saved results to be loaded and plotted at a later time (\autoref{fig:heatmap}). The `analysis` module can be used to calculate cooling rates, estimate the depth of pallasite meteorite genesis, and find the time when paleomagnetism could be recorded by these meteorite samples.

# Examples of applications

~~An earlier version of~~ `Pytesimal` has been used in a scientific publication to demonstrate that the inclusion of temperature dependent thermal properties in place of constant values can result in different interpretations of the meteorite record, with pallasite meteorites used as an example [@MurphyQuinlan2021]. \autoref{fig:heatmap} reproduces the results of @MurphyQuinlan2021. The default values provided by `load_plot_save.make_default_param_file` are from @MurphyQuinlan2021 and citations therein.

![Temperatures and cooling rates in a 250 km radius planetesimal, using temperature dependent material properties. Annotations and lines to show the mantle, core and core crystallisation period are added later, outside of the `pytesimal.load_plot_save` functions. \label{fig:heatmap}](heatmap.pdf){ width=80% }

# Benefits of this package

1. `Pytesimal` only requires the commonly available Python packages `numpy` and `matplotlib`, with `Jupyter` useful for running the provided examples, but not essential.
2. Simple models can be set up and run in a single function call with an input parameter file, while more bespoke set ups only require a few extra lines of code.
3. `Pytesimal` is designed to be modular and extensible so that it can apply to a wide range of modelling requirements, to speed up development of meteorite parent body models.
4. Quick and simple visualisation of the results can be achieved with a single function call, and can be modified easily to produce publication-quality figures.

# Acknowledgements

MMQ was supported by the Leeds-York Natural Environment Research Council Doctoral Training Partnership (NE/L002574/1). The authors would like to thank Christopher J Davies for his comments on the paper.

# References