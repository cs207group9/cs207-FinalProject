from Reaction import Reaction
import numpy as np

def ListTest(func):
    # func() is a test function that returns list of test results
    def inner():
        for t in func():
            assert(t)
    return inner

# ============ Tests on Results ============ #

@ListTest
def test_info():
    r = Reaction(reactants=dict(H=1,O2=1), products=dict(OH=1,H=1))
    return [
        r.getReactants() == dict(H=1,O2=1),
        r.getProducts() == dict(OH=1,H=1)]

@ListTest
def test_rateCeff():
    r1 = Reaction(coeffLaw='const', coeffParams=dict(k=3.14))
    r2 = Reaction(coeffLaw='arr', coeffParams=dict(E=8.314))
    r3 = Reaction(coeffLaw='modarr', coeffParams=dict(b=3,E=2*8.314))
    return [
        r1.rateCoeff() == 3.14,
        r2.rateCoeff(T=1.0) == 1/np.e,
        r3.rateCoeff(T=2.0) == 8/np.e]

@ListTest
def test_CoeffLaws_get():
    return [
        Reaction._CoeffLaws.getcopy('arr') == Reaction._CoeffLaws.arr,
        Reaction._CoeffLaws.getcopy_all() == Reaction._CoeffLaws._dict_all,
        Reaction._CoeffLaws.getcopy_builtin() == Reaction._CoeffLaws._dict_builtin]

@ListTest
def test_CoeffLaws_update_remove_reset():
    def _law1(**kwargs): return 0.0
    def _law2(**kwargs): return 0.0
    Reaction._CoeffLaws.reset()
    Reaction._CoeffLaws.update('_1',_law1)
    Reaction._CoeffLaws.update_group(dict(_1=_law1,_2=_law2))
    test = [
        '_1' in Reaction._CoeffLaws._dict_all,
        '_2' in Reaction._CoeffLaws._dict_all,
        '_1' not in Reaction._CoeffLaws._dict_builtin] 
    Reaction._CoeffLaws.remove('_1')
    test += [
        '_1' not in Reaction._CoeffLaws._dict_all,
        '_2' in Reaction._CoeffLaws._dict_all]
    Reaction._CoeffLaws.reset()
    test += [
        Reaction._CoeffLaws._dict_all == Reaction._CoeffLaws._dict_builtin]
    return test


# ============ Tests on Errors ============ #

def test_init_notimplemented():
    try:
        Reaction(reversible=True)
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)
    try:
        Reaction(**{'type':'duplicate'})
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)
    try:
        Reaction(coeffLaw='_')
    except NotImplementedError as err:
        assert(type(err) == NotImplementedError)
        
def test_CoeffLaws_changebuiltin():
    def _law1(**kwargs): return 0.0
    def _law2(**kwargs): return 0.0
    Reaction._CoeffLaws.reset()
    try:
        Reaction._CoeffLaws.update('arr',_law1)
    except KeyError as err:
        assert(type(err) == KeyError)
    try:
        Reaction._CoeffLaws.update_group(dict(_1=_law1,arr=_law2))
    except KeyError as err:
        assert(type(err) == KeyError)
    try:
        Reaction._CoeffLaws.remove('arr')
    except KeyError as err:
        assert(type(err) == KeyError)
    Reaction._CoeffLaws.reset()
        
def test_CoeffLaws_input():
    try:
        Reaction(coeffLaw='const', coeffParams=dict(k=-1.0)).rateCoeff()
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='arr').rateCoeff(T=-1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='arr', coeffParams=dict(A=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='arr', coeffParams=dict(R=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='modarr').rateCoeff(T=-1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='modarr', coeffParams=dict(A=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)
    try:
        Reaction(coeffLaw='modarr', coeffParams=dict(R=-1.0)).rateCoeff(T=1.0)
    except ValueError as err:
        assert (type(err) == ValueError)