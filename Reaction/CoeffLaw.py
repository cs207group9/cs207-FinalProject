from mathematical_science import MathModel
from check_and_response import ValueCheck
import numpy as np


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