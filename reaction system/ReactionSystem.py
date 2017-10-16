
import numpy as np
import Reaction

class ReactionSystem:
    
    def __init__(self, r_ls, e_ls):
        self._num_reaction = len(r_ls)
        self._num_element = len(e_ls)
        self._r_ls = r_ls
        self._e_ls = e_ls
        
    def set_conditions(self, **kwargs):
        if 'T' in kwargs:
            if (kwargs['T'] <= 0):
                raise ValueError("T = {0:18.16e}: Negative Temperature are prohibited!".format(T))
                
            self._T = kwargs['T']
            
        if 'concs' in kwargs:
            # check validity (concs>=0?)
            self._concs = kwargs['concs']
    
    def get_conditions(self):
        return dict(T=self._T, concs=self._concs)
    
    def rateCoeff(self):
        self._k = np.zeros(self._num_reaction)
        for n, r in enumerate(self._r_ls):
            self._k[n] = r.rateCoeff(T = self._T)
            
        return self._k
    
    def calculate_nu_1(self):
        self._reactants = np.zeros([self._num_element, self._num_reaction])
        for n, r in enumerate(self._r_ls):
            for idx, e in enumerate(self._e_ls):
                self._reactants[idx, n] = r.getReactants()[e] if e in r.getReactants() else 0
        
        return self._reactants
    
    def calculate_nu_2(self):
        self._products = np.zeros([self._num_element, self._num_reaction])
        for n, r in enumerate(self._r_ls):
            for idx, e in enumerate(self._e_ls):
                self._products[idx, n] = r.getProducats()[e] if e in r.getProducats() else 0
                
        return self._products
    
    def get_progress_rate(self):
        self._k = self.rateCoeff()
        nu_react = self.calculate_nu_1()
        self.progress = self._k # Initialize progress rates with reaction rate coefficients
        for jdx, rj in enumerate(self.progress):
            if rj < 0:
                raise ValueError("k = {0:18.16e}:  Negative reaction rate coefficients are prohibited!".format(rj))
            for idx, xi in enumerate(self._concs):
                nu_ij = nu_react[idx,jdx]
                if xi  < 0.0:
                    raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
                if nu_ij < 0:
                    raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ij))

                self.progress[jdx] *= xi**nu_ij
        return self.progress
    
    def get_reac_rate(self):
        self.progress = self.get_progress_rate()
        nu_react = self.calculate_nu_1()
        nu_prod = self.calculate_nu_2()
        nu = nu_prod - nu_react
        self.reac_rate = np.dot(nu, self.progress)
        return self.reac_rate