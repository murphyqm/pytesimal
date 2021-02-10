#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:14:58 2020

@author: maeve
"""

from context import draft_cond_cooling as mcc
# from context import modular_cond_cooling as mcc
# Error message from above line:
# from .context import modular_cond_cooling as mcc ## this didn't work - why?
# E   ImportError: attempted relative import with no known parent package

# from pytesimal import modular_cond_cooling as mcc

# Error message from above line:
# ImportError: cannot import name 'modular_cond_cooling' from 'pytesimal'
# (unknown location)

folder = "output_runs/auto_pytest"


def test_def_const():
    """
    Simple test to check default results of constant model.

    Runs constant model with default values and checks that these are expected.
    High level test that only checks final output - need more granular testing.

    Returns
    -------
    None.

    """
    (
        vbegins_to_freeze,
        vfinished_freezing,
        vEsquel_Depth,
        vEsq_timing,
        vImilac_Depth,
        vIm_timing,
    ) = (
        5411100000000000.0,
        7637200000000000.0,
        64.0,
        7576100000000000,
        57.0,
        5849600000000000,
    )
    run_ID = "simple_test_constant"
    (
        begins_to_freeze,
        finished_freezing,
        Esquel_Depth,
        Esq_timing,
        Imilac_Depth,
        Im_timing,
    ) = mcc.conductive_cooling(run_ID, folder, return_vars="y",
                               save_param_file="n")
    assert (
        vbegins_to_freeze,
        vfinished_freezing,
        vEsquel_Depth,
        vEsq_timing,
        vImilac_Depth,
        vIm_timing,
    ) == (
        begins_to_freeze,
        finished_freezing,
        Esquel_Depth,
        Esq_timing,
        Imilac_Depth,
        Im_timing,
    )


def test_def_var():
    """
    Simple test to check default results of variable model.

    Runs constant model with default values and checks that these are expected.
    High level test that only checks final output - need more granular testing.

    Returns
    -------
    None.

    """
    (
        vbegins_to_freeze,
        vfinished_freezing,
        vEsquel_Depth,
        vEsq_timing,
        vImilac_Depth,
        vIm_timing,
    ) = (
        6662500000000000.0,
        8978400000000000.0,
        68.0,
        7819700000000000,
        61.0,
        6501800000000000,
    )
    run_ID = "simple_test_variable"
    (
        begins_to_freeze,
        finished_freezing,
        Esquel_Depth,
        Esq_timing,
        Imilac_Depth,
        Im_timing,
    ) = mcc.conductive_cooling(
        run_ID,
        folder,
        cond_constant="n",
        density_constant="n",
        heat_cap_constant="n",
        return_vars="y",
        save_param_file="n",
    )
    assert (
        vbegins_to_freeze,
        vfinished_freezing,
        vEsquel_Depth,
        vEsq_timing,
        vImilac_Depth,
        vIm_timing,
    ) == (
        begins_to_freeze,
        finished_freezing,
        Esquel_Depth,
        Esq_timing,
        Imilac_Depth,
        Im_timing,
    )