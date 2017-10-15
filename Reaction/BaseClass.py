from copy import deepcopy

# ============================================================ #
class PartialLockedDict:
    """PartialLockedDict consists one built-in dict and one outer dict.
    The built-in dict is considered constant and user are not suggested to change it.
    The outer dict is defined by the user and is sujected to all kinds of changes.
    
    Methods
    ===========
    _error_change_builtin(cls, key):
        Throws KeyError based on the input key.
        Call this function when built-in dict is going to get changed.
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