# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:54:38 2017

@author: Camilo
"""

import sqlite3

def get_coeffs(species_name, temp_range):
    
    db = sqlite3.connect('HW10-DB.sqlite')
    cursor = db.cursor()
    
    if temp_range == 'low':
        res_of_query = cursor.execute('SELECT COEFF_1, COEFF_2, COEFF_3, COEFF_4, COEFF_5, COEFF_6, COEFF_7 FROM LOW WHERE SPECIES_NAME = "'+species_name+'"')
        coeffs = list(res_of_query.fetchall()[0])
    elif temp_range == 'high':
        res_of_query = cursor.execute('SELECT COEFF_1, COEFF_2, COEFF_3 ,COEFF_4, COEFF_5 ,COEFF_6, COEFF_7 FROM HIGH WHERE SPECIES_NAME = "'+species_name+'"')
        coeffs = list(res_of_query.fetchall()[0])
    else:
        raise ValueError('Temp range provided is neither "low" nor high"')
    return coeffs
 

def get_species(temp, temp_range):
    ''' 
    Returns species with a temperature range above or below a given value (temp). If temp_range is low,
    This function returns the specie name of any element with a TLOW in the LOW range inferior to the given temp. If
    temp_range is high, the species with a THIGH in the HIGH range superior to the given temp are returned.
    '''
    
    db = sqlite3.connect('HW10-DB.sqlite')
    cursor = db.cursor()
    
    if temp_range == 'low':
        res_of_query = cursor.execute('SELECT SPECIES_NAME FROM LOW WHERE TLOW < '+str(temp))
        species = [s[0] for s in res_of_query.fetchall()]
    elif temp_range == 'high':
        res_of_query = cursor.execute('SELECT SPECIES_NAME FROM HIGH WHERE THIGH > '+str(temp))    
        species = [s[0] for s in res_of_query.fetchall()]
    else:
        raise ValueError('Temp range provided is neither "low" nor high"')
    
    return species