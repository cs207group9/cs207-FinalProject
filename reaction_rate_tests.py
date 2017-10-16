# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:50:51 2017

@author: Camilo
"""

import Reaction
import ReactionSystem
import numpy as np

### Tests for ReactionSystems (rs):
   
def test_rs_nu_matrix_creation():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(reactants={'A':1,'C':2}, products = {'D':4}))
    
    rs = ReactionSystem(reactions)
    nu_1 = rs.calculate_nu_1()
    nu_2 = rs.calculate_nu_2()
    
    assert( nu_1 == [[1,1],[2,0],[0,2],[0,0]] )
    assert( nu_2 == [[0,0],[0,0],[2,0],[0,4]] )
    

def test_rs_progress_rate():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':2}, coeffLaw = 'const', coeffParams = 10))
    reactions.append(Reaction(reactants={'A':2,'C':2}, products = {'B':1, 'C':1}, coeffLaw = 'const', coeffParams = 10))
    
    concentrations = [1,2,1]
    rs = ReactionSystem(reactions, concentrations)
    prog_rate = rs.get_progress_rate()
            
    assert(prog_rate==[40,10])
    
def test_rs_reaction_rate():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':1}, coeffLaw = 'const', coeffParams = 10))
    reactions.append(Reaction(reactants={'C':2}, products = {'A':1, 'B':2}, coeffLaw = 'const', coeffParams = 10))
    
    concentrations = [1,2,1]
    rs = ReactionSystem(reactions, concentrations)
    prog_rate = rs.get_reac_rate()
            
    assert(prog_rate==[-30, -60,  20])
    
def test_rs_not_enough_concentrations():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':1}, coeffLaw = 'const', coeffParams = 10))
    reactions.append(Reaction(reactants={'C':2}, products = {'A':1, 'B':2}, coeffLaw = 'const', coeffParams = 10))
    
    concentrations = [1,2]
    
    try:
        rs = ReactionSystem(reactions, concentrations)
    except Exception as err:
        assert(type(err)==ValueError)
            
def test_rs_too_many_concentrations():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':1}, coeffLaw = 'const', coeffParams = 10))
    reactions.append(Reaction(reactants={'C':2}, products = {'A':1, 'B':2}, coeffLaw = 'const', coeffParams = 10))
    
    concentrations = [1,2,3,4]
    
    try:
        rs = ReactionSystem(reactions, concentrations)
    except Exception as err:
        assert(type(err)==ValueError)     
    
def test_rs_not_enough_params():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':1}, coeffLaw = 'arr', coeffParams = [10,10]))
    reactions.append(Reaction(reactants={'C':2}, products = {'A':1, 'B':2}, coeffLaw = 'const', coeffParams = 10))
    
    concentrations = [1,2,3]
    
    try:
        rs = ReactionSystem(reactions, concentrations)
    except Exception as err:
        assert(type(err)==ValueError)     
    
    