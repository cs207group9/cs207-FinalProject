from copy import deepcopy

# ============================================================ #
class PartialLockedDict:
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