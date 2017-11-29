class ValueCheck:
    """
    ValueCheck provides formatted response to invalid values.
    
    
    ATTRIBUTES
    ===========
    
    _criterion:  function-like, criterion to decide the validity of some value.
        ------------------------------
        should get called as self._criterion(x):
        INPUTS:  x, numeric type, to-be-judged value
        OUTPUTS: j, boolean, judgement
        
    _name: name of the criterion. will be used in the response(...) method.
    
    
    METHOD
    =======
    
    response(self, x, label, term): response to some value if it passes self._criterion
        INPUTS: x, numeric type, to-be-judged value
                label, str, the math symbel of x
                term, str, the terminology of x
        NOTE:   get reponse when self._criterion(x) == True
                the response will be a ValueError with message formatted:
                [MESSAGE] - (label of x) = (x): (criterion name) (term of x) is prohibited
    
    
    INITIALIZATION
    ===============
    __init__(self, criterion, name)
    
    INPUTS: 
    -----------
        criterion: function-like, initializes _criterion
        name:      str, initializes _name
    
    
    EXAMPLE
    ========
    
    >>> try:
    ...     ValueCheck(lambda x:x>0, 'positive').response(1, 'x', 'integer')
    ... except ValueError as err:
    ...     print(err)
    x = 1.0000000000000000e+00: positive integer is prohibited.
    
    """
    
    def __init__(self, criterion, name):
        # criteron should be a function type
        # criteron(x) returns boolean value
        self._criterion = criterion
        self._name = name
        
    def response(self, x, label, term):
        if self._criterion(x):
            raise ValueError(
                '{} = {:18.16e}: {} {} is prohibited.' \
                .format(label, x, self._name, term))