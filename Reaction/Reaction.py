from BaseClass import PartialLockedDict
from copy import deepcopy
import numpy as np

class Reaction:
    
    class _CoeffLaws(PartialLockedDict):
        
        class _BuiltIn: 
            def const(**kwargs):
                k = kwargs['k'] if 'k' in kwargs else 1.0
                if k <= 0.0:
                    raise ValueError(' '.join([
                        'k = {0:18.16e}:'.format(k), 
                        'Non-positive reaction rate coefficient is prohibited.']))
                return k
            def arr(**kwargs):
                T = kwargs['T']
                R = kwargs['R'] if 'R' in kwargs else 8.314
                A = kwargs['A'] if 'A' in kwargs else 1.0
                E = kwargs['E'] if 'E' in kwargs else 0.0
                if T <= 0.0:
                    raise ValueError(' '.join([
                        'T = {0:18.16e}:'.format(T),
                        'Non-positive temperature is prohibited.']))
                if A <= 0.0:
                    raise ValueError(' '.join([
                        'A = {0:18.16e}:'.format(A),
                        'Non-positive Arrhenius prefactor is prohibited.']))
                if R <= 0.0:
                    raise ValueError(' '.join([
                        'R = {0:18.16e}:'.format(R),
                        'Non-positive ideal gas constant is prohibited.']))
                return A * np.exp(-E / (R * T))
            def modarr(**kwargs):
                T = kwargs['T']
                R = kwargs['R'] if 'R' in kwargs else 8.314
                A = kwargs['A'] if 'A' in kwargs else 1.0
                b = kwargs['b'] if 'b' in kwargs else 0.0
                E = kwargs['E'] if 'E' in kwargs else 0.0
                if T <= 0.0:
                    raise ValueError(' '.join([
                        'T = {0:18.16e}:'.format(T),
                        'Non-positive temperature is prohibited.']))
                if A <= 0.0:
                    raise ValueError(' '.join([
                        'A = {0:18.16e}:'.format(A),
                        'Non-positive Arrhenius prefactor is prohibited.']))
                if R <= 0.0:
                    raise ValueError(' '.join([
                        'R = {0:18.16e}:'.format(R),
                        'Non-positive ideal gas constant is prohibited.']))
                return A * (T ** b) * np.exp(-E / (R * T))
            
        _dict_builtin = {
            'const' :_BuiltIn.const, 
            'arr'   :_BuiltIn.arr, 
            'modarr':_BuiltIn.modarr
        }
        _dict_all = deepcopy(_dict_builtin) 
        @classmethod
        def _error_change_builtin(cls, name):
            raise KeyError(' '.join([
                'LawName = {}'.format(name),
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
            
    
    def __init__(self, **kwargs):
        self._id          = kwargs['id']          if 'id'          in kwargs else ''
        self._reversible  = kwargs['reversible']  if 'reversible'  in kwargs else False
        self._type        = kwargs['type']        if 'type'        in kwargs else 'elementary'
        self._coeffLaw    = kwargs['coeffLaw']    if 'coeffLaw'    in kwargs else 'const'
        self._coeffParams = kwargs['coeffParams'] if 'coeffParams' in kwargs else {}
        self._reactants   = kwargs['reactants']   if 'reactants'   in kwargs else {}
        self._products    = kwargs['products']    if 'products'    in kwargs else {}
        if self._reversible == True:
            raise NotImplementedError(
                'Reversible reaction is not implemented.')
        if self._type != 'elementary':
            raise NotImplementedError(' '.join([
                'Type = {}.'.format(self._type),
                'Non-elementary reaction is not implemented.']))
        if not self._coeffLaw in self._CoeffLaws._dict_all:
            raise NotImplementedError(' '.join([
                'LawName = {}.'.format(self._coeffLaw),
                'Refered reaction rate coefficient law is not implemented.']))
    
    def rateCoeff(self, **otherParams):
        return self._CoeffLaws._dict_all[self._coeffLaw](**self._coeffParams, **otherParams)  
    def getReactants(self):
        return self._reactants  
    def getProducts(self):
        return self._products