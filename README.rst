area\_under\_curve
==================

-  Version 0.2
-  Python 3 module to calculate area under a curve
-  Copyright 2017 Steven Mycynek
-  Supports midpoint, trapezoid, and simpson approximations
-  https://pypi.python.org/pypi/area-under-curve

-  This was just a fun experiment I did on an airplane and probably isn't suitable for production
   use. Try a simple function you can integrate by hand easily, like ``f(x) = x^3`` from ``[0-10]``,
   and compare that to how accurate the midpoint, trapezoid, and simpson approximations are with
   various steps sizes.

example:

``python area_under_curve.py --cubic 1 --quadratic 0 --linear 0 --constant -0 --lower 0 --upper 10 --step .1 --algorithm trapezoid``
