from chemkin_CS207_G9.useful_structure import PartialLockedDict
from chemkin_CS207_G9.mathematical_science import MathModel
from copy import deepcopy
import numpy as np
from chemkin_CS207_G9.CoeffLaw import *


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
        
    _check_params(params): STATICMETHOD
        check if params are valid.
        will get called by the __init__ method.
        it raises `NotImplementedError` if:
            params['TYPE']       != 'Elementary'
            params['coeffLaw'] not in self._CoeffLawDict._dict_all
        it raises `ValueError` if:
            any stoich coeff is either non-integer or negative integer
            params['coeffParams'] cannot pass the param check of the referred coeff law
        NOTE: _check_params calls check_coeffparams method, of the referred MathModel type, 
            to check if params['coeffParams'] are valid. see mathematical_science.py
            
    _specify_CoeffLaw(coeffLaw, coeffParams): STATICMETHOD
        select the right law (MathModel type) to compute reaction rate coefficients, and 
        initialize it with coeffParams. it will get called by the __init__ method.
        INPUTS:  
            coeffLaw:    str, law name, _specify_CoeffLaw will search for the associated
                         MathModel type in the _CoeffLawDict.
            coeffParams: dict, the provided coeff params to initialize the referred MathModel
        OUTPUTS: 
            rateCoeff:   the compute method of the MathModel object, whose type claimed by 
                         coeffLaw, and params initialized by coeffParams
            finalParams: the final version of coeff params. since coeffParams might not contain
                         all the params required by the law model, the model will automatically
                         add what is missing to coeffParams with default values, finalParams is 
                         the result of this process
        NOTE: 
            _specify_CoeffLaw does not check the validity of coeffParams. when calling the 
            __init__ method of the referred MathModel type, it passes in check=False, which 
            avoids param check. see mathematical_science.py, one may want to first do param 
            check, then apply this _specify_CoeffLaw method. 
            
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
        
        
    NOTE:
    ---------------------
        attributes _params and rateCoeff will get initialized.
        inner class _CoeffLawDict does not require instantiation.
        several argument checks will run automatically:
            --------------------------------------------------------------------------------
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
    1H + 1O2 =] 1H + 1OH
    ----------------------------------------
    Reaction Info:
    ID: reaction
    TYPE: Elementary
    reversible: False
    coeffLaw: Arrhenius
    coeffParams: [('A', 2.718281828459045), ('E', 8.314), ('R', 8.314)]
    coeffUnits: []
    ========================================
    >>> r.rateCoeff(T=1.0)
    1.0
    
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
        >>> sorted(Reaction._CoeffLawDict.update('sl', somelaw).getcopy_all())
        ['Arrhenius', 'Constant', 'modArrhenius', 'modifiedArrhenius', 'sl']
        >>> r = Reaction( \
            reactants=dict(H=1,O2=1), \
            products=dict(OH=1,H=1), \
            coeffLaw='sl', \
            coeffParams=dict(A=2.0)\
        )
        >>> r.rateCoeff(T=0.1)
        0.2
        >>> sorted(Reaction._CoeffLawDict.reset().getcopy_all())
        ['Arrhenius', 'Constant', 'modArrhenius', 'modifiedArrhenius']
        """
            
        _dict_builtin = {
            'Constant'         :Constant, 
            'Arrhenius'        :Arrhenius, 
            'modArrhenius'     :modArrhenius, 
            'modifiedArrhenius':modArrhenius
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
        params = {
            'reversible'  : reversible, 
            'TYPE'        : TYPE, 
            'ID'          : ID, 
            'coeffLaw'    : coeffLaw, 
            'coeffParams' : coeffParams,
            'coeffUnits'  : coeffUnits,
            'reactants'   : reactants,
            'products'    : products
        }
        if params['reversible'] == 'yes':
            params['reversible'] = True
        elif params['reversible'] == 'no':
            params['reversible'] = False
        self._check_params(params)
        self._params = deepcopy(params)
        self.rateCoeff, self._params['coeffParams'] = \
            self._specify_CoeffLaw(params['coeffLaw'], params['coeffParams'])

    def is_reversible(self):
        '''reversible method added'''
        return self._params['reversible']
    
    def get_params(self):
        return deepcopy(self._params)
    
    def set_params(self, **kwargs):
        old_params = deepcopy(self._params)
        kwargs_eliminated = deepcopy(kwargs)
        for k in kwargs.keys():
            if k not in old_params:
                kwargs_eliminated.pop(k)
        new_params = deepcopy(old_params)
        new_params.update(**kwargs_eliminated)
        self._params = deepcopy(self._check_params(new_params))
        self.rateCoeff, self._params['coeffParams'] = \
            self._specify_CoeffLaw(new_params['coeffLaw'], new_params['coeffParams'])
        return self
    
    def getReactants(self):
        return self._params['reactants']
    
    def getProducts(self):
        return self._params['products']
    
    def get_species(self):
        sp_dict = self.getReactants().copy()
        sp_dict.update(self.getProducts())
        return sp_dict.keys()
    
    @staticmethod
    def _check_params(params):
        if 'TYPE' in params and params['TYPE'] != 'Elementary':
            raise NotImplementedError(' '.join([
                'TYPE = {}.'.format(params['TYPE']),
                'Non-elementary reaction is not implemented.']))
        if 'coeffLaw' in params:
            if params['coeffLaw'] not in Reaction._CoeffLawDict._dict_all:
                raise NotImplementedError(' '.join([
                    'coeffLaw = {}.'.format(params['coeffLaw']),
                    'Referred reaction rate coefficient law is not implemented.']))
            elif 'coeffParams' in params:
                law_model = Reaction._CoeffLawDict._dict_all[params['coeffLaw']]
                law_model(check=True, **params['coeffParams'])
        if 'reactants' in params:
            for ele,stoich in params['reactants'].items():
                if type(stoich) != int or stoich < 0:
                    raise ValueError(' '.join([
                        'Reactant {}:{}.'.format(ele, stoich),
                        'Stoich. coeff must be a non-negative integer.']))
        if 'products' in params:
            for ele,stoich in params['products'].items():
                if type(stoich) != int or stoich < 0:
                    raise ValueError(' '.join([
                        'Product {}:{}.'.format(ele, stoich),
                        'Stoich. coeff must be a non-negative integer.']))
        return params
    
    @staticmethod         
    def _specify_CoeffLaw(coeffLaw, coeffParams):
        selection = Reaction._CoeffLawDict._dict_all[coeffLaw](check=False, **coeffParams)
        return (selection.compute, selection.get_coeffparams())
    
    def __repr__(self):
        return str(self._params)
    
    def __str__(self):
        streq_left = ' + '.join(  
                ['{}{}'.format(v,k) for k,v in 
                sorted(self._params['reactants'].items(), key=lambda x:x[0])]  )
        streq_right = ' + '.join( 
            ['{}{}'.format(v,k) for k,v in 
            sorted(self._params['products'].items(), key=lambda x:x[0])]  )
        streq_con = ' [=] ' if self.is_reversible() else ' =] '
        streq_full = streq_con.join(  [streq_left, streq_right]  )
        keylist = [
            'TYPE', 'reversible', 
            'coeffLaw', 'coeffParams', 'coeffUnits'
        ]
        strparams = 'ID: ' + str(self._params['ID'])
        for k in keylist:
            item = self._params[k]
            if type(item) == dict:
                item = sorted(item.items(), key=lambda x:x[0])
            strparams = '\n'.join( [strparams, k + ': ' + str(item)] )
        return '\n'.join( [
            '=' * 40, 'Reaction Equation:', streq_full, 
            '-' * 40, 'Reaction Info:', strparams, '=' * 40] )