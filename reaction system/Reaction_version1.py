from copy import deepcopy
import numpy as np


class Reaction:
    
    class _CoeffLaws:
        
        class _BuiltIn:
            def const(**kwargs):
                k = kwargs['k'] if 'k' in kwargs else 1.0
                if k <= 0.0:
                    raise ValueError('k = {0:18.16e}:  Non-positive reaction rate coefficient is prohibited.'.format(k))
                return k
            def arr(**kwargs):
                T = kwargs['T']
                R = kwargs['R'] if 'R' in kwargs else 8.314
                A = kwargs['A'] if 'A' in kwargs else 1.0
                E = kwargs['E'] if 'E' in kwargs else 0.0
                if T <= 0.0:
                    raise ValueError("T = {0:18.16e}:  Non-positive Arrhenius prefactor is prohibited.".format(T))
                if A <= 0.0:
                    raise ValueError("A = {0:18.16e}:  Non-positive temperature is prohibited.".format(A))
                if R <= 0.0:
                    raise ValueError("R = {0:18.16e}:  Non-positive ideal gas constant is prohibited.".format(R))
                return A * np.exp(-E / (R * T))
            def modarr(**kwargs):
                T = kwargs['T']
                R = kwargs['R'] if 'R' in kwargs else 8.314
                A = kwargs['A'] if 'A' in kwargs else 1.0
                b = kwargs['b'] if 'b' in kwargs else 0.0
                E = kwargs['E'] if 'E' in kwargs else 0.0
                if T <= 0.0:
                    raise ValueError("T = {0:18.16e}:  Non-positive Arrhenius prefactor is prohibited.".format(T))
                if A <= 0.0:
                    raise ValueError("A = {0:18.16e}:  Non-positive temperature is prohibited.".format(A))
                if R <= 0.0:
                    raise ValueError("R = {0:18.16e}:  Non-positive ideal gas constant is prohibited.".format(R))
                return A * (T ** b) * np.exp(-E / (R * T))
            
        _dict_builtin = {
            'const' :_BuiltIn.const, 
            'arr'   :_BuiltIn.arr, 
            'modarr':_BuiltIn.modarr
        }
        _dict_full = deepcopy(_dict_builtin)
        
        @classmethod
        def get(cls, name):
            return cls._dict_full[name]
        @classmethod
        def update(cls, name, law):
            if name in cls._dict_builtin:
                raise ValueError('LawName = {}. Changing a built-in law is prohibited.'.format(name))
            cls._dict_full[name] = law
        @classmethod
        def remove(cls, name):
            if name in cls._dict_builtin:
                raise ValueError('LawName = {}. Removing a built-in law is prohibited.'.format(name))
            del cls._dict_full[name]
        @classmethod
        def reset(cls):
            cls._dict_full = deepcopy(cls._dict_builtin)
            
    
    
    def __init__(self, **kwargs):
        self._id          = kwargs['id']          if 'id'          in kwargs else ''
        self._reversible  = kwargs['reversible']  if 'reversible'  in kwargs else False
        self._type        = kwargs['type']        if 'type'        in kwargs else 'elementary'
        self._coeffLaw    = kwargs['coeffLaw']    if 'coeffLaw'    in kwargs else 'const'
        self._coeffParams = kwargs['coeffParams'] if 'coeffParams' in kwargs else {}
        self._reactants   = kwargs['reactants']   if 'reactants'   in kwargs else {}
        self._products    = kwargs['products']    if 'products'    in kwargs else {}
        if self._reversible == True:
            raise NotImplementedError('Reversible reaction is not implemented.')
        if self._type != 'elementary':
            raise NotImplementedError('Type = {}. Non-elementary reaction is not implemented.'.format(self._type))
        if not self._coeffLaw in self._CoeffLaws._dict_full:
            raise NotImplementedError('Law = {}. Refered reaction rate coefficient law is not implemented.'.format(self._coeffLaw))
    
    def rateCoeff(self, **otherParams):
        return self._CoeffLaws._dict_full[self._coeffLaw](**self._coeffParams, **otherParams)
    
    def getReactants(self):
        return self._reactants
    
    def getProducats(self):
        return self._products