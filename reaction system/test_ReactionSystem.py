# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:50:51 2017
@author: Camilo
"""

import sys
sys.path.insert(0, '../final')
from Reaction import Reaction
from ReactionSystem import ReactionSystem
import numpy as np

### Tests for ReactionSystems (rs):
   
def test_rs_nu_matrix_creation():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(reactants={'A':1,'C':2}, products = {'D':4}))
    
    rs = ReactionSystem(reactions)
    nu_1 = rs.get_nu_1()
    nu_2 = rs.get_nu_2()
    
    assert( nu_1.tolist() == [[1,1],[2,0],[0,2],[0,0]] )
    assert( nu_2.tolist() == [[0,0],[0,0],[1,0],[0,4]] )
    

def test_rs_progress_rate():
    
    reactions = []
    reactions.append(Reaction( coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':2}))
    reactions.append(Reaction(reactants={'A':2,'C':2}, coeffLaw = 'Constant', coeffParams = {'k':10},  products = {'B':1, 'C':1}))
    
    concs = {'A':1, 'B':2, 'C':1}
    rs = ReactionSystem(reactions, initial_concs=concs)
    prog_rate = rs.get_progress_rate()
    
    print(prog_rate.tolist())
        
    assert(prog_rate.tolist() == [40.,10.])
    
def test_rs_reaction_rate():
    
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2, 'C':1}
    rs = ReactionSystem(reactions, initial_concs=concs)
    reac_rate = rs.get_reac_rate()
            
    assert(reac_rate.tolist()==[-30., -60.,  20.])
    
def test_rs_not_enough_concentrations():
    
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1} ))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2}
    
    try:
        rs = ReactionSystem(reactions, initial_concs=concs)
    except Exception as err:
        assert(type(err)==ValueError)
            
def test_rs_too_many_concentrations():
    
    reactions = []
    reactions.append(Reaction( coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction( coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2, 'C':1, 'D':1}
    try:
        rs = ReactionSystem(reactions, initial_concs=concs)
    except Exception as err:
        assert(type(err)==ValueError)     
    
def test_rs_not_enough_params():
    
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2, 'C':1}
    
    try:
        rs = ReactionSystem(reactions, initial_concs=concs)
    except Exception as err:
        assert(type(err)==ValueError)     
    
