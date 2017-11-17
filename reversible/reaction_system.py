from coeff_rate_laws import *



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
    
    def __init__(self, reactions_ls, nasa_base, species_ls = [], initial_T = 273, initial_concs = {}):
        
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

        self._nu_1 = self.get_nu_1()
        self._nu_2 = self.get_nu_2()

        '''
        nasa_base should have method:
            nasa_base.feed_back(species, T), returns a[1:7] of species and T
        '''
        self._nasa_base = nasa_base

       
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
        '''reversible method added'''
        if not self._T:
            raise ValueError("Temperature not yet defined. Call set_state() before calling this function.")
        kf = np.zeros(len(self._reactions_ls))
        for n, r in enumerate(self._reactions_ls):
            kf[n] = r.rateCoeff(T = self._T)
        nu = self._nu_2 - self._nu_1
        a = np.zeros((len(self._species_ls), 7))
        for m, e in enumerate(self._species_ls):
            a[m, :] = self._nasa_base(e, self._T)
        ke = BackwardLaw().equilibrium(a, nu, self._T)
        kb = kf / ke
        return kf, kb
    
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
        '''reversible method added'''
        if not self._concs:
            raise ValueError("Concentrations not yet defined. Call set_state() before calling this function.")
            
        if len(self._concs) != len(self._species_ls):
            raise ValueError("Dimensions of concentrations and species arrays do not match. Update your concentrations.")
            
        kf, kb = self.get_reac_rate_coefs()
        nu_react = self._nu_1
        nu_prod = self._nu_2
        progress_rate_f, progress_rate_b = kf, kb # Initialize progress rates with reaction rate coefficients
        
        for j, r in enumerate(self._reactions_ls):
            for i, sp in enumerate(self._species_ls):
                progress_rate_f[j] *= self._concs[sp]**nu_react[i,j]
            if r.is_reversible():
                for i, sp in enumerate(self._species_ls):
                    progress_rate_b[j] *= self._concs[sp]**nu_prod[i,j]
            else:
                progress_rate_b[j] = 0

        progress_rate = progress_rate_f - progress_rate_b
                
        return progress_rate
    
    def get_reac_rate(self, species_idx = []):
            
        nu_react = self._nu_1
        nu_prod = self._nu_2
        nu = nu_prod - nu_react
        
        progress_rate = self.get_progress_rate()
            
        if not species_idx:
            return np.dot(nu, p66rogress_rate)
        else:
            return np.dot(nu[species_idx,:], progress_rate)