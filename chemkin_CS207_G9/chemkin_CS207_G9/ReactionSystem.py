
import numpy as np

from chemkin_CS207_G9.Reaction import Reaction
from more_itertools import unique_everseen
from chemkin_CS207_G9.CoeffLaw import BackwardLaw

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

    nasa_query: CoeffQuery object, or object of any type with method response(...) implemented.
    nasa_query.response(species_name, temp) should return the nasa coeffs of given species at given temperature
    
    **initial_state: optional parameter indicating the initial state of the reaction.
    Can contain temperature and an array of concentrations.
           
    ATTRIBUTES
    ===========
    
    _reactions_ls: list of class Reaction, reactions included in the system
    
    _species_ls: list of str, concentration element
    
    _T: float, temperature
    
    _concs: array of float, concentration

    _a: ndarray of float, nasa coefficients for all species

    _nu_1: ndarray of float, stoich coeffs for reactants

    _nu_2: ndarray of float, stoich coeffs for products

    _nasa_query: CoeffQuery object, or object of any type with method response(...) implemented.
    an object that connect this reaction system to the database of nasa coeffs.

    
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
    
    compute_nu_1(self):
            return formatted reactant matrix
            OUTPUTS: matrix of float
            
    compute_nu_2(self):
            return formatted product matrix
            OUTPUTS: matrix of float
    
    get_progress_rate(self):
            return the progress rate of a system of irreversible, elementary reactions
            OUTPUTS: numpy array of floats, size: num_reactions, progress rate of each reaction
            
    get_reac_rate(self):
            returns the reaction rate of a system of irreversible, elementary reactions
            OUTPUTS: numpy array of floats, size: num_species, reaction rate of each specie
            
            
    EXAMPLES:
    =========
    # >>> r_ls = []
    # >>> r_ls.append(Reaction(\
    #         reactants=dict(H=1,O2=1), products=dict(OH=1,O=1),\
    #         coeffLaw='Arrhenius', coeffParams=dict(A=2.0)\
    #     ))
    # >>> r_ls.append(Reaction(\
    #         reactants=dict(H2=1,O=1), products=dict(OH=1,H=1),\
    #         coeffLaw='Arrhenius', coeffParams=dict(A=2.0)\
    #     ))
    # >>> concs = {'H':2, 'O2': 1, 'OH':0.5, 'O':1, 'H2':1}
    # >>> species = ['H', 'O2', 'OH', 'O', 'H2']
    # >>> rs = ReactionSystem(r_ls, species_ls= species, initial_concs = concs);
    # >>> rs.get_reac_rate()
    # array([-2., -4.,  6.,  2., -2.])
    """
    
    def __init__(self, reactions_ls, species_ls = [], nasa_query=None, initial_T = 273, initial_concs = {}):
        
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

        self._nasa_query = nasa_query
        self._a = np.zeros( (len(self._species_ls), 7) )
            
        self.set_temp(initial_T)
        if initial_concs:
            self.set_concs(initial_concs)    
        else:
            self._concs = {}

        self._nu_1 = self.compute_nu_1()
        self._nu_2 = self.compute_nu_2()

       
    def set_temp(self, T, update_nasa=True):
        if (T <= 0):
            raise ValueError("T = {0:18.16e}: Negative Temperature is prohibited!".format(T))
         
        self._T = T

        if update_nasa:
            if self._nasa_query is None:
                self._a = np.zeros( (len(self._species_ls), 7) )
            else:
                self._a = [self._nasa_query.response(sp, T).reshape(1, -1) 
                                for sp in self._species_ls]
                self._a = np.concatenate(self._a, axis=0)
        
    def get_temp(self):
        return self._T

    def get_a(self):
        return self._a
    
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
        if self._nasa_query is None:
            kb = np.zeros(len(kf))
        else:
            nu = self._nu_2 - self._nu_1
            ke = BackwardLaw().equilibrium_coeffs(nu, self._a, self._T)
            kb = kf / ke
        return kf, kb
    
    def compute_nu_1(self):
        nu_1 = np.zeros([len(self._species_ls), len(self._reactions_ls)])
        
        for n, r in enumerate(self._reactions_ls):
            reactants = r.getReactants()
            for idx, e in enumerate(self._species_ls):
                nu_1[idx, n] = reactants[e] if e in reactants else 0
                if nu_1[idx, n] < 0:
                    raise ValueError("nu_{0}1 = {1}:  Negative stoichiometric coefficients are prohibited!".format(idx, nu_1[idx, n]))

        self._nu_1 = nu_1
        return nu_1
    
    def compute_nu_2(self):
        nu_2= np.zeros([len(self._species_ls), len(self._reactions_ls)])
        
        for n, r in enumerate(self._reactions_ls):
            products = r.getProducts()
            for idx, e in enumerate(self._species_ls):
                nu_2[idx, n] = products[e] if e in products else 0
                if nu_2[idx, n] < 0:
                    raise ValueError("nu_{0}2 = {1}:  Negative stoichiometric coefficients are prohibited!".format(idx, nu_2[idx, n]))

        self._nu_2 = nu_2
        return nu_2

    def get_nu_1(self):
        return self._nu_1

    def get_nu_2(self):
        return self._nu_2
    
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
            return np.dot(nu, progress_rate)
        else:
            return np.dot(nu[species_idx,:], progress_rate)
     
        