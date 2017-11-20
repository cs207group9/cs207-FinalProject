from chemkin_CS207_G9.Reaction import *
from chemkin_CS207_G9 import CoeffLaw
import numpy as np


# ============ Tests on Results ============ #

def test_info():
    r = Reaction(reactants=dict(H=1,O2=1), products=dict(OH=1,H=1))
    assert(r.getReactants() == dict(H=1,O2=1))
    assert(r.getProducts() == dict(OH=1,H=1))
    r.set_params(**dict(coeffLaw='Arrhenius', sth_irrel=42))
    assert(r.get_params()['coeffParams']['A'] == 1.0)
    assert(r.is_reversible()==False)

def test_rateCoeff():
    r1 = Reaction(coeffLaw='Constant', coeffParams=dict(k=3.14))
    r2 = Reaction(coeffLaw='Arrhenius', coeffParams=dict(E=8.314))
    r3 = Reaction(coeffLaw='modArrhenius', coeffParams=dict(b=3,E=2*8.314))
    assert(r1.rateCoeff() == 3.14)
    assert(r2.rateCoeff(T=1.0) == 1/np.e)
    assert(r3.rateCoeff(T=2.0) == 8/np.e)

def test_CoeffLaws_get():
    assert(Reaction._CoeffLawDict.getcopy('Arrhenius') == CoeffLaw.Arrhenius)
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
    # try:
    #     Reaction(reversible=True)
    # except NotImplementedError as err:
    #     assert(type(err) == NotImplementedError)
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