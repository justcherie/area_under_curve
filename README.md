# area_under_curve
* Version 0.9
* Python 3 module to calculate area under a curve
* Copyright 2017 Steven Mycynek
* Supports midpoint, trapezoid, and simpson approximations
* https://pypi.python.org/pypi/area-under-curve

* This was just a fun experiment I did on an airplane and probably isn't suitable for production use.  Try a simple function you can integrate by hand easily, like `f(x) = x^3` from `[0-10]`, and compare that to how accurate the midpoint, trapezoid, and simpson approximations are with various steps sizes.

example:

`python area_under_curve\__init__.py --cubic 1 --lower 0 --upper 10 --step .1 --algorithm simpson`


or:

`import area_under_curve as auc`

`algorithm = auc.get_algorithm("simpson")`

`bounds = auc.get_bounds(0, 10, .1)`

`polynomial = auc.get_polynomial(1, 0, 0, 0)`

`params = auc.Parameters._make([polynomial, bounds, algorithm])`

`AREA = auc.area_under_curve(params.polynomial, params.bounds, params.algorithm)`

`print(str(AREA))`
