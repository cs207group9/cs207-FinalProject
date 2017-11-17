import numpy as np



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

# ================================================================================ #



class BackwardLaw:
    """Methods for calculating the backward reaction rate.

    Cp_over_R: Returns specific heat of each specie given by 
               the NASA polynomials.
    H_over_RT:  Returns the enthalpy of each specie given by 
                the NASA polynomials.
    S_over_R: Returns the entropy of each specie given by 
              the NASA polynomials.
    backward_coeffs:  Returns the backward reaction rate 
                      coefficient for reach reaction.

    Please see the notes in each routine for clarifications and 
    warnings.  You will need to customize these methods (and 
    likely the entire class) to suit your own code base.  
    Nevertheless, it is hoped that you will find these methods 
    to be of some use.
    """

    def __init__(self):
        self.p0 = 1.0e+05
        self.R = 8.3144598

    def Cp_over_R(self, a, T):

        # WARNING:  This line will depend on your own data structures!
        # Be careful to get the correct coefficients for the appropriate 
        # temperature range.  That is, for T <= Tmid get the low temperature 
        # range coeffs and for T > Tmid get the high temperature range coeffs.

        Cp_R = (a[:,0] + a[:,1] * T + a[:,2] * T**2.0 \
                + a[:,3] * T**3.0 + a[:,4] * T**4.0)

        return Cp_R

    def H_over_RT(self, a, T):

        # WARNING:  This line will depend on your own data structures!
        # Be careful to get the correct coefficients for the appropriate 
        # temperature range.  That is, for T <= Tmid get the low temperature 
        # range coeffs and for T > Tmid get the high temperature range coeffs.

        H_RT = (a[:,0] + a[:,1] * T / 2.0 + a[:,2] * T**2.0 / 3.0 \
                + a[:,3] * T**3.0 / 4.0 + a[:,4] * T**4.0 / 5.0 \
                + a[:,5] / T)

        return H_RT
               

    def S_over_R(self, a, T):

        # WARNING:  This line will depend on your own data structures!
        # Be careful to get the correct coefficients for the appropriate 
        # temperature range.  That is, for T <= Tmid get the low temperature 
        # range coeffs and for T > Tmid get the high temperature range coeffs.

        S_R = (a[:,0] * np.log(T) + a[:,1] * T + a[:,2] * T**2.0 / 2.0 \
               + a[:,3] * T**3.0 / 3.0 + a[:,4] * T**4.0 / 4.0 + a[:,6])

        return S_R

    def equilibrium_coeffs(self, a, nu, T):

        # Change in enthalpy and entropy for each reaction
        delta_H_over_RT = np.dot(nu.T, self.H_over_RT(a, T))
        delta_S_over_R = np.dot(nu.T, self.S_over_R(a, T))

        # Negative of change in Gibbs free energy for each reaction 
        delta_G_over_RT = delta_S_over_R - delta_H_over_RT

        # Prefactor in Ke
        fact = self.p0 / self.R / T

        # gamma
        gamma = np.sum(nu, axis=0)

        # Ke
        ke = fact**self.gamma * np.exp(delta_G_over_RT)

        return ke
