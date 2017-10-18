"""
Created on Tue Oct 17 2017
Harvard GSAS
CS207 Group 9
Module chemkin.py 
"""

import os
from chemkin import *
import numpy as np


# ============ Tests on Results ============ #

def test_info():
    r = Reaction(reactants=dict(H=1,O2=1), products=dict(OH=1,H=1))
    assert(r.getReactants() == dict(H=1,O2=1))
    assert(r.getProducts() == dict(OH=1,H=1))
    r.set_params(**dict(coeffLaw='Arrhenius', sth_irrel=42))
    assert(r.get_params()['coeffParams']['A'] == 1.0)

def test_rateCoeff():
    r1 = Reaction(coeffLaw='Constant', coeffParams=dict(k=3.14))
    r2 = Reaction(coeffLaw='Arrhenius', coeffParams=dict(E=8.314))
    r3 = Reaction(coeffLaw='modArrhenius', coeffParams=dict(b=3,E=2*8.314))
    assert(r1.rateCoeff() == 3.14)
    assert(r2.rateCoeff(T=1.0) == 1/np.e)
    assert(r3.rateCoeff(T=2.0) == 8/np.e)

def test_CoeffLaws_get():
    assert(Reaction._CoeffLawDict.getcopy('Arrhenius') == Arrhenius)
    assert(Reaction._CoeffLawDict.getcopy_all() == Reaction._CoeffLawDict._dict_all)
    assert(Reaction._CoeffLawDict.getcopy_builtin() == Reaction._CoeffLawDict._dict_builtin)

def test_CoeffLaws_update_remove_reset():
    def _law1(**kwargs): return 0.0
    def _law2(**kwargs): return 0.0
    Reaction._CoeffLawDict.reset()
    Reaction._CoeffLawDict.update('_1',_law1)
    Reaction._CoeffLawDict.update_group(dict(_1=_law1,_2=_law2))
    assert('_1' in Reaction._CoeffLawDict._dict_all)
    assert('_2' in Reaction._CoeffLawDict._dict_all)
    assert('_1' not in Reaction._CoeffLawDict._dict_builtin)
    Reaction._CoeffLawDict.remove('_1')
    assert('_1' not in Reaction._CoeffLawDict._dict_all)
    assert('_2' in Reaction._CoeffLawDict._dict_all)
    Reaction._CoeffLawDict.reset()
    assert(Reaction._CoeffLawDict._dict_all == Reaction._CoeffLawDict._dict_builtin)


# ============ Tests on Errors ============ #

def test_init_notimplemented():
    try:
        Reaction(reactants=dict(H=0.5,O2=1), products=dict(OH=1,H=1))
    except ValueError as err:
        assert(type(err) == ValueError)
    try:
        Reaction(reactants=dict(H=1,O2=1), products=dict(OH=-1,H=1))
    except ValueError as err:
        assert(type(err) == ValueError)

def test_init_bad_stoich():
    try:
        Reaction(reversible=True)
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)
    try:
        Reaction(**{'TYPE':'duplicate'})
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)
    try:
        Reaction(coeffLaw='_')
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)
        
def test_CoeffLaws_changebuiltin():
    def _law1(**kwargs): return 0.0
    def _law2(**kwargs): return 0.0
    Reaction._CoeffLawDict.reset()
    try:
        Reaction._CoeffLawDict.update('Arrhenius',_law1)
    except KeyError as err:
        assert(type(err) == KeyError)
    try:
        Reaction._CoeffLawDict.update_group(dict(_1=_law1,Arrhenius=_law2))
    except KeyError as err:
        assert(type(err) == KeyError)
    try:
        Reaction._CoeffLawDict.remove('Arrhenius')
    except KeyError as err:
        assert(type(err) == KeyError)
    Reaction._CoeffLawDict.reset()
        
def test_CoeffLaws_input():
    try:
        Reaction(coeffLaw='Constant', coeffParams=dict(k=-1.0)).rateCoeff()
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='Arrhenius').rateCoeff(T=-1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='Arrhenius', coeffParams=dict(A=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='Arrhenius', coeffParams=dict(R=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='modArrhenius').rateCoeff(T=-1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='modArrhenius', coeffParams=dict(A=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='modArrhenius', coeffParams=dict(R=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)


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
    rs = ReactionSystem(reactions, species_ls=['A','B','C'], initial_concs=concs)
    prog_rate = rs.get_progress_rate()
    
    print(prog_rate.tolist())
        
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



def test_class1():
    r = xml2dict()
    print(os.listdir('.'))
    r.parse('./final/rxns.xml')
    assert(r.get_info()[1][1]['TYPE'] == 'Elementary')
    
def test_class2():
    r = xml2dict()
    r.parse('./final/rxns.xml')
    assert(r.get_info()[0][1] == 'O')    
    
def test_class3():
    r = xml2dict()
    r.parse('./final/rxns.xml')
    assert(r.get_info()[1][1]['products'] == {'H': 1, 'OH': 1})
    
def test_class5():
    r = xml2dict()
    r.parse('./final/rxns2.xml')
    assert(r.get_info()[1][1]['reactants'] == {'HO2': 1, 'OH': 1}) 
    
def test_class6():
    r = xml2dict()
    r.parse('./final/rxns2.xml')
    assert(r.get_info()[1][2]['ID'] == 'reaction03') 
    
def test_class7():
    r = xml2dict()
    r.parse('./final/rxns2.xml')
    assert(r.get_info()[1][2]['reversible'] == 'no') 