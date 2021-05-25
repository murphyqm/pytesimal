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

The `Pytesimal` package focuses on the conductive cooling of differentiated planetesimals, with the ability to alter the model set-up to also investigate primitive bodies that have not segregated a core. It provides an extensible toolkit for modelling the temperature and cooling rate distribution inside meteorite parent bodies in 1D, with the option of including temperature-dependent material properties. The code returns time-series Numpy arrays of temperatures and cooling rates across all radii for the core and mantle, which can be saved in binary compressed `.npz` format along with a `.json` file containing metadata and parameter values to allow processing at a later time. Full documentation of the modules and functions in the package are included in the API reference (`https://pytesimal.readthedocs.io/en/latest/apiref.html`).

![Cartoon sketch of model set-up, with different boundary conditions indicated by dotted and dashed lines; applications of different boundary conditions can be seen in the examples gallery in the documentation. \label{fig:model}](model_setups_edited_colours.pdf){ width=100% }

**Functionality includes:**

* Forward-Time Central-Space (FTCS) numerical solver for the 1D conduction equation for the mantle of a planetesimal
* Extensible boundary condition functions; current implementation includes a fixed temperature condition which can be applied to either the top or bottom boundary of the discretised region/mantle, and a fixed flux boundary condition that can be applied at the bottom boundary when the core is removed
* Vonn Neumann stability testing to ensure the combination of timestep, diffusivity and radial step will not result in numerical instabilities
* Simple isothermal eutectic core model
* Parameter file generator that populates an easy to read `.json` file with default parameters which can then be edited to suit the specific model set up
* Heatmap plotting functions to visualise data
* Functions to calculate the depth of formation and timing of paleomagnetic recording in pallasite meteorites [based on equations and theory from @Bryson2015; @Yang2010; used in @MurphyQuinlan2021]

# Statement of Need

`Pytesimal` was designed to be used by meteoriticists and other small body researchers, to quickly develop models of planetesimals and investigate the thermal history of meteorite parent bodies without having to rebuild the same basic architecture each time. While meteorite parent body modelling is an active field in small-body planetary science, there is a lack of open source, well-documented software specifically aimed at modelling the interiors of  planetesimal-scale bodies, especially if temperature-dependent material properties are desired. It can be difficult and time-consuming to recreate results from the literature without the availability of source code, making it challenging to build upon previous results and discoveries. Codes designed for Earth and other large planetary bodies, such as `ASPECT` [@KHB12] are often too complex for the simple, poorly constrained problems faced in meteoritics. `Pytesimal` is designed to be modular to allow future contributions and developments to be included. The package has been used in the scientific literature [@MurphyQuinlan2021] to demonstrate the importance of including temperature-dependent conductivity, heat capacity and density in models of the pallasite parent body. Examples recreating the results of @MurphyQuinlan2021 and @Bryson2015 are available in the documentation. The package is available for download from the Python Package Index (https://pypi.org/project/pytesimal/) and the source code is archived to Zenodo [@pytesimal].

![Temperatures and cooling rates in two 250 km radius planetesimals, using temperature dependent material properties. Data produced and plotted with the `Pytesimal` package. (a) and (b) show a body with a 125 km core, while (c) and (d) show an entirely silicate body with no core. Annotations and lines to show the mantle, core and core crystallisation period are added later, outside of the included plotting functions. \label{fig:heatmap}](both_results.pdf){ width=100% }

# Benefits of this package

1. `Pytesimal` only requires the commonly available Python packages `numpy` and `matplotlib`, with `Jupyter` useful for running the provided examples, but not essential.
2. Simple models can be set up and run in a single function call with an input parameter file, while more bespoke configurations only require a few extra lines of code.
3. `Pytesimal` is designed to be modular and extensible so that it can apply to a wide range of modelling requirements, to speed up development of meteorite parent body models.
4. Quick and simple visualisation of the results can be achieved with a single function call, and can be modified easily to produce publication-quality figures.

# Acknowledgements

MMQ was supported by the Leeds-York Natural Environment Research Council Doctoral Training Partnership (NE/L002574/1). The authors would like to thank Christopher J Davies for his comments on the paper. Thanks also to friends and colleagues who installed and tested the package, including Sam Greenwood, Lukas Hallen, Kate Quinlan, and Andrew Watson.

# References