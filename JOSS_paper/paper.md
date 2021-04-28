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
    affiliation: 3
  - name: Liam S. E. Teggin
    orcid: 0000-0003-0814-8766
    affiliation: 1

affiliations:
 - name: School of Earth and Environment, University of Leeds, Leeds, UK
   index: 1
 - name: Dept. of Earth Sciences, University of Oxford, Oxford, UK
   index: 2
 - name: University of Leicester
   index: 3
date: 21 April 2021
bibliography: paper.bib
   
---

# Summary

Planetesimals, the building blocks of planets in our Solar System, are sampled by the meteorite record. Thermal processing recorded in meteorites can be linked to the thermal evolution of their parent bodies, and so can inform us of the size and geometries of these parent bodies, and how deep within them the meteorite material resided before being broken apart and distributed across the asteroid belt. The `pytesimal` package focuses on the conductive cooling stage of planetesimal evolution, and provides a toolkit for modelling the temperature and cooling rate distribution inside meteorite parent bodies in 1D, with and without temperature-dependent material properties.

# Statement of need

`pytesimal` is a Python package for modelling the thermal evolution of planetesimals and other small planetary bodies. Meteorite parent body modelling is an activate field in small-body planetary science. There are two broad categories of models: those focusing on the accretion and differentiation of planetesimals, and those investigating the later conductive cooling of parent bodies [@Bryson2015; @Elkins-Tanton2011; @Haack1990; @MurphyQuinlan2021; @Nichols2016; @Sahijpal2021]. The `pytesimal` package fits into this second category, and has already been used in a scientific publication to demonstrate that the inclusion of temperature-dependent properties such as conductivity, heat capacity and density in place of constant values can result in different interpretations of the meteorite record, with pallasite meteorites used as an example [@MurphyQuinlan2021].

`pytesimal` will enable groups to continue to develop models of planetesimals and investigate the thermal history of meteorite parent bodies without having to rebuild the same basic architecture each time. `pytesimal` provides a framework for modelling the conductive cooling of planetesimals, and is designed to be modular to allow future contributions and developments to be included. `pytesimal` also includes plotting functionality to visualise the results of model runs, and a number of specialised tools designed to investigate pallasite meteorites specifically.

# Background

Meteorites provide insights into some of the earliest planetary bodies in the Solar System: planetesimals, the building blocks of the planets and the asteroid belt. Unlike geological samples collected from field locations, meteorite samples often lack geological context. Modelling the evolution of small bodies in the Solar System allows us to make estimates about the conditions under which the meteorite material formed and was processed, placing the samples in context and allowing us to better understand planet building processes in the early Solar System.

The `pytesimal` package focuses on the conductive cooling of differentiated planetesimals, with the ability to alter the model set-up to also investigate primitive bodies that have not segregated a core. The conductive cooling of the mantle in 1D is controlled by the heat equation:

\begin{equation}
\frac{\partial T}{\partial t} \rho C=
\frac{1}{r^2} \frac{\partial}{\partial r}\left(k r^2 \frac{\partial T}{\partial r} \right) =
\overbrace{\frac{dk}{dT}\left(\frac{\partial T}{\partial r} \right) ^2} ^{\text{non-linear term}}+
\underbrace{\frac{2k}{r} \frac{\partial T}{\partial r}}_{\text{geometric term}} +
\overbrace{k \frac{\partial ^2 T}{\partial r^2}}^{\text{linear term}},
\label{eq:non_lin_heat}
\end{equation}

where $T$ is the temperature in the mantle, $r$ is the radial value, $t$ is time, and $k$, $\rho$ and $C$ are the conductivity, density and heat capacity respectively.  @MurphyQuinlan2021 demonstrated that neglecting to include temperature-dependent material properties when modelling meteorite parent bodies can lead to different interpretations of cooling-rate data in meteorite samples. `pytesimal` provides the capability to use temperature-dependent conductivity, heat capacity and density, with functions suitable for an olivine mantle included. These $T$-dependent material properties are illustrated in \autoref{fig:matprops}.

![Caption for example figure.\label{fig:matprops}](material_properties.pdf)

Differentiated meteorites formed within bodies that melted and segregated to a certain extent, before slowly cooling. Some meteorite samples capture a cooling history attributed to this later conductive cooling stage of the parent body. One such group of meteorites, the pallasites, may have formed through a collision which caused molten metal to be injected into the olivine-rich mantle of a differentiated planetesimal [@Walte2020]. The cooling rate of this metal below 975 K following injection into the mantle is captured in Ni profiles in regions of Widmanstätten pattern [@Yang2010]. Paleomagnetic records in some samples indicate that a core dynamo was active when the regions of pallasite material cooled through the tetrataenite formation temperature [@Bryson2015; @Nichols2016].

# Mathematics

EXAMPLE PAPER FROM JOSS.ORG.
Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

EXAMPLE PAPER FROM JOSS.ORG.
Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

EXAMPLE PAPER FROM JOSS.ORG.
Figures can be included like this:

![Caption for example figure.\label{fig:example}](material_properties.pdf)

and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:

![Caption for example figure.](material_properties.pdf){ width=20% }

# Acknowledgements

EXAMPLE PAPER FROM JOSS.ORG.
We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References