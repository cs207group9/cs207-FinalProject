# -*- coding: utf-8 -*-
"""
Database query tests

Created on Wed Nov 15 12:16:57 2017

@author: Camilo
"""

import database_query

def test_get_coeffs():
    
    assert(get_coeffs('O2', 'high') == [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.45323129])
    assert(get_coeffs('O2', 'low') == [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.45323129])

def test_get_coeffs_wrong_range():
    try:
        get_coeffs('O','hello')
    except Exception as err:
        assert(type(err)==ValueError)

def test_get_coeffs_wrong_specie():
    try:
        get_coeffs('Fe','low')
    except Exception as err:
        assert(type(err)==ValueError)
    
def test_get_species():
    