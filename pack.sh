#! /bin/bash
rm -rf dist\*.*
rm -rf build\*.*
rm -rf area_under_curve.egg-info\*.*
python3 setup.py sdist bdist_wheel --universal
