from useful_structure import PartialLockedDict
from mathematical_science import MathModel
from copy import deepcopy
import numpy as np
import CoeffLaw


class Reaction:
    """
    Class Reaction:
    Reaction keeps all the information from one given reaction. It also helps to select 
    the right law function, as attribute rateCoeff, to compute the reaction rate coefficient 
    based on the classification of the given reaction. In the inner class _CoeffLawDict several 
    laws including constant coeffs, Arrhenius coeffs and Modified Arrhenius coeffs have been 
    implemented, and _CoeffLawDict forms up a dict-like structure to manage them.
    
    
    
    ATTRIBUTES
    ===========
    
    _params: dict, records the parameters has has built up the instance.
        it is initialized by __init__ and can be set to other values using set_params method.
        the keys of _params are fixed to the following list and should not be changed:
        [KEYS] - reversible, TYPE, ID, coeffLaw, coeffParams, coeffUnits, reactants, products
    
    rateCoeff: function, typically called as self.rateCoeff(check=True, **state)
        this function compute the reaction rate coefficient under certain state.
        it is selected from the _CoeffLawDict by __init__, and reseting self._params should 
        automatically respecify this rateCoeff. 
        --------------------------------------------
        For function rateCoeff(self, check=True, **state):
        INPUTS: 
            check, boolean, decides whether to check the state input, defaults True
            state, non-positional args, currently known as potentially containing:
                'T': float, temperature under which reaction happens, valid when positive
        OUTPUTS: k, float, reaction rate coefficient
        
    _CoeffLawDict: inner class, dict-like structure
        _CoeffLawDict Keeps and manages the law functions (MathModel type, see CoeffLaw.py) 
        that might be used to compute the reaction rate coefficients. Each function is 
        associated with a key - mostly their name, in a string. It also provides several 
        dict-like methods. All these will be further specified inside the _CoeffLawDict.
    
    
    
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
        will get called by the __init__ method.
        it raises `NotImplementedError` if:
            self._params['reversible'] == True
            self._params['TYPE']       != 'Elementary'
            self._params['coeffLaw'] not in self._CoeffLawDict._dict_all
        it raises `ValueError` if:
            any stoich coeffs in self._params['reactants'] and self._params['products']
            are either non-integer or negative integer
        NOTE: _check_params does not check if self._params['coeffParams'] are valid.
            if wanted, the check_coeffparams method of the referred MathModel type should be
            called seperately from this _check_params. see _specify_rateCoeff below.
            
    _specify_rateCoeff(self):
        select the right law (MathModel type) to compute reaction rate coefficients, 
        and initialize it with self._params['coeffParams']. 
        self will get changed - attribute rateCoeff will get updated.
        will get called by the __init__ method.
        OUTPUTS: self.rateCoeff, function
            self.rateCoef(...) itself does not need self._params['coeffParams'] as inputs
        NOTE: _specify_rateCoeff does not check the validity of self._params['coeffParams']
            explicitly. However, it will call the __init__ method of a MathModel type, which 
            is expected to call self.check_coeffparams(...) to check the inputing coeffParams 
            by default. If the coeffParams are invalid, a ValueError is expected to get raised 
            from inside that check_coeffparams method.
            
    __repr__(self):
        return a wrapped dict of all params, namely str(self._params)
        OUTPUTS: representational str, valid input for eval()
        
    __str__(self):
        return a str to show the contents of self. 
        when printed out, there will be two parts:
            the reaction equation, in a chemistry convention
            the params list, in a 'param name: param value' fashion
        OUTPUTS: descriptive str
        
    
    
    INITIALIZATION
    ===============  
    
    INPUTS:
    ---------------------
    
        ID:          str keyword, defaults 'reaction', reaction id

        reversible:  boolean keyword, defaults False, reversibility
                     if True, will raise NotImplementedError

        TYPE:        str keyword, defaults 'Elementary', reaction type, 
                     if not 'Elementary', will raise NotImplementedError

        coeffLaw:    str keyword, defaults 'Constant', 
                     name of the law that computes the reaction rate coefficients
                     if not in Reaction._CoeffLawDict._dict_all, will raise NotImplementedError

        coeffParams: dict keyword, defaults {}, param values required by coeffLaw
                     if not empty, should be in form of paramName(str): paramValue(float)
                     should not contain state params such as temperature and concentration
                     coeffParams will be checked based on the input of coeffLaw,
                     if such check cannot pass, ValueError will be raised

        coeffUnits:  dict keyword, defaults {}, param units associated with coeffParams
                     if not empty, should be in form of paramName(str): paramUnit(str)

        reactants:   dict keyword, defaults {}, reactants
                     if not empty, should be in form of reactantName(str): stoichCoeff(int)
                     non-int or negative stoich. coeffs will raise ValueError

        products:    dict keyword, defaults {}, products
                     if not empty, should be in form of productName(str): stoichCoeff(int)
                     non-int or negative stoich. coeffs will raise ValueError

        kwargs:      some non-positional arguments that are currently not helpful
        
        
    NOTES:
    ---------------------
        attributes _params and rateCoeff will get initialized.
        inner class _CoeffLawDict does not require instantiation.
        several argument checks will run automatically:
            --------------------------------------------------------------------------------
            reversible           if True                                 NotImplementedError
            TYPE                 if not 'Elementary'                     NotImplementedError
            coeffLaw             if not in _CoeffLawDict._dict_all       NotImplementedError
            coeffParams          if cannot pass the param check          ValueError
                                 provided by the claimed coeffLaw
            reactants, products  if non-integer or negative integer      ValueError
                                 stoich coeffs detected
            --------------------------------------------------------------------------------
            
            
    
    EXAMPLES
    =========
    
    >>> r = Reaction( \
            reactants=dict(H=1,O2=1), \
            products=dict(OH=1,H=1), \
            coeffLaw='Arrhenius', \
            coeffParams=dict(A=np.e, E=8.314)\
        )
    >>> eval(repr(r))['coeffLaw']
    'Arrhenius'
    >>> print(str(r))
    ========================================
    Reaction Equation:
    1H + 1O2 [=] 1OH + 1H
    ----------------------------------------
    Reaction Info:
    reversible: False
    TYPE: Elementary
    ID: reaction
    coeffLaw: Arrhenius
    coeffParams: {'A': 2.718281828459045, 'E': 8.314, 'R': 8.314}
    coeffUnits: {}
    reactants: {'H': 1, 'O2': 1}
    products: {'OH': 1, 'H': 1}
    ========================================
    >>> r.rateCoeff(T=1.0)
    1.0
    >>> r.getReactants()
    {'H': 1, 'O2': 1}
    >>> r.set_params(reactants=dict(H=2,O2=2)).getReactants()
    {'H': 2, 'O2': 2}
    
    """
    
    class _CoeffLawDict(PartialLockedDict):
        """
        _CoeffLawDict keeps and manages the built-in laws (CoeffLaw inheritors) that compute 
        the reaction rate coefficients. At the same time it also allow user to add their self
        -defined laws with similar interface - the simplest way is just making a subclass from the 
        CoeffLaw class, and specifying the _kernel staticmethod.
        
        _CoeffLawDict inherits the PartialLockedDict class.
        
        
        ATTRIBUTES
        ===========
        
        built-in laws (CoeffLaw inheritors) includes:
            `Constant`     for constant coeffs
            `Arrhenius`    for Arrhenius coeffs
            `modArrhenius` for Modified Arrhenius coeffs
            
        _dict_builtin: dict
            the built-in dict which is not supposed to be changed.
            records mapping relation from names to the associated CoeffLaw inheritors,
            such as: ` 'Constant': CoeffLaw.Constant `
            
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
            return _CoeffLawDict._dict_all, as a reference
            OUTPUTS: _dict_all, dict (reference)
            
        _get_builtin(cls):
            return _CoeffLawDict._dict_builtin, as a reference
            OUTPUTS: _dict_builtin, dict (reference)
            
        other methods stays the same as in the PartialLockedDict class
            
            
        EXAMPLES
        =========
        >>> class somelaw(MathModel):
        ...     @staticmethod
        ...     def _kernel(T, A, **other_params):
        ...         return T * A
        >>> Reaction._CoeffLawDict.update('sl', somelaw).getcopy_all().keys()
        dict_keys(['Constant', 'Arrhenius', 'modArrhenius', 'sl'])
        >>> r = Reaction( \
            reactants=dict(H=1,O2=1), \
            products=dict(OH=1,H=1), \
            coeffLaw='sl', \
            coeffParams=dict(A=2.0)\
        )
        >>> r.rateCoeff(T=0.1)
        0.2
        >>> Reaction._CoeffLawDict.reset().getcopy_all().keys()
        dict_keys(['Constant', 'Arrhenius', 'modArrhenius'])
        """
            
        _dict_builtin = {
            'Constant'    :CoeffLaw.Constant, 
            'Arrhenius'   :CoeffLaw.Arrhenius, 
            'modArrhenius':CoeffLaw.modArrhenius
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
        self._specify_rateCoeff(coeffLaw, coeffParams)
        # this brings up the attribute self.rateCoeff
    
    def get_params(self):
        return deepcopy(self._params)
    
    def set_params(self, **kwargs):
        old_params = deepcopy(self._params)
        kwargs_eliminated = deepcopy(kwargs)
        for k in kwargs.keys():
            if k not in self._params:
                kwargs_eliminated.pop(k)
        self._params.update(**kwargs_eliminated)
        if self._params != old_params:
            self._check_params()
            coeffLaw = self._params['coeffLaw']
            coeffParams = self._params['coeffParams']
            if (old_params['coeffLaw'] != coeffLaw \
                or old_params['coeffParams'] != coeffParams):
                self._specify_rateCoeff(coeffLaw, coeffParams)
        return self
    
    def getReactants(self):
        return self._params['reactants']
    
    def getProducts(self):
        return self._params['products']
    
    def get_species(self):
        return self.getReactants()+self.getProducts()
    
    def _check_params(self):
        if self._params['reversible']:
            raise NotImplementedError(
                'Reversible reaction is not implemented.')
        if self._params['TYPE'] != 'Elementary':
            raise NotImplementedError(' '.join([
                'TYPE = {}.'.format(self._params['TYPE']),
                'Non-elementary reaction is not implemented.']))
        if not self._params['coeffLaw'] in self._CoeffLawDict._dict_all:
            raise NotImplementedError(' '.join([
                'coeffLaw = {}.'.format(self._params['coeffLaw']),
                'Refered reaction rate coefficient law is not implemented.']))
        for ele,stoich in self._params['reactants'].items():
            if type(stoich) != int or stoich < 0:
                raise ValueError(' '.join([
                    'Reactant {}:{}.'.format(ele, stoich),
                    'Stoich. coeff must be a non-negative integer.']))
        for ele,stoich in self._params['products'].items():
            if type(stoich) != int or stoich < 0:
                raise ValueError(' '.join([
                    'Product {}:{}.'.format(ele, stoich),
                    'Stoich. coeff must be a non-negative integer.']))
                
    def _specify_rateCoeff(self, coeffLaw, coeffParams):
        selection = self._CoeffLawDict._dict_all[coeffLaw](**coeffParams)
        self._params['coeffParams'] = selection.get_coeffparams()
        def rateCoeff_specified(check=True, **stateparams):
            return selection.compute(check, **stateparams)
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