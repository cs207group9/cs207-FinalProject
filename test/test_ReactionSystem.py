# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:50:51 2017
@author: Camilo, Yiqi
"""

import sys
from chemkin_CS207_G9.database_query import CoeffQuery
from chemkin_CS207_G9.CoeffLaw import BackwardLaw
from chemkin_CS207_G9.Reaction import Reaction
from chemkin_CS207_G9.ReactionSystem import ReactionSystem
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':2}))
    reactions.append(Reaction(reactants={'A':2,'C':2}, coeffLaw = 'Constant', coeffParams = {'k':10},  products = {'B':1, 'C':1}))
    
    concs = {'A':1, 'B':2, 'C':1}
    rs = ReactionSystem(reactions, species_ls=['A','B','C'], initial_concs=concs)
    prog_rate = rs.get_progress_rate()
    
    # print(prog_rate.tolist())
        
    assert(prog_rate.tolist() == [40.,10.])
    
def test_rs_reaction_rate():
    
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2, 'C':1}
    rs = ReactionSystem(reactions, species_ls=['A','B','C'], initial_concs=concs)
    reac_rate = rs.get_reac_rate()
            
    assert(reac_rate.tolist()==[-30., -60.,  20.])
    
def test_rs_not_enough_concentrations():
    
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1} ))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2}
    
    try:
        ReactionSystem(reactions, initial_concs=concs)
    except Exception as err:
        assert(type(err)==ValueError)
            
def test_rs_too_many_concentrations():
    
    reactions = []
    reactions.append(Reaction( coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction( coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2, 'C':1, 'D':1}
    try:
        ReactionSystem(reactions, initial_concs=concs)
    except Exception as err:
        assert(type(err)==ValueError)     
    
def test_rs_not_enough_params():
    
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    concs = {'A':1, 'B':2, 'C':1}
    
    try:
        ReactionSystem(reactions, initial_concs=concs)
    except Exception as err:
        assert(type(err)==ValueError)     
    
def test_rs_wrong_input_reacs():
    
    reactions = ['hey']
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    try:
        ReactionSystem(reactions)
    except Exception as err:
        assert(type(err)==TypeError) 

def test_rs_wrong_input_species():
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    try:
        ReactionSystem(reactions, species_ls = [1,'H2'])
    except Exception as err:
        assert(type(err)==TypeError) 
        
def test_rs_empty_array():
    try:
        ReactionSystem([])
    except Exception as err:
        assert(type(err)==ValueError) 
        
def test_set_and_get_temp():
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
   
    rs = ReactionSystem(reactions)
    rs.set_temp(100)
    assert(rs.get_temp()==100)
    
def test_set_and_get_concs():
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
   
    concs = {'A':1, 'B':2, 'C':1}
    rs = ReactionSystem(reactions)
    rs.set_concs(concs)
    assert(rs.get_concs()=={'A':1, 'B':2, 'C':1})
    try:
        rs.set_concs({'A':1, 'C':2})
    except Exception as err:
        assert(type(err)==ValueError)
    
def test_len_and_repr():
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    
    rs = ReactionSystem(reactions)
    assert(len(rs)==1)
        
    #assert(str(rs) == "ReactionSystem object with following Reactions:\nReaction 0: {'reversible': False, 'TYPE': 'Elementary', 'ID': 'reaction', 'coeffLaw': 'Constant', 'coeffParams': {'k': 10}, 'coeffUnits': {}, 'reactants': {'A': 1, 'B': 2}, 'products': {'C': 1}}")
    
def test_add_reaction_and_update_species():
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'D':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'D':1, 'B':2}))
    rs = ReactionSystem(reactions)
    
    rs.add_reaction(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'D':1}))
    
    assert(rs.get_species(update = False) == ['A', 'B', 'C', 'D'])
    
def test_reac_rate_with_no_concs_error():
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    rs = ReactionSystem(reactions)
    try:
        rs.get_reac_rate()
    except Exception as err:
        assert(type(err) == ValueError)
        
def test_species_order_maintained_when_specified():
    reactions = []
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(coeffLaw = 'Constant', coeffParams = {'k':10}, reactants={'C':2}, products = {'A':1, 'B':2}))
    
    rs = ReactionSystem(reactions, species_ls=['A','C','D','B'])
    assert(rs.get_species() == ['A', 'C', 'D', 'B'])


# ========================== REVERSIBLE APPROACHES =============================== #

nasa_query = CoeffQuery(os.path.join(BASE_DIR, 'nasa_thermo.sqlite'))

tol = 1e-10

# def test_set_temp_with_nasa():
#     reactions = []
#     reactions.append(Reaction(reactants={'H2':2,'O2':1}, products={'OH':2,'H2':1}))
#     reactions.append(Reaction(reactants={'OH':1,'HO2':1}, products={'H2O':1,'O2':1}))
#     species = ['H2','O2','OH','HO2','H2O']

#     rs = ReactionSystem(reactions, species, nasa_query, initial_T=300)

#     a_res = rs.get_a()

#     a_truth = np.zeros((5,7))
#     a_truth[0,:] = np.array([
#         3.3372792, -4.94024731e-05, 4.99456778e-07,
#         -1.79566394e-10, 2.00255376e-14, -950.158922, -3.20502331])
#     a_truth[1,:] = np.array([
#         3.28253784, 0.00148308754, -7.57966669e-07, 
#         2.09470555e-10, -2.16717794e-14, -1088.45772, 5.45323129])
#     a_truth[2,:] = np.array([
#         3.09288767, 0.000548429716, 1.26505228e-07, 
#         -8.79461556e-11, 1.17412376e-14, 3858.657, 4.4766961])
#     a_truth[3,:] = np.array([
#         4.0172109, 0.00223982013, -6.3365815e-07, 
#         1.1424637e-10, -1.07908535e-14, 111.856713, 3.78510215])
#     a_truth[4,:] = np.array([
#         3.03399249, 0.00217691804, -1.64072518e-07, 
#         -9.7041987e-11, 1.68200992e-14, -30004.2971, 4.9667701])

#     assert( np.prod(np.abs(a_truth-a_res)<tol) )


def test_validate_equilibrium():
    '''This test validates that 'reaction rate == 0' at equilibrium'''

    species = ['H2','O2','OH']
    reactions = [ Reaction(reversible='yes', 
                           reactants={'H2':2,'O2':1}, 
                           products={'OH':2,'H2':1}) ]
    nu = np.array([-1,-1,2]).reshape(-1,1)
    T = 2200

    rs = ReactionSystem(reactions, species, nasa_query, initial_T=T)
    ke_truth = BackwardLaw().equilibrium_coeffs(nu, rs.get_a(), T)

    # make sure that ke is at the order of 1
    assert( np.log10(ke_truth) > -0.5 and np.log10(ke_truth) < 0.5 )

    # calculate concentrations at equilibrium
    concs_prob = dict(H2=2, O2=2, OH=2*np.sqrt(ke_truth))
    rs.set_concs(concs_prob)

    # calsulate reaction rate at equilibrium (relative to kf,kb)
    # they should be essentially zero
    kf_res, kb_res = rs.get_reac_rate_coefs()
    reac_rate_res = rs.get_reac_rate()
    ratiof = reac_rate_res / kf_res
    ratiob = reac_rate_res / kb_res

    assert( np.prod(ratiof<tol) and np.prod(ratiob<tol) )


