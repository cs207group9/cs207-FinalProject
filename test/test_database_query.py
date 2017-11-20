# -*- coding: utf-8 -*-
"""
Database query tests

Created on Wed Nov 15 12:16:57 2017

@author: Camilo, Yiqi
"""

from chemkin_CS207_G9.database_query import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# def test_get_coeffs():
    
#     assert(get_coeffs('O2', 'high') == [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.45323129])
#     assert(get_coeffs('O2', 'low') == [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.45323129])

# def test_get_coeffs_wrong_range():
#     try:
#         get_coeffs('O','hello')
#     except Exception as err:
#         assert(type(err)==ValueError)

# def test_get_coeffs_wrong_specie():
#     try:
#         get_coeffs('Fe','low')
#     except Exception as err:
#         assert(type(err)==ValueError)
    
# def test_get_species():

def test_response():

    nasa_query = CoeffQuery(os.path.join(BASE_DIR, 'test_database.sqlite'))
    coeffs_low = nasa_query.response('O', 500)
    coeffs_high = nasa_query.response('O', 5000)
    truth_low = np.array([  
        2.94642878e+00, -1.63816649e-03, 2.42103170e-06,
        -1.60284319e-09, 3.89069636e-13, 2.91476445e+04, 2.96399498e+00])
    truth_high = np.array([  
        2.54205966e+00, -2.75506191e-05, -3.10280335e-09,
        4.55106742e-12, -4.36805150e-16, 2.92308027e+04, 4.92030811e+00])
    assert( np.prod(coeffs_low - truth_low) == 0 )
    assert( np.prod(coeffs_high - truth_high) == 0 )
    nasa_query.terminate()

def test_response_no_such_species():
    nasa_query = CoeffQuery(os.path.join(BASE_DIR, 'test_database.sqlite'))
    try:
        coeffs = nasa_query.response('ARBITRARY', 100)
    except ValueError as err:
        assert( type(err) == ValueError )
    nasa_query.terminate()
    
def test_response_out_of_range():
    nasa_query = CoeffQuery(os.path.join(BASE_DIR, 'test_database.sqlite'))
    try:
        coeffs = nasa_query.response('O', 100)
    except ValueError as err:
        assert( type(err) == ValueError )
    nasa_query.terminate()