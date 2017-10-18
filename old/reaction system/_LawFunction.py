import numpy as np

class _LawFunction:
    def compute(self, check=True):
        raise NotImplementedError
    def check_params(self):
        raise NotImplementedError
    def check_conditions(self):
        raise NotImplementedError

class _LawFunction_NPCheck:
    def compute(self, check=True):
        raise NotImplementedError
    def check_params(self):
        raise NotImplementedError
    def check_conditions(self):
        raise NotImplementedError
    @staticmethod
    def check_nonpositive(x, label, name):
        if x <= 0.0:
            raise ValueError(' '.join([
                '{0} = {1:18.16e}:'.format(label, x), 
                'Non-positive {} is prohibited.'.format(name)]))
        
        
class _Constant(_LawFunction_NPCheck):
    def __init__(self, k=1.0, check=True, **kwargs):
        self._k = k
        if check:
            self.check_params()
    def compute(self, check=True):
        if check:
            self.check_conditions()
        return self._k
    def check_params(self):
        self.check_nonpositive(self._k, 'k', 'reaction rate coefficient')
    def check_conditions(self):
        pass
    
class _Arrhenius(_LawFunction_NPCheck):
    def __init__(self, R=8.314, A=1.0, E=0.0, check=True, **kwargs):
        self._R = R
        self._A = A
        self._E = E
        if check:
            self.check_params()
    def compute(self, T, check=True):
        self._T = T
        if check: 
            self.check_conditions()
        return self._A * np.exp(-self._E / (self._R * self._T))
    def check_params(self):
        self.check_nonpositive(self._A, 'A', 'Arrhenius prefactor')
        self.check_nonpositive(self._R, 'R', 'ideal gas constant')
    def check_conditions(self):
        self.check_nonpositive(self._T, 'T', 'temperature')