
def twice(x:float)->float:
    """
    Precondition:x is a float
    
    this function evaluates 2 * x where x is the argument of the function

    >>> twice(2.0)
    4.0

    >>> twice(3.0)
    6.0
    
    """
    assert isinstance(x,float)
    lp = 2 * x
    
    return lp
