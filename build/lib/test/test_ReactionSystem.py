# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:50:51 2017
@author: Camilo, Yiqi
"""

import sys
from chemkin_CS207_G9.parser.xml2dict import xml2dict
from chemkin_CS207_G9.parser.database_query import CoeffQuery
from chemkin_CS207_G9.reaction.CoeffLaw import BackwardLaw
from chemkin_CS207_G9.reaction.Reaction import Reaction
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem
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



# ========================== EVOLUTION =============================== #

path_xml = os.path.join(BASE_DIR, 'rxns_reversible.xml') # path to the .xml file
path_sql = os.path.join(BASE_DIR, 'nasa_thermo.sqlite')  # path to the .sqlite file

reader = xml2dict()
reader.parse(path_xml)
species, r_info = reader.get_info()
nasa_query = CoeffQuery(path_sql)

reactions = [Reaction(**r) for r in r_info]
concentrations = dict(H=2, O=1, OH=0.5, H2=1, H2O=1, O2=1, HO2=0.5, H2O2=1)
temperature = 3000

tol = 1e-6

def test_evolute_to_equilibrium():
    rs = ReactionSystem(
        reactions, species, nasa_query, 
        initial_concs=concentrations, initial_T=temperature)
    reac_rate_initial = rs.get_reac_rate()
    res_evo = rs.evolute(1e-12)
    reac_rate_final = rs.get_reac_rate()
    ratio = np.sqrt( np.sum(reac_rate_final**2) / np.sum(reac_rate_initial**2) )
    assert( ratio < tol )
