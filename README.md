# area_under_curve
* Version 0.965
* Python 3 module to calculate area under a curve
* Copyright 2017 Steven Mycynek
* Supports simpson, trapezoid, and midpoint algorithms, n-degree single variable polynomials, and variable step size

* https://pypi.python.org/pypi/area-under-curve


`USAGE = """ -p|--poly {DegreeN1:CoefficientM1, DegreeN2:CoefficientM2, ...}...`
`-l|--lower <lower_bound> -u|--upper <upper_bound> -s|--step <step>` 
`-a|--algorithm <simpson | trapezoid | midpoint>`

* This was just a fun experiment I did on a couple airplane rides and might not be suitable for production use.  
* Try a simple function you can integrate by hand easily, like `f(x) = x^3` from `[0-10]`, and compare that to how accurate the midpoint, trapezoid, and simpson approximations are with various steps sizes.

example:

`python area_under_curve.py --polynomial {3:1} --lower 0 --upper 10 --step .1 --algorithm simpson`

or:

`import area_under_curve as auc`

`algorithm = auc.get_algorithm("simpson")`

`bounds = auc.Bounds(0, 10, .1)`

`polynomial = auc.Polynomial({3:1})`

`params = auc.Parameters._make([polynomial, bounds, algorithm])`

`AREA = auc.area_under_curve(params.polynomial, params.bounds, params.algorithm)`

`print(str(AREA))`
