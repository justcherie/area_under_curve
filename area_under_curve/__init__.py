#!python3
"""Find approximate sum area under curve
Supports simpson, trapezoid, and midpoint algorithms,
n-degree single variable polynomials,
and variable step size
"""
import ast
import collections
import getopt
import sys
import math
import numpy

LOGGING = True # Typically set to false when not using interactively

USAGE = """ -p|--poly {DegreeN1:CoefficientM1, DegreeN2:CoefficientM2, ...}...
-l|--lower <lower_bound> -u|--upper <upper_bound> -s|--step <step> 
-a|--algorithm <simpson | trapezoid | midpoint>

e.g. To evaluate the area of y=x^2 + 2x -2 from [1-50] with .1 width sums and the midpoint algorithm:

python __init__.py --poly "{2:1, 1:2, 0:-2}" --lower 1 --upper 50 --step .1 --algorithm midpoint"""

FULL_USAGE = USAGE

Parameters = collections.namedtuple("Parameters", ["polynomial", "bounds", "algorithm"])

class Bounds:
    """Range of values class"""
    def __init__(self, lower_bound, upper_bound, step_size):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.step_size = step_size
        self.full_range = numpy.arange(lower_bound, upper_bound + step_size, step_size).tolist()

    def __str__(self):
        return "Bounds: [" + str(self.lower_bound) + "-" + str(self.upper_bound) + "] step_size: " +  str(self.step_size)


class Polynomial:
    """Single variable polynomial class supporting n degrees"""
    def __init__(self, coefficient_dict):
        """ The coefficient dict keys are the term orders, and the values are the coefficients
            e.g
            f(x) = 3x^2 would be expressed as {2:3}
            f(x) = 9x^5 + 3 would be {5:9, 0:3}
        """
        self.coefficient_dict = coefficient_dict
    
    def format_term(self, degree, value):
        """string format a single term"""
        value_formatted = str(value)
        if value == 1:
            value_formatted = ""

        if degree == 0:
            return str(value)
        if value == 0:
            return
        else:
            if degree == 1:
                return value_formatted + "x"
            else:
                return value_formatted + "x^" + str(degree)

    def __str__(self):
        """string format the entire polynomial"""
        terms = []
        degrees = list(self.coefficient_dict.keys())
        degrees.sort()
        degrees.reverse()
        for degree in degrees:
            term_formatted = (self.format_term(degree, self.coefficient_dict[degree]))
            if term_formatted:
                terms.append(term_formatted)
        return "f(x)=" + " + ".join(terms)

    def evaluate(self, value):
        """Evaluate the polynomial at a given value"""
        total = 0
        for degree in self.coefficient_dict:
            current_term = math.pow(value, degree)* self.coefficient_dict[degree]
            # print("order: " + str(order) + " coeff " + str(self.coefficient_dict[order]) + " current  " + str(current_term))
            total += current_term
        return total
    


def parse_polynomial_coefficients(dict_literal):
    try:
        return ast.literal_eval(dict_literal)
    except:
        log("Error parsing polynomial args: " + dict_literal)
        return None


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
    lower = 0
    upper = 10
    step_size = 1
    algorithm = "trapezoid"
    polynomial_coefficients = {}

    try:
        opts, args = getopt.getopt(argv, "hl:u:s:a:p:", ["lower=", "upper=", "step=", "algorithm=", "polynomial="])
        numerical_params = list(filter(lambda t: t[0] != '-a' and t[0] != '--algorithm' and t[0] != "-p" and t[0] !="--polynomial", opts))
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
        elif opt in ("-l", "--lower"):
            lower = float(arg)
        elif opt in ("-u", "--upper"):
            upper = float(arg)
        elif opt in ("-s", "--step"):
            step_size = float(arg)
        elif opt in ("-a", "--algorithm"):
            algorithm = arg
        elif opt in ("-p", "--polynomial"):
            polynomial_coefficients = parse_polynomial_coefficients(arg)
        else:
            log("?")

    algorithm_function = get_algorithm(algorithm)
    if not algorithm_function:
        log("Algorithm :" + algorithm + " not found!")
        return
    if not polynomial_coefficients:
        log("Polynomial not specified or invalid")
        return
    return get_parameters(polynomial_coefficients,
                          lower, upper, step_size, algorithm_function)

def get_parameters(polynomial_coefficients, lower, upper, step, algorithm):
    """Create parameters tuple from polynomial, bounds, and algorithm parameters"""
    bounds = Bounds(lower, upper, step)
    polynomial = Polynomial(polynomial_coefficients)
    return Parameters._make([polynomial, bounds, algorithm])

def get_algorithm(algorithm_name):
    """Get algorithm function by name by looking up in globals with the 'algorithm' attribute set"""
    if algorithm_name in globals():
        algorithm = globals()[algorithm_name]
        if "algorithm" in dir(algorithm):
            return globals()[algorithm_name]
    else:
        log("Algorithm " + algorithm_name + " not found or invalid!")

@has_property("algorithm")
def midpoint(poly, lower, upper):
    """Calculate midpoint slice from two polynomial evaluations and step size"""
    value = poly.evaluate((upper+lower)/2)
    return (upper - lower) * value

@has_property("algorithm")
def trapezoid(poly, lower, upper):
    """Calculate trapezoid slice from two polynomial evaluations and step size"""
    lower_value = poly.evaluate(lower)
    upper_value = poly.evaluate(upper)
    return (upper - lower) * ((lower_value + upper_value)/2)

@has_property("algorithm")
def simpson(poly, lower, upper):
    """Calculate parabola (Simpson) slice from two polynomial evaluations and step size"""
    lower_value = poly.evaluate(lower)
    upper_value = poly.evaluate(upper)
    midpoint_value = poly.evaluate((lower+upper)/2)
    return ((upper - lower) / 6) * (lower_value + 4 * midpoint_value + upper_value)

def area_under_curve(poly, bounds, algorithm):
    """Finds the area under a polynomial between the specified bounds
    using a rectangle-sum (of width 1) approximation.
    """
    log(bounds)
    log(poly)
    log("Algorithm: " + algorithm.__name__)
    range_upper_index = len(bounds.full_range) - 1
    total_area = 0
    for range_index, val in enumerate(bounds.full_range):
        # Can't calculate trapezoid with only lower bound value, so we're done summing.
        if range_index == range_upper_index:
            return total_area
        else:
            total_area += algorithm(poly, val, bounds.full_range[range_index + 1])


if __name__ == '__main__':
    FULL_USAGE = __doc__ + "\n\nUsage : python " + sys.argv[0] + USAGE
    PARSED_PARAMETERS = parse_arguments(sys.argv[1:])
    if not PARSED_PARAMETERS:
        log(FULL_USAGE)
        exit(2)
    AREA = area_under_curve(PARSED_PARAMETERS.polynomial,
                            PARSED_PARAMETERS.bounds, PARSED_PARAMETERS.algorithm)
    log("Total Area (" + PARSED_PARAMETERS.algorithm.__name__ + ")= " + str(AREA))
