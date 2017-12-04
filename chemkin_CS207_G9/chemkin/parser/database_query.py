# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:54:38 2017

@author: Camilo, Yiqi
"""

import sqlite3
import numpy as np

class CoeffQuery:

    def __init__(self, path_database):
        self.db = sqlite3.connect(path_database)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def terminate(self):
        self.db.close()

    def response(self, species_name, temp):
        query_low = '''SELECT 
                        TLOW, THIGH, 
                        COEFF_1, COEFF_2, COEFF_3, 
                        COEFF_4, COEFF_5, COEFF_6, COEFF_7 
                    FROM LOW WHERE 
                        SPECIES_NAME = "''' + species_name + '''"'''
        query_high = '''SELECT 
                        TLOW, THIGH, 
                        COEFF_1, COEFF_2, COEFF_3, 
                        COEFF_4, COEFF_5, COEFF_6, COEFF_7 
                    FROM HIGH WHERE 
                        SPECIES_NAME = "''' + species_name + '''"'''
        res_low = self.cursor.execute(query_low).fetchall()
        res_high = self.cursor.execute(query_high).fetchall()
        if len(res_low) == 0 or len(res_high) == 0:
            raise ValueError('Species = "{}". No match in the database.'.format(species_name))
        if temp >= res_low[0][0] and temp <= res_low[0][1]:
            coeffs = np.array(res_low[0][2:])
        elif temp >= res_high[0][0] and temp <= res_high[0][1]:
            coeffs = np.array(res_high[0][2:])
        else:
            raise ValueError('Species = "{}", T = {}. No match in the database.'.format(species_name, temp))

        return coeffs


# def get_coeffs(path_database, species_name, temp_range):
    
#     db = sqlite3.connect(path_database)
#     cursor = db.cursor()
    
#     if temp_range == 'low':
#         res_of_query = cursor.execute('SELECT COEFF_1, COEFF_2, COEFF_3, COEFF_4, COEFF_5, COEFF_6, COEFF_7 FROM LOW WHERE SPECIES_NAME = "'+species_name+'"')
#         coeffs = list(res_of_query.fetchall()[0])
#     elif temp_range == 'high':
#         res_of_query = cursor.execute('SELECT COEFF_1, COEFF_2, COEFF_3 ,COEFF_4, COEFF_5 ,COEFF_6, COEFF_7 FROM HIGH WHERE SPECIES_NAME = "'+species_name+'"')
#         coeffs = list(res_of_query.fetchall()[0])
#     else:
#         raise ValueError('Temp range provided is neither "low" nor high"')

#     db.close()

#     return coeffs
 

# def get_species(path_database, temp, temp_range):
#     ''' 
#     Returns species with a temperature range above or below a given value (temp). If temp_range is low,
#     This function returns the specie name of any element with a TLOW in the LOW range inferior to the given temp. If
#     temp_range is high, the species with a THIGH in the HIGH range superior to the given temp are returned.
#     '''
    
#     db = sqlite3.connect(path_database)
#     cursor = db.cursor()
    
#     if temp_range == 'low':
#         res_of_query = cursor.execute('SELECT SPECIES_NAME FROM LOW WHERE TLOW < '+str(temp))
#         species = [s[0] for s in res_of_query.fetchall()]
#     elif temp_range == 'high':
#         res_of_query = cursor.execute('SELECT SPECIES_NAME FROM HIGH WHERE THIGH > '+str(temp))    
#         species = [s[0] for s in res_of_query.fetchall()]
#     else:
#         raise ValueError('Temp range provided is neither "low" nor high"')

#     db.close()
    
#     return species



# def get_range(path_database, species_name, temp):

#     db = sqlite3.connect(path_database)
#     cursor = db.cursor()

#     query_low = 'SELECT TLOW, THIGH FROM LOW WHERE SPECIES_NAME = "'+species_name+'"'
#     query_high = 'SELECT TLOW, THIGH FROM HIGH WHERE SPECIES_NAME = "'+species_name+'"'

#     range_low = cursor.execute(query_low).fetchall()[0]
#     range_high = cursor.execute(query_high).fetchall()[0]

#     if temp >= range_low[0] and temp <= range_low[1]:
#         res_range = 'low'
#     elif temp >= range_high[0] and temp <= range_high[1]:
#         res_range = 'high'
#     else:
#         res_range = None

#     db.close()

#     if res_range is None:
#         raise ValueError('Species = "{}", T = {}. no match in the database.'.format(species_name, temp))
#     else:
#         return res_range