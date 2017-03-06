from setuptools import setup

setup(name='area_under_curve',
      version='0.4',
      description='Calculate area under curve',
      url='https://github.com/smycynek/area_under_curve',
      author='Steven Mycynek',
      author_email='sv@stevenvictor.net',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],

      packages=['area_under_curve'],
      install_requires=[
          'numpy',
      ],
      keywords='riemann-sum calculus',
      zip_safe=False)
