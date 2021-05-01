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
  - name: Christopher J. Davies
    orcid: 0000-0002-1074-3815
    affiliation: 1
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

Planetesimals, the building blocks of planets in our Solar System, are sampled by the meteorite record. Thermal processing recorded in meteorites can be linked to the thermal evolution of their parent bodies, and so can inform us of the size and geometries of these parent bodies, and how deep within them the meteorite material resided before being broken apart and distributed across the asteroid belt. Modelling the temperatures and cooling rates within these bodies that existed 4.5 billion years ago is one of the key ways to understand the geological context of meteorites.
The `Pytesimal` package focuses on the conductive cooling stage of planetesimal evolution, and provides a toolkit for modelling the temperature and cooling rate distribution inside meteorite parent bodies in 1D, with and without temperature-dependent material properties.

# Statement of need

`Pytesimal` is a Python package for modelling the thermal evolution of planetesimals and other small planetary bodies. Meteorite parent body modelling is an active field in small-body planetary science. There are two broad categories of models: those focusing on the accretion and differentiation of planetesimals, and those investigating the later conductive cooling of parent bodies [@Bryson2015; @Elkins-Tanton2011; @Haack1990; @MurphyQuinlan2021; @Nichols2016; @Sahijpal2021]. The `Pytesimal` package fits into this second category, and has already been used in a scientific publication to demonstrate that the inclusion of temperature-dependent properties such as conductivity, heat capacity and density in place of constant values can result in different interpretations of the meteorite record, with pallasite meteorites used as an example [@MurphyQuinlan2021].

`Pytesimal` will enable groups to continue to develop models of planetesimals and investigate the thermal history of meteorite parent bodies without having to rebuild the same basic architecture each time. `Pytesimal` provides a framework for modelling the conductive cooling of planetesimals, and is designed to be modular to allow future contributions and developments to be included. `Pytesimal` also includes plotting functionality to visualise the results of model runs, and a number of specialised tools designed to investigate pallasite meteorites specifically.

# Method

The `Pytesimal` package focuses on the conductive cooling of differentiated planetesimals, with the ability to alter the model set-up to also investigate primitive bodies that have not segregated a core. The basic 1D set-up includes a conductively cooling discretised region which can include a low-diffusivity megaregolith layer, and an isothermal convecting core. The core can be removed to closer approximate primitive meteorite parent bodies, with a zero flux boundary condition applied across the centre to ensure symmetry (\autoref{fig:model}).

![TEMP PLACEHOLDER - TO BE PROPERLY DRAWN UP. Cartoon sketch of model set-up.\label{fig:model}](model_setups.pdf)

The 1D conductive cooling of the discretised region is controlled by the heat equation:

\begin{equation}
\frac{\partial T}{\partial t} \rho C=
\frac{1}{r^2} \frac{\partial}{\partial r}\left(k r^2 \frac{\partial T}{\partial r} \right) =
\overbrace{\frac{dk}{dT}\left(\frac{\partial T}{\partial r} \right) ^2} ^{\text{non-linear term}}+
\underbrace{\frac{2k}{r} \frac{\partial T}{\partial r}}_{\text{geometric term}} +
\overbrace{k \frac{\partial ^2 T}{\partial r^2}}^{\text{linear term}},
\label{eq:non_lin_heat}
\end{equation}

where $T$ is the temperature, $r$ is the radial value, $t$ is time, and $k$, $\rho$ and $C$ are the conductivity, density and heat capacity respectively. `Pytesimal` provides the capability to use temperature-dependent conductivity, heat capacity and density, with functions suitable for an olivine mantle included. These $T$-dependent material properties of olivine (\autoref{fig:matprops}) are based on experimental results and mineral physics theory from Fei2013, Robie1982, Su2018, Suzuki1975, Xu2004, with more information in @MurphyQuinlan2021.

![Conductivity ($k$) and volumetric heat capacity ($\rho C$) in olivine.\label{fig:matprops}](material_properties.pdf){ width=80% }
The `numerical_methods` module uses the explicit Forward-Time Central-Space (FTCS) scheme which is conditionally stable and must satisfy Von Neumann stability criteria in 1D:
$\frac{\kappa \delta t}{\delta r ^{2}} \leq \frac{1}{2}$, where $\kappa$ is the thermal diffusivity of the material, $\delta t$ is the timestep of the numerical scheme, and $\delta r$ is the radial step [@Crank1947]. `Pytesimal.numerical_methods` includes functions to calculate the diffusivity from $k$, $\rho$ and $C$, and to check whether the chosen timestep will result in instabilities.

Boundary conditions for the top and bottom of the discretised region are passed into `numerical_methods.discretisation` as callable objects to allow for user-defined functions to be easily incorporated. Two different boundary conditions are currently provided, illustrated in \autoref{fig:matprops}: a fixed temperature condition which can be applied to either the top or bottom boundary of the discretised region, and a zero flux boundary condition that can be applied at the bottom boundary when the core is removed.

The core interacts with the mantle through heat extracted across the core-mantle boundary over one timestep in the form of power (P, in Watts). The heat extracted in one timestep ($P_{\mathrm{CMB}}$) is calculated:

\begin{equation}
P_{\mathrm{CMB}} = - {A}_{\mathrm{c}} k_{\mathrm{m}} \frac{\partial T}{\partial r}\bigg\vert _{r = r_\mathrm{c}}
\end{equation}

where $A_\mathrm{c}$ is the core surface area, $r_\mathrm{c}$ is the core radius, and $k_\mathrm{m}$ is the thermal conductivity at the base of the mantle or discretised region. The core boundary temperature is then updated by $\Delta T$, the resulting change in temperature over one timestep:

\begin{equation}
\Delta T = - \frac{P_{\mathrm{CMB}}}{\rho_{\mathrm{c}} C_{\mathrm{c}} V_{\mathrm{c}}} \delta t
\end{equation}

where $\rho_{\mathrm{c}}$ and $C_{\mathrm{c}}$ are the density and heat capacity of the core, and $V_{\mathrm{c}}$ is the volume of the core. The core cools until it reaches its freezing temperature, at which point the temperature is held constant and latent heat is extracted until the total latent heat associated with core crystallisation has been removed. This core cooling method differs subtly from the method implemented in @MurphyQuinlan2021 which used an earlier version of the code that instead calculated energy extracted from the core in Joules. This simple eutectic core model ignores inner core formation and treats the liquid and solid fraction as identical, but is implemented in a way that would allow the `IsothermalEutecticCore` object to be easily replaced with a more complex core mode where applicable.

![Temperatures and cooling rates in a 250 km radius planetesimal, using temperature dependent material properties. Annotations and lines to show the mantle, core and core crystallisation period are added later, outside of the `pytesimal.load_plot_save` functions. \label{fig:heatmap}](heatmap.pdf){ width=80% }

`Pytesimal` also contains the functionality to quickly plot results, which allows for both on-the-go data visualisation and for saved results to be loaded and plotted at a later time.


# Benefits of this package

1. `Pytesimal` only requires the commonly available Python packages `numpy` and `matplotlib`, with `Jupyter` useful for running the provided examples, but not essential.
2. Simple models can be set up and run in a single function call with an input parameter file, while more bespoke set ups only require a few extra lines of code.
3. `Pytesimal` is designed to be modular and extensible so that it can applied to a wide range of modelling requirements, to speed up development of meteorite parent body models.
4. Quick and simple visualisation of the results can be achieved with a single function call, and can be modified easily to produce publication-quality figures.

# Acknowledgements

We acknowledge funding support to MMQ from the Leeds-York Natural Environment Research Council Doctoral Training Partnership (NE/L002574/1) and to CJD by the Natural Environment Research Council Independent Research Fellowship (NE/L011328/1).

# References