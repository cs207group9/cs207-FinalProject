from BaseClass import PartialLockedDict
from copy import deepcopy
import numpy as np



class Reaction:
    """
    Reaction keeps all the infomation from one given reaction. It also helps to select 
    the right law function, as attribute rateCoeff, to compute the reaction rate coefficient 
    based on the classification of the given reaction. In the inner class _CoeffLaws several 
    laws including constant coeffs, Arrhenius coeffs and Modified Arrhenius coeffs have been 
    implemented, and _CoeffLaws forms up a dict-like structure to manage them.
    
    
    
    INPUTS
    =======
    
    ID:          str keyword, defaults 'reaction', reaction id
    
    reversible:  boolean keyword, defaults False, reversibility
                 if True, will raise NotImplementedError
                 
    TYPE:        str keyword, defaults 'Elementary', reaction type, 
                 if not 'Elementary', will raise NotImplementedError
                 
    coeffLaw:    str keyword, defaults 'Constant', 
                 name of the law that computes the reaction rate coefficients
                 if not in Reaction._CoeffLaws._dict_all, will raise NotImplementedError
                 
    coeffParams: dict keyword, defaults {}, param values required by coeffLaw
                 if not empty, should be in form of paramName(str): paramValue(float)
                 should not contain condition params such as temperature and concentration
    
    coeffUnits:  dict keyword, defaults {}, param units associated with coeffParams
                 if not empty, should be in form of paramName(str): paramUnit(str)
    
    reactants:   dict keyword, defaults {}, reactants
                 if not empty, should be in form of reactantName(str): stoichCoeff(int)
    
    products:    dict keyword, defaults {}, products
                 if not empty, should be in form of productName(str): stoichCoeff(int)
    
    kwargs:      some non-positional arguments that are currently not helpful
    
    
    
    ATTRIBUTES
    ===========
    
    rateCoeff: function, typically called as self.rateCoeff(**conditions)
        this function compute the reaction rate coefficient under certain condition.
        it is selected from the _CoeffLaws by __init__, and reseting self._params should 
        automatically reselect this rateCoeff. 
        --------------------------------------------
        For function rateCoeff(self, **conditions):
        INPUTS: conditions, non-positional params, usually contains:
            'T': float, temperature under which reaction happens
            'concs': array-like, chemical concentrations
        OUTPUTS: k, float, reaction rate coefficient
        
    _CoeffLaws: inner class, dict-like structure
        _CoeffLaws Keeps and manages the law functions that might be used to compute the 
        reaction rate coefficients. Each function is associated with a key - mostly their 
        name, in a string. It also provides several dict-like methods. All these will be 
        further specified inside the _CoeffLaws.
    
    _params: dict, records the parameters building up the instance.
        the keys of self._params are fixed to the following list and should not be changed:
        [KEYS] - reversible, TYPE, ID, coeffLaw, coeffParams, coeffUnits, reactants, products
    
    
    
    METHODS
    ========
    
    get_params(self): 
        return a deepcopy of self._params
        OUTPUTS: self._params, dict (deepcopy)
        
    set_params(self, **kwargs):
        update self._params with kwargs.
        only keys that are originally in _params would be updated.
        will call self._check_params() to see if this update is valid.
        if 'coeffLaw' is updated, will call self._specify_rateCoeff() to reset self.rateCoeff
        INPUTS:  kwargs, non-positional, contains the updates 
        OUTPUTS: self, Reaction instance
        
    getReactants(self): 
        returns the reactants in a dict
        OUTPUTS: self._params['reactants'], dict (deepcopy)
            has the form of (reactant name):(stoich coeff)
        
    getProducts(self): 
        returns the reactants in a dict
        OUTPUTS: self._params['products'], dict (deepcopy)
            has the form of (product name):(stoich coeff)
        
    _check_params(self):
        check if self._params are valid.
        it raises `NotImplementedError` if:
            self._params['reversible'] == True
            self._params['TYPE']       != 'Elementary'
            self._params['coeffLaw'] not in self._CoeffLaws._dict_all
            
    _specify_rateCoeff(self):
        select the right law to compute reaction rate coefficients, 
        and initialize it with self._params['coeffParams']. 
        self will get changed - attribute rateCoeff will be updated
        OUTPUTS: self.rateCoeff, function
            self.rateCoef(**conditions) will not need to take in 
            self._params['coeffParams'] as inputs
            
    __repr__(self):
        return a wrapped dict of all params, namely str(self._params)
        OUTPUTS: representational str, valid input for eval()
        
    __str__(self):
        return a str to show the contents of self. 
        when printed out, there will be two parts:
            the reaction equation, in a chemistry convention
            the params list, in a 'param name: param value' fashion
        OUTPUTS: descriptive str
    
    
    EXAMPLES
    =========
    >>> r = Reaction( \
            reactants=dict(H=1,O2=1), \
            products=dict(OH=1,H=1), \
            coeffLaw='Arrhenius', \
            coeffParams=dict(A=np.e, E=8.314)\
        )
    >>> r.rateCoeff(T=1.0)
    1.0
    >>> r.getReactants()
    {'H': 1, 'O2': 1}
    >>> r.set_params(reactants=dict(H=2,O2=2)).getReactants()
    {'H': 2, 'O2': 2}
    
    """
    
    class _CoeffLaws(PartialLockedDict):
        """
        _CoeffLaws keeps and manages the built-in methods that compute the reaction 
        rate coefficients. At the same time it also allow user to add their self-defined
        methods with similar usage. _CoeffLaws inherits the PartialLockedDict class.
        
        
        ATTRIBUTES
        ===========
        
        built-in functions includes:
            `Constant`     for constant coeffs
            `Arrhenius`    for Arrhenius coeffs
            `modArrhenius` for Modified Arrhenius coeffs
            
        _dict_builtin: dict
            the built-in dict which is not supposed to be changed.
            records mapping relation from names to the associated built-in functions,
            such as: ` 'Constant': const `
            
        _dict_all: dict
            a dict that contains what's in the built-in dict as well as user defined mappings.
            all searches and updates would be made on this dict.
            
            
        METHODS
        ========
        all methods are classmethods inherited from PartialLockedDict, among which the 
        following methods get further specification in this class:
        
        _error_change_builtin(cls, key):
            specified the message thrown by the KeyError
            input key will be clarified in that message
            
        _get_all(cls): 
            return _CoeffLaws._dict_all, as a reference
            OUTPUTS: _dict_all, dict (reference)
            
        _get_builtin(cls):
            return _CoeffLaws._dict_builtin, as a reference
            OUTPUTS: _dict_builtin, dict (reference)
            
            
        EXAMPLES
        =========
        >>> def somelaw(T, A=1.0): return T * A
        >>> Reaction._CoeffLaws.update('sl', somelaw).getcopy_all().keys()
        dict_keys(['Constant', 'Arrhenius', 'modArrhenius', 'sl'])
        >>> r = Reaction( \
            reactants=dict(H=1,O2=1), \
            products=dict(OH=1,H=1), \
            coeffLaw='sl', \
            coeffParams=dict(A=2.0)\
        )
        >>> r.rateCoeff(T=0.1)
        0.2
        >>> Reaction._CoeffLaws.reset().getcopy_all().keys()
        dict_keys(['Constant', 'Arrhenius', 'modArrhenius'])
        """
        

        def const(k=1.0):
            if k <= 0.0:
                raise ValueError(' '.join([
                    'k = {0:18.16e}:'.format(k), 
                    'Non-positive reaction rate coefficient is prohibited.']))
            return k
        def arr(T, R=8.314, A=1.0, E=0.0):
            if T <= 0.0:
                raise ValueError(' '.join([
                    'T = {0:18.16e}:'.format(T),
                    'Non-positive temperature is prohibited.']))
            if A <= 0.0:
                raise ValueError(' '.join([
                    'A = {0:18.16e}:'.format(A),
                    'Non-positive Arrhenius prefactor is prohibited.']))
            if R <= 0.0:
                raise ValueError(' '.join([
                    'R = {0:18.16e}:'.format(R),
                    'Non-positive ideal gas constant is prohibited.']))
            return A * np.exp(-E / (R * T))
        def modarr(T, R=8.314, A=1.0, b=0.0, E=0.0):
            if T <= 0.0:
                raise ValueError(' '.join([
                    'T = {0:18.16e}:'.format(T),
                    'Non-positive temperature is prohibited.']))
            if A <= 0.0:
                raise ValueError(' '.join([
                    'A = {0:18.16e}:'.format(A),
                    'Non-positive Arrhenius prefactor is prohibited.']))
            if R <= 0.0:
                raise ValueError(' '.join([
                    'R = {0:18.16e}:'.format(R),
                    'Non-positive ideal gas constant is prohibited.']))
            return A * (T ** b) * np.exp(-E / (R * T))
            
        _dict_builtin = {
            'Constant'    :const, 
            'Arrhenius'   :arr, 
            'modArrhenius':modarr
        }
        _dict_all = deepcopy(_dict_builtin) 
        
        @classmethod
        def _error_change_builtin(cls, key):
            raise KeyError(' '.join([
                'LawName = {}'.format(key),
                'exists as a built-in law.',
                'Changing a built-in law is prohibited.']))
        @classmethod
        def _get_all(cls):
            return cls._dict_all
        @classmethod
        def _get_builtin(cls):
            return cls._dict_builtin
        @classmethod
        def reset(cls):
            cls._dict_all = deepcopy(cls._dict_builtin)
            return cls
            
    
    def __init__(
        self, 
        reversible  = False, 
        TYPE        = 'Elementary', 
        ID          = 'reaction', 
        coeffLaw    = 'Constant', 
        coeffParams = {},
        coeffUnits  = {},
        reactants   = {},
        products    = {},
        **kwargs
    ):
        self._params = {
            'reversible'  : reversible, 
            'TYPE'        : TYPE, 
            'ID'          : ID, 
            'coeffLaw'    : coeffLaw, 
            'coeffParams' : coeffParams,
            'coeffUnits'  : coeffUnits,
            'reactants'   : reactants,
            'products'    : products
        }
        self._check_params()
        self._specify_rateCoeff()
        # this brings up the attribute self.rateCoeff
    
    def get_params(self):
        return deepcopy(self._params)
    def set_params(self, **kwargs):
        for k in kwargs.keys():
            if k not in self._params:
                kwargs.pop(k)
        self._params.update(**kwargs)
        self._check_params()
        self._specify_rateCoeff()
        return self
    
    def getReactants(self):
        return self._params['reactants']
    def getProducts(self):
        return self._params['products']
    
    def _check_params(self):
        if self._params['reversible']:
            raise NotImplementedError(
                'Reversible reaction is not implemented.')
        if self._params['TYPE'] != 'Elementary':
            raise NotImplementedError(' '.join([
                'TYPE = {}.'.format(self._params['TYPE']),
                'Non-elementary reaction is not implemented.']))
        if not self._params['coeffLaw'] in self._CoeffLaws._dict_all:
            raise NotImplementedError(' '.join([
                'coeffLaw = {}.'.format(self._params['coeffLaw']),
                'Refered reaction rate coefficient law is not implemented.']))
        return deepcopy(self._params)
    def _specify_rateCoeff(self):
        def rateCoeff_specified(**conditions):
            selection = self._params['coeffLaw']
            params = self._params['coeffParams']
            return self._CoeffLaws._dict_all[selection](**params, **conditions)
        self.rateCoeff = rateCoeff_specified
        return self.rateCoeff
    
    def __repr__(self):
        return str(self._params)
    
    def __str__(self):
        streq_lefthand = ' + '.join(
            ['{}{}'.format(v,k) for k,v in self._params['reactants'].items()])
        streq_righthand = ' + '.join(
            ['{}{}'.format(v,k) for k,v in self._params['products'].items()])
        streq_full = ' [=] '.join([streq_lefthand, streq_righthand])
        strparams = '\n'.join(
            [': '.join([str(k), str(v)]) for k,v in self._params.items()])
        return '\n'.join([
            '=' * 40, 'Reaction Equation:', streq_full, 
            '-' * 40, 'Reaction Info:', strparams,
            '=' * 40])