
import numpy as np

from Reaction import Reaction
from more_itertools import unique_everseen

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
            self.user_defined_order = False
            self.update_species()
        else:
            self.user_defined_order = True
            
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
        repr_ls = "ReactionSystem object with following Reactions:"
        for i,r in enumerate(self._reactions_ls):
            repr_ls += "\nReaction "+str(i)+": "+repr(r)
        return repr_ls
    
    def add_reaction(self, reaction):
        if not isinstance(reaction, Reaction):
            raise ValueError('Input parameter is not instance of Reaction')
            
        self._reactions_ls.append(reaction)
        self.update_species()
        
    def update_species(self):
        species_list = []
        for r in self._reactions_ls:
            species_list+=r.get_species()
        if self.user_defined_order:
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
        #print('nu_react', nu_react)
        #print('nu_prod', nu_prod)
        #print('nu', nu)
        progress_rate = self.get_progress_rate()
            
        if not species_idx:
            return np.dot(nu, progress_rate)
        else:
            return np.dot(nu[species_idx,:], progress_rate)
     
        