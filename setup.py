from setuptools import setup

setup(name='area_under_curve',
      version='0.1',
      description='Calculate area under curve',
      url='https://github.com/smycynek/area_under_curve',
      author='Steven Mycynek',
      author_email='sv@stevenvictor.net',
      license='MIT',
      packages=['area_under_curve'],
      install_requires=[
          'numpy',
      ],
      zip_safe=False)