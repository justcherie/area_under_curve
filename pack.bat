del /q dist\*.*
del /q build\*.*
del /q area_under_curve.egg-info\*.*
python setup.py sdist bdist_wheel --universal
