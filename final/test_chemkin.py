"""
Created on Tue Oct 17 2017
Harvard GSAS
CS207 Group 9
Module chemkin.py 
"""

import os
from chemkin import *


def test_class1():
    r = Xml2dict()
    print(os.listdir('.'))
    r.parse('./final/rxns.xml')
    assert(r.get_info()[1][1]['TYPE'] == 'Elementary')
    
def test_class2():
    r = Xml2dict()
    r.parse('./final/rxns.xml')
    assert(r.get_info()[0][1] == 'O')    
    
def test_class3():
    r = Xml2dict()
    r.parse('./final/rxns.xml')
    assert(r.get_info()[1][1]['products'] == {'H': 1, 'OH': 1})
    
def test_class5():
    r = Xml2dict()
    r.parse('./final/rxns2.xml')
    assert(r.get_info()[1][1]['reactants'] == {'HO2': 1, 'OH': 1}) 
    
def test_class6():
    r = Xml2dict()
    r.parse('./final/rxns2.xml')
    assert(r.get_info()[1][2]['ID'] == 'reaction03') 
    
def test_class7():
    r = Xml2dict()
    r.parse('./final/rxns2.xml')
    assert(r.get_info()[1][2]['reversible'] == 'no') 