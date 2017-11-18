
"""
Created on Tue Oct 17 2017
Harvard GSAS
CS207 Group 9
Module chemkin.py 
"""


import numpy as np
from more_itertools import unique_everseen
import xml.etree.ElementTree as ET
from copy import deepcopy



class MathModel:
    """
    THIS IS A BASE CLASS
    
    MathModel is basically a well wrapped function. 
    as a "model", it has hypothesis - some implicit parameters, and some math relationships.
    it can take in some inputs, check their validity, and compute some result. 
    
    MathModel should be able to check the validity of implicit params and provide the math relation 
    without instantiation. But to check the validity of model inputs, it may need information from 
    the instance itself.
    
    * following specifications are vulnerable to further inheritance *
    * these are just an example implementation on the common sense of a MathModel *
    * users are not demanded to follow these implementations, but might find them useful *
    
    
    ATTRIBUTES
    ===========
    
    _default_settings: dict, the default settings. usually this should contain:
                       the name and the default values of the implicit params and model inputs
    _coeffparams:      dict, the implicit parameters of the model, initialized by the __init__ method.
    
    
    METHODS
    ========
    
    compute(self, check=True, **stateparams): compute the result on some inputs.
        INPUTS:  check, boolean, defaults True, whether to start a param check before computation.
                 stateparams, undefined non-positional, the inputs of the model.
        OUTPUTS: result, undefined, the output of the model.
        NOTE:    calls check_stateparams(...) to check inputs
                 calls _kernel(...) to do computation
    
    get_defaults(cls): classmethod, returns the _default_settings dict

    get_coeffparams(self): return the implicit params, in a dict
        
    check_stateparams(self, **stateparams): check validity of the model inputs.
        defaults doing nothing. user are expected to specify it in its inheritors.
        INPUTS:  stateparams, undefined non-positional, model inputs
        OUTPUTS: defaults nothing, but is expected to raise error if params are invalid
    
    check_coeffparams(**coeffparams): staticmethod, check validity of the model implicit params.
        defaults doing nothing. user are expected to specify it in its inheritors.
        INPUTS:  coeffparams, undefined non-positional, implicit params (hypothesis) of the model
        OUTPUTS: defaults nothing, but is expected to raise error if params are invalid
        
    _kernel(**params): staticmethod, the mathematical function.
        computes the result base on both model implicit params and model inputs.
        is the CORE of MathModel - the whole MathModel class is basically a wrapper of this function.
        will get called by the compute(...) method.
        INPUTS:  params, undefined non-positional, combination of implicit params and model inputs.
        OUTPUTS: result, undefined, the output of the model
        NOTE:    is the most efficient implementation one can write on the mathematical relation.
                 is expected to take in as less keyword arguments as possible.
                 is expected to do only computation. no checks should be involved.
                 is not suggested to get called from outside of the class for its vulnerablility to
                 invalid implicit params or invalid model inputs. 
    
    
    INITIALIZATION
    ===============
    __init__(self, check=True, **coeffparams)
    * this is just an example of initialization, with some unversality *
    * details could vary a lot for different models *
    
    INPUTS: 
    -----------
        check:       boolean, if True, check_stateparams(...) will get called to check coeffparams
        coeffparams: implicit params of the model, initializes self._coeffparams
        
        
    EXAMPLE
    ========

    >>> class somelaw(MathModel):
    ...     @staticmethod
    ...     def _kernel(T, E, R):
    ...         return E / (T * R)
    ...     @staticmethod
    ...     def check_coeffparams(R, **other_params):
    ...         if R == 0.0: raise ValueError
    ...     def check_stateparams(self, T, **other_params):
    ...         if T == 0.0: raise ValueError
    >>> somelaw(E=8.314, R=8.314).compute(T=2.0)
    0.5
    
    """

    _default_settings = dict()

    def __init__(self, check=True, **coeffparams):
        if check:
            self.check_coeffparams(**coeffparams)
        self._coeffparams = coeffparams
        
    def compute(self, check=True, **stateparams):
        if check: 
            self.check_stateparams(**stateparams)
        return self._kernel(**self._coeffparams, **stateparams)

    @classmethod
    def get_defaults(cls):
        return cls._default_settings

    def get_coeffparams(self):
        return self._coeffparams
    
    def check_stateparams(self, **stateparams):
        pass
    
    @staticmethod
    def check_coeffparams(**coeffparams):
        pass
    
    @staticmethod
    def _kernel(**params):
        raise NotImplementedError
        
        
class ValueCheck:
    """
    ValueCheck provides formatted response to invalid values.
    
    
    ATTRIBUTES
    ===========
    
    _criterion:  function-like, criterion to decide the validity of some value.
        ------------------------------
        should get called as self._criterion(x):
        INPUTS:  x, numeric type, to-be-judged value
        OUTPUTS: j, boolean, judgement
        
    _name: name of the criterion. will be used in the response(...) method.
    
    
    METHOD
    =======
    
    response(self, x, label, term): response to some value if it passes self._criterion
        INPUTS: x, numeric type, to-be-judged value
                label, str, the math symbel of x
                term, str, the terminology of x
        NOTE:   get reponse when self._criterion(x) == True
                the response will be a ValueError with message formatted:
                [MESSAGE] - (label of x) = (x): (criterion name) (term of x) is prohibited
    
    
    INITIALIZATION
    ===============
    __init__(self, criterion, name)
    
    INPUTS: 
    -----------
        criterion: function-like, initializes _criterion
        name:      str, initializes _name
    
    
    EXAMPLE
    ========
    
    >>> try:
    ...     ValueCheck(lambda x:x>0, 'positive').response(1, 'x', 'integer')
    ... except ValueError as err:
    ...     print(err)
    x = 1.0000000000000000e+00: positive integer is prohibited.
    
    """
    
    def __init__(self, criterion, name):
        # criteron should be a function type
        # criteron(x) returns boolean value
        self._criterion = criterion
        self._name = name
        
    def response(self, x, label, term):
        if self._criterion(x):
            raise ValueError(
                '{} = {:18.16e}: {} {} is prohibited.' \
                .format(label, x, self._name, term))        



class Constant(MathModel):
    """
    Constant reaction rate coefficient, inherited from MathModel
    its implicit param is k, which is valid when positive
    it does not take any model input, and the output is just k itself, 
    so check_stateparams(...) method need not be specified.
    
    
    ATTRIBUTES
    ===========
    _check_np: ValueCheck type, will reponse to non-positive input
    _k:        float, constant reaction rate coefficient
    
    other attributes follow the MathModel pattern, 
    including: _coeffparams, _default_settings
    
    
    METHODS
    ========
    compute(self, **other_params): compute constant reaction rate coefficient
        doesn't (even need to) call _kernel method, just returns self._k
        NOTE: non-positional arg, other_params, are placed in case too many inputs are passed.
              this notation is effective to the end of this file.
    check_coeffparams(k, **other_params): check if k is positive, raise ValueError if not.
        NOTE: calls _check_np.reponse(k)
    _kernel(k, **other_params): mathematical relation, returns k itself.
    
    other methods follow the MathModel pattern, 
    including: check_stateparams(...), get_coeffparams(...), get_defaults(...)
    
    
    
    INITIALIZATION
    ===============
    follows the MathModel pattern
    
    
    EXAMPLE
    ========
    >>> Constant(k=2.0).compute()
    2.0
    
    """

    _default_settings = dict(
        coeffparams=dict(k=1.0), 
        stateparams=dict()
    )

    _check_np = ValueCheck(lambda x:x<=0.0, 'non-positive')
    
    def __init__(self, check=True, 
        k = _default_settings['coeffparams']['k'],
        **other_params
    ):
        if check:
            self.check_coeffparams(k)
        self._k = k
        self._coeffparams = dict(k=k)
        
    def compute(self, check=True, **other_params):
        return self._k
    
    @staticmethod
    def check_coeffparams(k, **other_params):
        Constant._check_np.response(k, 'k', 'reaction rate coefficient')
        
    @staticmethod
    def _kernel(k, **other_params):
        return k


# ================================================================================ #
    
class Arrhenius(MathModel):
    """
    Arrhenius reaction rate coefficient, inherited from MathModel
    
    implicit params, all float:
        A, Arrhenius prefactor, valid when positive, defaults 1.0
        E, reaction energy,     valid as always,     defaults 0.0
        R, ideal gas constant,  valid when positive, defaults 8.314
    model input, all float:
        T, temperature,         valid when positive, defaults 1e-16
        
    by default this model will behave like Constant
    
    
    ATTRIBUTES
    ===========
    _check_np:  ValueCheck type, will reponse to non-positive input
    _A, _E, _R: implicit params, as specified above
    
    other attributes follow the MathModel pattern, 
    including: _coeffparams, _default_settings
    
    
    METHODS
    ========
    compute(self, check=True, T=1e-16, **other_params): 
        compute Arrhenius reaction rate coefficient. follows the MathModel pattern.
    check_coeffparams(A, R, **other_params): 
        check if A, R are positive, raise ValueError if not.
        NOTE: calls _check_np.reponse() on A and R
    check_stateparams(self, T, **other_params):
        check if T is positive, raise ValueError if not
    _kernel(k, **other_params): mathematical relation.
    
    other methods follow the MathModel pattern, 
    including: get_coeffparams(...), get_defaults(...)
    
    
    INITIALIZATION
    ===============
    follows the MathModel pattern
    
    
    EXAMPLE
    ========
    >>> Arrhenius(A=np.e, E=8.314).compute(T=1.0)
    1.0
    
    """

    _default_settings = dict(
        coeffparams=dict(A=1.0, E=0.0, R=8.314), 
        stateparams=dict(T=1e-16)
    )
    
    _check_np = ValueCheck(lambda x:x<=0.0, 'non-positive')
    
    def __init__(self, check=True,
        A = _default_settings['coeffparams']['A'],
        E = _default_settings['coeffparams']['E'],
        R = _default_settings['coeffparams']['R'],
        **other_params
    ):
        if check:
            self.check_coeffparams(A, R)
        self._A, self._E, self._R = A, E, R
        self._coeffparams = dict(A=A, E=E, R=R)
        
    def compute(self, check=True, 
        T = _default_settings['stateparams']['T'], 
        **other_params
    ):
        if check: 
            self.check_stateparams(T)
        return self._kernel(T, self._A, self._E, self._R)
    
    def check_stateparams(self, T, **other_params):
        self._check_np.response(T, 'T', 'temperature')
        
    @staticmethod
    def check_coeffparams(A, R, **other_params):
        Arrhenius._check_np.response(R, 'R', 'ideal gas constant')
        Arrhenius._check_np.response(A, 'A', 'Arrhenius prefactor')
        
    @staticmethod
    def _kernel(T, A, E, R, **other_params):
        return A * (np.e ** (-E / (R * T)))

    
    
# ================================================================================ #
    
class modArrhenius(MathModel):
    """
    Modified Arrhenius reaction rate coefficient, inherited from MathModel
    
    implicit params, all float:
        A, Arrhenius prefactor,          valid when positive, defaults 1.0
        b, modified Arrhenius parameter, valid when real,     defaults 0.0
        E, reaction energy,              valid as always,     defaults 0.0
        R, ideal gas constant,           valid when positive, defaults 8.314
    model input, all float:
        T, temperature,                  valid when positive, defaults 1e-16
        
    by default this model will behave like Constant
    if b is the only one that follows the default value, 
    this model will behave just like the Arrhenius
    
    
    ATTRIBUTES
    ===========
    _check_np:      ValueCheck type, will reponse to non-positive input
    _A, _b, _E, _R: implicit params, as specified above
    
    other attributes follow the MathModel pattern, 
    including: _coeffparams, _default_settings

    
    METHODS
    ========
    compute(self, check=True, T=1e-16, **other_params): 
        compute Arrhenius reaction rate coefficient. follows the MathModel pattern.
    check_coeffparams(A, R, **other_params): 
        check if A, R are positive, raise ValueError if not.
        NOTE: calls _check_np.reponse() on A and R
    check_stateparams(self, T, **other_params):
        check if T is positive, raise ValueError if not
    _kernel(k, **other_params): mathematical relation.
    
    other methods follow the MathModel pattern, 
    including: get_coeffparams(...), get_defaults(...)
    
    
    INITIALIZATION
    ===============
    follows the MathModel pattern
    
    
    EXAMPLE
    ========
    >>> modArrhenius(A=np.e, b=-1.0, E=4.157).compute(T=0.5)
    2.0

    """

    _default_settings = dict(
        coeffparams=dict(A=1.0, b=0.0, E=0.0, R=8.314), 
        stateparams=dict(T=1e-16)
    )
    
    _check_np = ValueCheck(lambda x:x<=0.0, 'non-positive')
    
    def __init__(self, check=True, 
        A = _default_settings['coeffparams']['A'],
        b = _default_settings['coeffparams']['b'],
        E = _default_settings['coeffparams']['E'],
        R = _default_settings['coeffparams']['R'],
        **other_params
    ):
        if check:
            self.check_coeffparams(A, R)
        self._A, self._b, self._E, self._R = A, b, E, R
        self._coeffparams = dict(A=A, b=b, E=E, R=R)
        
    def compute(self, check=True, 
        T = _default_settings['stateparams']['T'], 
        **other_params
    ):
        if check: 
            self.check_stateparams(T)
        return self._kernel(T, self._A, self._b, self._E, self._R)
    
    def check_stateparams(self, T, **other_params):
        self._check_np.response(T, 'T', 'temperature')
        
    @staticmethod
    def check_coeffparams(A, R, **other_params):
        modArrhenius._check_np.response(A, 'A', 'Arrhenius prefactor')
        modArrhenius._check_np.response(R, 'R', 'ideal gas constant')
        
    @staticmethod
    def _kernel(T, A, b, E, R, **other_params):
        return A * (T ** b) * (np.e ** (-E / (R * T)))



class PartialLockedDict:
    """
    THIS IS A BASECLASS
    
    PartialLockedDict conceptually consists one built-in dict and one outer dict.
    The built-in dict is considered constant and users are not suggested to change it.
    The outer dict is defined by the user and is subjected to all kinds of changes.
    PartialLockedDict provides methods accessing data with high security.
    
    
    
    METHODS
    ========
    these are all classmethods
    
    _error_change_builtin(cls, key):
        throws KeyError based on the input key.
        Call this function when built-in dict is going to get changed.
    
    _get_all(cls):
        * currently not implemented *
        return the dict covering both built-in dict and outer dict
        OUTPUT: * should be * dict (reference)
        
    _get_builtin(cls):
        * currently not implemented *
        return the built-in dict
        OUTPUT: * should be * dict (reference)
    
    reset(cls):
        * currently not implemented *
        clear the outer dict
        OUTPUT: * should be * cls
    
    getcopy(cls, key):
        retrieve the value with key in the whole dict
        INPUTS:  key, dict-key-like, the key to the value of interest
        OUTPUTS: value, dict-value-like, the value retrieved
    
    getcopy_all(cls):
        returns a deepcopy of the dict covering both built-in dict and outer dict
        OUTPUTS: dict (deepcopy)
        
    getcopy_builtin(cls):
        returns a deepcopy of the built-in dict
        OUTPUTS: dict (deepcopy)
        
    update(cls, key, value):
        updates the outer dict's dict-item indexed key with value
        if key in built-in dict, calls cls._error_change_builtin(cls, key) to raise KeyError
        INPUTS:  key, dict-key-like, the key to the item to be updated
                 value, dict-value-like, the value of update
        OUTPUTS: cls
    
    update_group(cls, dict_update):
        updates the outer dict with dict_update
        if dict_update contains any key that is also in the built-in dict, 
        calls cls._error_change_builtin(cls, key) to raise KeyError
        INPUTS:  dict_update, dict, the group of items as the update
        OUTPUTS: cls
        
    remove(cls, key):
        remove the key indexed dict-item in the outer dict
        if key in built-in dict, calls cls._error_change_builtin(cls, key) to raise KeyError
        INPUTS:  key, dict-key-like, the key to the item to be removed
        OUTPUTS: cls
    
    """
    @classmethod
    def _error_change_builtin(cls, key):
        raise KeyError
        
    @classmethod
    def _get_all(cls):
        raise NotImplementedError
        
    @classmethod
    def _get_builtin(cls):
        raise NotImplementedError
        
    @classmethod
    def reset(cls):
        raise NotImplementedError
        
    @classmethod
    def getcopy(cls, key):
        return cls._get_all()[key]
    
    @classmethod
    def getcopy_all(cls):
        return deepcopy(cls._get_all())
    
    @classmethod
    def getcopy_builtin(cls):
        return deepcopy(cls._get_builtin())
    
    @classmethod
    def update(cls, key, value):
        if key in cls._get_builtin():
            cls._error_change_builtin(key)
        cls._get_all()[key] = value
        return cls
    
    @classmethod
    def update_group(cls, dict_update):
        for key in dict_update.keys():
            if key in cls._get_builtin():
                cls._error_change_builtin(key)
        for key,value in dict_update.items():
            cls._get_all()[key] = value
        return cls
    
    @classmethod
    def remove(cls, key):
        if key in cls._get_builtin():
            cls._error_change_builtin(key)
        del cls._get_all()[key]
        return cls


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
            params['reversible'] == True
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
        
        
    NOTE:
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
    1H + 1O2 => 1H + 1OH
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
        ['Arrhenius', 'Constant', 'modArrhenius', 'sl']
        >>> r = Reaction( \
            reactants=dict(H=1,O2=1), \
            products=dict(OH=1,H=1), \
            coeffLaw='sl', \
            coeffParams=dict(A=2.0)\
        )
        >>> r.rateCoeff(T=0.1)
        0.2
        >>> sorted(Reaction._CoeffLawDict.reset().getcopy_all())
        ['Arrhenius', 'Constant', 'modArrhenius']
        """
            
        _dict_builtin = {
            'Constant'    :Constant, 
            'Arrhenius'   :Arrhenius, 
            'modArrhenius':modArrhenius
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
        self._params = deepcopy(self._check_params(params))
        self.rateCoeff, self._params['coeffParams'] = \
            self._specify_CoeffLaw(params['coeffLaw'], params['coeffParams'])
    
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
        if 'reversible' in params and params['reversible'] == True:
            raise NotImplementedError(
                'Reversible reaction is not implemented.')
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
        streq_full = ' => '.join(  [streq_left, streq_right]  )
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


class ReactionSystem:

    """
    
    Class ReactionSystem(reactions_ls, species_ls):
    ReactionSystem formats and calculates information for a system of reactions, 
    including progress rate and reaction rate. It stores an array
    of reactions, and an array of species that interact in these reactions.
    An object of this class can be queried for reaction rates of its species and progress rates of its reactions.
    
    INPUTS
    ======
    reactions_ls: list of Reaction objects.
    
    species_ls: optional list of strings, with one specie per string. The list of species
    must match the total set of species in the given Reactions. Order is important
    and is maintained throughout the class.
    
    **initial_state: optional parameter indicating the initial state of the reaction.
    Can contain temperature and an array of concentrations.
           
    ATTRIBUTES
    ===========
    
    _reactions_ls: list of class Reaction, reactions included in the system
    
    _species_ls: list of str, concentration element
    
    _T: float, temperature
    
    _concs: array of float, concentration
    
    METHODS:
    ========
    set_state(self, **kwargs): 
            set initial state Temperature kwargs['T'] and concentration kwargs['concs']
            if length of e_ls is not equal to number of concentration kwargs['concs'], raise ValueError
    
    get_state(self):
            return initial state
            OUTPUTS: dictionary
    
    __len__(self):
            return number of reaction
            OUTPUTS: integer
            
    __repr__(self):
            return a wrapped dict of all params for every reaction, namely str(self._params)
            OUTPUTS: representational str
    
    rateCoeff(self):
            function in class Reaction to calculate coefficient rate under given conditions
            OUTPUTS: k, float, reaction rate coefficient
    
    calculate_nu_1(self):
            return formatted reactant matrix
            OUTPUTS: matrix of float
            
    calculate_nu_2(self):
            return formatted product matrix
            OUTPUTS: matrix of float
    
    get_progress_rate(self):
            return the progress rate of a system of irreversible, elementary reactions
            OUTPUTS: numpy array of floats, size: num_reactions, progress rate of each reaction
            
    get_reac_rate(self):
            returns the reaction rate of a system of irreversible, elementary reactions
            OUTPUTS: numpy array of floats, size: num_species, reaction rate of each specie
            
    compute_all(self):
            return the reaction rate of a system reactions without calling the other methods
            OUTPUTS: numpy array of floats, size: num_species, reaction rate of each specie
            
    EXAMPLES:
    =========
    >>> r_ls = []
    >>> r_ls.append(Reaction(\
            reactants=dict(H=1,O2=1), products=dict(OH=1,O=1),\
            coeffLaw='Arrhenius', coeffParams=dict(A=2.0)\
        ))
    >>> r_ls.append(Reaction(\
            reactants=dict(H2=1,O=1), products=dict(OH=1,H=1),\
            coeffLaw='Arrhenius', coeffParams=dict(A=2.0)\
        ))
    >>> concs = {'H':2, 'O2': 1, 'OH':0.5, 'O':1, 'H2':1}
    >>> species = ['H', 'O2', 'OH', 'O', 'H2']
    >>> rs = ReactionSystem(r_ls, species_ls= species, initial_concs = concs);
    >>> rs.get_reac_rate()
    array([-2., -4.,  6.,  2., -2.])
    """
    
    def __init__(self, reactions_ls, species_ls = [], initial_T = 273, initial_concs = {}):
        
        if not reactions_ls:
            raise ValueError("Reaction array is empty or None.")
            
        for s in species_ls:
            if not isinstance(s, str): 
                raise TypeError("input species_ls array contains elements that are not of type string")
                
        for r in reactions_ls:
            if not isinstance(r, Reaction): 
                raise TypeError("input reactions_ls array contains elements that are not instances of Reaction")
        
        self._reactions_ls = reactions_ls
        self._species_ls = species_ls
        
        if not self._species_ls:
            self._user_defined_order = False
            self.update_species()
        else:
            self._user_defined_order = True
            
        self.set_temp(initial_T)
        if initial_concs:
            self.set_concs(initial_concs)    
        else:
            self._concs = {}
       
    def set_temp(self, T):
        if (T <= 0):
            raise ValueError("T = {0:18.16e}: Negative Temperature is prohibited!".format(T))
         
        self._T = T    
        
    def get_temp(self):
        return self._T
    
    def set_concs(self, concs):
        
        if len(concs.keys()) != len(self._species_ls):
            raise ValueError("Length of concentrations ("+str(len(concs.keys()))+") and species arrays ("+str(len(self._species_ls))+") do not match. Update your concentrations.")
            
        for i, conc in enumerate(concs.values()):
            if conc < 0:
                raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(i, conc))

        self._concs = concs
    
    def get_concs(self):
        return self._concs
    
    def __len__(self):
        return len(self._reactions_ls)
    
    def __repr__(self):
        # TODO: add info about concentrations
        repr_ls = ", ".join([repr(r) for i,r in enumerate(self._reactions_ls)])
        repr_ls = "( " + repr_ls + " )"
        return repr_ls
    
    def __str__(self):
        str_ls = "ReactionSystem object with following Reactions: \n"
        for i,r in enumerate(self._reactions_ls):
            str_ls += "\nReaction "+str(i)+": \n"+str(r)+"\n"
        return str_ls
    
    def add_reaction(self, reaction):
        if not isinstance(reaction, Reaction):
            raise ValueError('Input parameter is not instance of Reaction')
            
        self._reactions_ls.append(reaction)
        self.update_species()
        
    def update_species(self):
        species_list = []
        for r in self._reactions_ls:
            species_list+=r.get_species()
        if self._user_defined_order:
            for specie in species_list:
                if specie not in self._species_ls:
                    self._species_ls.append(specie)
        else:
            species_list = []
            for r in self._reactions_ls:
                species_list+=r.get_species()
            self._species_ls = list(unique_everseen(species_list))
            self._species_ls = sorted(self._species_ls)
        
    def get_species(self, update = True):
        # This can be used by the user to check the internal order of species
        if update:
            self.update_species()
            
        return self._species_ls
        
    def get_reac_rate_coefs(self):
        if not self._T:
            raise ValueError("Temperature not yet defined. Call set_state() before calling this function.")
        k = np.zeros(len(self._reactions_ls))
        for n, r in enumerate(self._reactions_ls):
            k[n] = r.rateCoeff(T = self._T)
            
        return k
    
    def get_nu_1(self):
        nu_1 = np.zeros([len(self._species_ls), len(self._reactions_ls)])
        
        for n, r in enumerate(self._reactions_ls):
            reactants = r.getReactants()
            for idx, e in enumerate(self._species_ls):
                nu_1[idx, n] = reactants[e] if e in reactants else 0
                if nu_1[idx, n] < 0:
                    raise ValueError("nu_{0}1 = {1}:  Negative stoichiometric coefficients are prohibited!".format(idx, nu_1[idx, n]))

        return nu_1
    
    def get_nu_2(self):
        nu_2= np.zeros([len(self._species_ls), len(self._reactions_ls)])
        
        for n, r in enumerate(self._reactions_ls):
            products = r.getProducts()
            for idx, e in enumerate(self._species_ls):
                nu_2[idx, n] = products[e] if e in products else 0
                if nu_2[idx, n] < 0:
                    raise ValueError("nu_{0}2 = {1}:  Negative stoichiometric coefficients are prohibited!".format(idx, nu_2[idx, n]))

        return nu_2
    
    def get_progress_rate(self):
        
        if not self._concs:
            raise ValueError("Concentrations not yet defined. Call set_state() before calling this function.")
            
        if len(self._concs) != len(self._species_ls):
            raise ValueError("Dimensions of concentrations and species arrays do not match. Update your concentrations.")
            
        k = self.get_reac_rate_coefs()
        nu_react = self.get_nu_1()
        #print('In progress_rate, nu_react is', nu_react)
        progress_rate = k # Initialize progress rates with reaction rate coefficients
        
        for j in range(len(progress_rate)):
            for i, sp in enumerate(self._species_ls):
                nu_ij = nu_react[i,j]
                progress_rate[j] *= self._concs[sp]**nu_ij     
                
        return progress_rate
    
    def get_reac_rate(self,species_idx = []):
            
        nu_react = self.get_nu_1()
        nu_prod = self.get_nu_2()
        nu = nu_prod - nu_react
        
#        print('nu_react', nu_react)
#        print('nu_prod', nu_prod)
#        print('nu', nu)
        progress_rate = self.get_progress_rate()
            
        if not species_idx:
            return np.dot(nu, progress_rate)
        else:
            return np.dot(nu[species_idx,:], progress_rate)
     
        




class xml2dict:
    """
    xml2dict turns an XML file into a array of all the species involved into the system of
    reactions and a list of dictionaries. This latter contains a dictionary for every single 
    reaction of the system of reactions. Each dictionary contains the information about the 
    reactants, the products, the stoichiometric coefficients and the kinetic law for the 
    reaction constant (Arrhenius Law, Modified Arrhenius Law, Constant Law, and so forth).
    where list of dictionary Reaction contains all the infomation from one given reaction.
    
    INPUTS
    ======
    
    file: XML file.
          The format of the this input file must follow
          the format given by Prof. David Sondak.
          
    METHODS
    =======
    
    parse(self, file): 
        extract all the information contained into the XML file provided by
        the user, namely the names of all the species involved in the system
        of reactions, stored into the array self.Species, and all the information
        about every reaction, stored into self.ListDictionaries
        
    get_info(self):
        return the array self.Species containing the names of the species involved
        and the list of dictionaries self.ListDictionaries
        OUTPUTS: self.Species, self.ListDictionaries
           
    __repr__(self):
        return a string of all the sppecies and all the information contained in 
        self.dictionaries
        OUTPUTS: str
    
    
    EXAMPLES
    =========
    >>> reader = xml2dict()
    >>> reader.parse('./final/rxns.xml')
    >>> reader.get_info()[0][0]
    'H'
    """

    def parse(self, file):
        self.file = file
        tree = ET.parse(file)
        root = tree.getroot()

        SpeciesArray=root.find('phase').find('speciesArray')
        self.Species = SpeciesArray.text.strip().split(" ")
    
        self.ListDictionaries = []
    
        #Now: go through every reaction to read the features:
    
        for reaction in root.find('reactionData').findall('reaction'):
        
            #Initialization of the variables
        
            Dict = {}
            reactants = []
            products = []
            Nup = []
            Nupp = []
        
            ListReactants = reaction.find('reactants').text.split()
            for elementsR in ListReactants:
                specie, nu = elementsR.split(':')
                reactants.append(specie)
                Nup.append(int(nu))
            ListProducts = reaction.find('products').text.split()
            for elementsP in ListProducts:
                specie, nu = elementsP.split(':')
                products.append(specie)
                Nupp.append(int(nu))
            for name in reaction.find('rateCoeff'):
                Law = name.tag
                ListCoeffTag = []
                ListCoeffValue = []
                for coeff in name:
                    ListCoeffTag.append(coeff.tag)
                    ListCoeffValue.append(float(coeff.text))
                #    if len(coeff.attrib) != 0:
                #        ListCoeffUnits.append(coeff.attrib['units'])
                #    else:
                #        ListCoeffUnits.append('dimensionless')
            Dict['coeffParams'] = dict(zip(ListCoeffTag, ListCoeffValue))
            #Dict['coeffUnits'] = dict(zip(ListCoeffTag,ListCoeffUnits))
            Dict['ID'] = reaction.attrib['id']
            Dict['reversible'] = reaction.attrib['reversible']
            Dict['TYPE'] = reaction.attrib['type']
            Dict['reactants'] = dict(zip(reactants, Nup))
            Dict['products'] = dict(zip(products, Nupp))
            Dict['coeffLaw'] = Law
            self.ListDictionaries.append(Dict)
    
    def get_info(self):
        return self.Species, self.ListDictionaries
    
    def __repr__(self):
        return '( ' + str(self.Species) + ', ' + str(self.ListDictionaries) + ' )'

    def __str__(self):
        return str(self.Species) + ' ' + str(self.ListDictionaries)



