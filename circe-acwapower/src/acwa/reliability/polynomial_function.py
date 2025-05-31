"""
acwa.reliability.polynomial_function

Auxiliary builder of polynomial function
"""

from typing import Callable

def build_polynomial_function(degree: int) -> Callable:
    """
    Build a Polynomial function, that receives x as first argument, and the 
    different coefficients from higher to lower degree next

    Args:
        degree (int): Degree of the polynomial

    Raises:
        NotImplementedError: If degree >3

    Returns:
        Callable: Polynomial function
    """

    if degree == 1:
        return linear
    elif degree == 2:
        return poly2
    elif degree == 3:
        return poly3
    else:
        raise NotImplementedError("Only implemented degres 1 to 3")

def linear(x,a,b):
    return a*x + b

def poly2(x,a,b,c):
    return a*x*x + b*x + c

def poly3(x,a,b,c,d):
    return a*x*x*x + b*x*x + c*x + d
