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