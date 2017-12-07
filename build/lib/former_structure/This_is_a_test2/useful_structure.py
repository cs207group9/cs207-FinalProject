from copy import deepcopy


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