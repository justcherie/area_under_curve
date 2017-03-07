#!python3
"""Find approximate sum area under curve
Supports simpson, trapezoid, and midpoint algorithms and variable step size
"""

import collections
import getopt
import sys
import math
import numpy

LOGGING = True # Typically set to false when not using interactively

USAGE = """ -c|--cubic <cubic_coeff> -q|--quadratic <quadratic_coeff>
-i|--linear <linear_coeff> -n|--constant <constant> 
-l|--lower <lower_bound> -u|--upper <upper_bound> -s|--step <step> 
-a|--algorithm <simpson | trapezoid | midpoint>

e.g. To evaluate the area of y=x^2 + 2x -2 from [1-50] with .1 width sums and the midpoint algorithm:

python __init__.py --quadratic 1 --linear 2 --constant -2 --lower 1 --upper 50 --step .1 --algorithm midpoint'"""

FULL_USAGE = USAGE

Bounds = collections.namedtuple("Bounds", ['lower', 'upper', 'step_size', 'range'])
Polynomial = collections.namedtuple("Polynomial", ['cubic', 'quadratic', 'linear', 'constant'])
Parameters = collections.namedtuple("Parameters", ["polynomial", "bounds", "algorithm"])

def log(string):
    """Simple logging"""
    if LOGGING:
        print(string)

def is_number(string):
    """Simple check to see if string is valid number"""
    try:
        float(string)
        return True
    except ValueError:
        log("Error: " + string)
        return False

def has_property(name):
    """Simple function property decorator"""
    def wrap(func):
        """Wrapper function"""
        setattr(func, name, True)
        return func
    return wrap

def parse_arguments(argv):
    """Parse command line arguments and return a parameters
    object with Bounds, Polynomial, and Algorithm
    """
    cubic = 0
    quadratic = 0
    linear = 0
    constant = 0
    lower = 0
    upper = 10
    step_size = 1
    algorithm = "trapezoid"
    try:
        opts, args = getopt.getopt(argv, "hc:q:l:i:n:l:u:s:a:",
                                   ["cubic=", "quadratic=", "linear=", "constant=",
                                    "lower=", "upper=", "step=", "algorithm="])
        numerical_params = list(filter(lambda t: t[0] != '-a' and t[0] != '--algorithm', opts))
        if any(map(lambda n: not is_number(n[1]), numerical_params)):
            log("Error in numerical arguments.")
            return
    except getopt.GetoptError:
        log("Error...")
        return
    for opt, arg in opts:
        if opt == "-h":
            log(FULL_USAGE)
            return
        elif opt in ("-c", "--cubic"):
            cubic = float(arg)
        elif opt in ("-q", "--quadratic"):
            quadratic = float(arg)
        elif opt in ("-i", "--linear"):
            linear = float(arg)
        elif opt in ("-n", "--constant"):
            constant = float(arg)
        elif opt in ("-l", "--lower"):
            lower = float(arg)
        elif opt in ("-u", "--upper"):
            upper = float(arg)
        elif opt in ("-s", "--step"):
            step_size = float(arg)
        elif opt in ("-a", "--algorithm"):
            algorithm = arg
        else:
            log("?")
    if cubic == 0 and quadratic == 0 and linear == 0 and constant == 0:
        log(FULL_USAGE)
        log("")
    algorithm_function = get_algorithm(algorithm)
    if not algorithm_function:
        log("Algorithm :" + algorithm + " not found!")
        return
    return get_parameters(cubic, quadratic, linear, constant,
                          lower, upper, step_size, algorithm_function)

def get_parameters(cubic, quadratic, linear, constant, lower, upper, step, algorithm):
    """Create parameters tuple from polynomial, bounds, and algorithm parameters"""
    bounds = get_bounds(lower, upper, step)
    polynomial = get_polynomial(cubic, quadratic, linear, constant)
    return Parameters._make([polynomial, bounds, algorithm])

def get_polynomial(cubic, quadratic, linear, constant):
    """Parse polynomial from string arguments"""
    new_poly = Polynomial._make([cubic, quadratic, linear, constant])
    return new_poly

def get_bounds(lower, upper, step):
    """Create function boundaries and range from boundary and steps size"""
    full_range = numpy.arange(lower, upper + step, step).tolist()
    new_bounds = Bounds._make([lower, upper, step, full_range])
    return new_bounds

def get_algorithm(algorithm_name):
    """Get algorithm function by name by looking up in globals with the 'algorithm' attribute set"""
    if algorithm_name in globals():
        algorithm = globals()[algorithm_name]
        if "algorithm" in dir(algorithm):
            return globals()[algorithm_name]
    else:
        log("Algorithm " + algorithm_name + " not found or invalid!")

def print_polynomial(poly):
    """Formats polynomial tuple coefficients as an algebraic function"""
    return "f(x) = " + str(poly.cubic) + " x^3 + " + str(poly.quadratic) + " x^2 + " + str(poly.linear) + "x + " +  str(poly.constant)

def print_bounds(bounds):
    """Formats the upper and lower bounds of a function"""
    return "Bounds: [" + str(bounds.lower) + ", " + \
        str(bounds.upper) + "], Step size: " + str(bounds.step_size) + " Slice count : " + str(len(bounds.range) -1)

def evaluate_polynomial(x, poly):
    """Evaluates a polynomial for a given input 'x'"""
    fx_value = (poly.cubic * math.pow(x, 3)) + (poly.quadratic * math.pow(x, 2)) + (poly.linear * x) + poly.constant
    return fx_value

@has_property("algorithm")
def midpoint(poly, lower, upper):
    """Calculate midpoint slice from two polynomial evaluations and step size"""
    value = evaluate_polynomial((upper+lower)/2, poly)
    return (upper - lower) * value

@has_property("algorithm")
def trapezoid(poly, lower, upper):
    """Calculate trapezoid slice from two polynomial evaluations and step size"""
    lower_value = evaluate_polynomial(lower, poly)
    upper_value = evaluate_polynomial(upper, poly)
    return (upper - lower) * ((lower_value + upper_value)/2)

@has_property("algorithm")
def simpson(poly, lower, upper):
    """Calculate parabola (Simpson) slice from two polynomial evaluations and step size"""
    lower_value = evaluate_polynomial(lower, poly)
    upper_value = evaluate_polynomial(upper, poly)
    midpoint_value = evaluate_polynomial((lower+upper)/2, poly)
    return ((upper - lower) / 6) * (lower_value + 4 * midpoint_value + upper_value)

def area_under_curve(poly, bounds, algorithm):
    """Finds the area under a polynomial between the specified bounds
    using a rectangle-sum (of width 1) approximation.
    """
    log(print_bounds(bounds))
    log(print_polynomial(poly))
    log("Algorithm: " + algorithm.__name__)
    range_upper_index = len(bounds.range) - 1
    total_area = 0
    for range_index, val in enumerate(bounds.range):
        # Can't calculate trapezoid with only lower bound value, so we're done summing.
        if range_index == range_upper_index:
            return total_area
        else:
            total_area += algorithm(poly, val, bounds.range[range_index + 1])


if __name__ == '__main__':
    FULL_USAGE = __doc__ + "\n\nUsage : python " + sys.argv[0] + USAGE
    PARSED_PARAMETERS = parse_arguments(sys.argv[1:])
    if not PARSED_PARAMETERS:
        log(FULL_USAGE)
        exit(2)
    AREA = area_under_curve(PARSED_PARAMETERS.polynomial, 
                            PARSED_PARAMETERS.bounds, PARSED_PARAMETERS.algorithm)
    log("Total Area (" + PARSED_PARAMETERS.algorithm.__name__ + ")= " + str(AREA))
