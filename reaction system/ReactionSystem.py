
import numpy as np

class ReactionSystem:
<<<<<<< HEAD
    """ReactionSystem formats and calculates information for a system of irreversible, elementary reactions, 
    including progress rate and reaction rate.
    
    INPUTS:
    =======
    r_ls: list of class Reaction, reactions included in the system
    
    e_ls: list of str, concentration element
    
    kwargs: non-positional arguments, dictionary of initial state, 
            including Temperature kwargs['T'] and concentration kwargs['concs']
    
    
    ATTRIBUTES
    ===========
    _num_reaction: integer, number of reactions
    
    _num_element: integer, number of elements
    
    _r_ls: list of class Reaction, reactions included in the system
    
    _e_ls: list of str, concentration element
    
    _T: float, temperature
    
    _concs: array of float, concentration
    
    _k: array of float, coefficient rates for every equation
    
    _reactants: matrix of float, formatted reactant matrix
    
    _products: matrix of float, formatted product matrix
    
    progress: array of float, progress rate
    
    reac_rate: array of float, reaction rate
    
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
    >>> r_ls = []\
        r_ls.append(Reaction.Reaction(\
            reactants=dict(H=1,O2=1), products=dict(OH=1,O=1),\
            coeffLaw='Arrhenius', coeffParams=dict(A=2.0)\
        ))\
        r_ls.append(Reaction.Reaction(\
            reactants=dict(H2=1,O=1), products=dict(OH=1,H=1),\
            coeffLaw='Arrhenius', coeffParams=dict(A=2.0)\
        ))
    >>> d = {}\
        d['T'] = 1\
        d['concs'] = np.array([2, 1, 0.5, 1, 1]).transpose()
    >>> rs = ReactionSystem.ReactionSystem(e_ls=e_ls, r_ls=r_ls, **d)
    >>> rs.compute_all()
    array([-2.,  2.,  6., -2., -4.])
    """
    
    def __init__(self, r_ls, e_ls, **initial_state):
        self._num_reaction = len(r_ls)
        self._num_element = len(e_ls)
        self._r_ls = r_ls
        self._e_ls = e_ls
        self.set_state(**initial_state)
        
    def set_state(self, **kwargs):
        if 'T' in kwargs:
            if (kwargs['T'] <= 0):
                raise ValueError("T = {0:18.16e}: Negative Temperature are prohibited!".format(kwargs['T']))
=======
    '''
    Class ReactionSystem(reaction_ls, species_ls):
    This class represents a set of reactions defined by the user. It stores an array
    of reactions, and an array of species that interact in these reactions.
    The role of ReactionSystem is to store reactions. An object of this class
    can be queried for reaction rates of its species and progress rates of its reactions.
    
    INPUTS
    ======
    reaction_ls: list of Reaction objects.
    species_ls: optional list of strings, with one specie per string. The list of species
    must match the total set of species in the given Reactions. Order is important
    and is maintained throughout the class.
        
    ATTRIBUTES
    ==========
    self._num_reactions = len(reaction_ls)
    self._num_elements = len(species_ls)
    self._reaction_ls = reaction_ls
    self._species_ls = species_ls
    
    METHODS
    =======
    set_conditions
    get_conditions
    get_reaction_rate_coefs
    calculate_nu_1
    calculate_nu_2
    get_progress_rate
    get_reac_rate
    
    
        
    '''
    
    
    def __init__(self, reaction_ls, species_ls = []):
        self._num_reactions = len(reaction_ls)
        self._num_elements = len(species_ls)
        self._reaction_ls = reaction_ls
        self._species_ls = species_ls
        
    def set_conditions(self, **kwargs):
        # C: I believe that this should be changed to clearly indicate what are the possible inputs.
        if 'T' in kwargs:
            if (kwargs['T'] <= 0):
                raise ValueError("T = {0:18.16e}: Negative Temperature are prohibited.".format(T))
>>>>>>> 8682293af8914a5873ba91e4f39f0f2650daecd6
                
            self._T = kwargs['T']
            
        if 'concs' in kwargs:
<<<<<<< HEAD
            for idx, xi in enumerate(kwargs['concs']):
                if xi  < 0.0:
                        raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
            
            if len(kwargs['concs']) != self._num_element:
                raise ValueError("The dimension of concentration and element list are not the same!")
            
            self._concs = kwargs['concs']
    
    def get_state(self):
        return dict(T=self._T, concs=self._concs)
    
    def __len__(self):
        return self._num_reaction
    
    def __repr__(self):
        repr_ls = ""
        for r in self._r_ls:
            repr_ls += repr(r)

        return repr_ls
    
    def rateCoeff(self):
        self._k = np.zeros(self._num_reaction)
        
        for n, r in enumerate(self._r_ls):
=======
            if (len(kwargs['concs']) != len(self.species_ls)):
                raise ValueError('The number of concentrations ({}) is different than the number of species ({})'.format(len(kwargs['concs']), len(self._species_ls))
            for conc in kwargs['concs']:
                if conc < 0:
                    raise ValueError('Negative concentrations are prohibited.')
                
            self._concentration_ls = kwargs['concs']
    
    def get_conditions(self):
        # I think that a dictionary is not necessary in this case.
        return dict(T=self._T, concs=self._concentration_ls)
    
    def get_reaction_rate_coefs(self):
        self._k = np.zeros(self._num_reaction)
        for n, r in enumerate(self._reaction_ls):
>>>>>>> 8682293af8914a5873ba91e4f39f0f2650daecd6
            self._k[n] = r.rateCoeff(T = self._T)
            
        return self._k
    
    def calculate_nu_1(self):
        self._reactants = np.zeros([self._num_element, self._num_reaction])
<<<<<<< HEAD
        
        for n, r in enumerate(self._r_ls):
            for idx, e in enumerate(self._e_ls):
=======
        for n, r in enumerate(self._reaction_ls):
            for idx, e in enumerate(self._species_ls):
>>>>>>> 8682293af8914a5873ba91e4f39f0f2650daecd6
                self._reactants[idx, n] = r.getReactants()[e] if e in r.getReactants() else 0
                if self._reactants[idx, n] < 0:
                    raise ValueError("nu_{0}1 = {1}:  Negative stoichiometric coefficients are prohibited!".format(idx, self._reactants[idx, n]))

        return self._reactants
    
    def calculate_nu_2(self):
        self._products = np.zeros([self._num_element, self._num_reaction])
<<<<<<< HEAD
        
        for n, r in enumerate(self._r_ls):
            for idx, e in enumerate(self._e_ls):
                self._products[idx, n] = r.getProducts()[e] if e in r.getProducts() else 0
                if self._products[idx, n] < 0:
                    raise ValueError("nu_{0}2 = {1}:  Negative stoichiometric coefficients are prohibited!".format(idx, self._products[idx, n]))

=======
        for n, r in enumerate(self._reaction_ls):
            for idx, e in enumerate(self._species_ls):
                self._products[idx, n] = r.getProducats()[e] if e in r.getProducats() else 0
                
>>>>>>> 8682293af8914a5873ba91e4f39f0f2650daecd6
        return self._products
    
    def get_progress_rate(self):
        self._k = self.rateCoeff()
        nu_react = self.calculate_nu_1()
        self.progress = self._k # Initialize progress rates with reaction rate coefficients
        
        for jdx, rj in enumerate(self.progress):
<<<<<<< HEAD
            for idx, xi in enumerate(self._concs):
=======
            if rj < 0:
                raise ValueError("k = {0:18.16e}:  Negative reaction rate coefficients are prohibited!".format(rj))
            for idx, xi in enumerate(self._concentration_ls):
>>>>>>> 8682293af8914a5873ba91e4f39f0f2650daecd6
                nu_ij = nu_react[idx,jdx]
                self.progress[jdx] *= xi**nu_ij
                
        return self.progress
    
    def get_reac_rate(self):
        self.progress = self.get_progress_rate()
        nu_react = self.calculate_nu_1()
        nu_prod = self.calculate_nu_2()
        nu = nu_prod - nu_react
        self.reac_rate = np.dot(nu, self.progress)
        
        return self.reac_rate
    
    def compute_all(self):
        self.rateCoeff()
        self.calculate_nu_1()
        self.calculate_nu_2()
        self.get_progress_rate()
        self.get_reac_rate()
        
        return self.reac_rate