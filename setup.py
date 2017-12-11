from setuptools import setup, find_packages
import sys
from setuptools.command.test import test as TestCommand


setup(name='chemkin_CS207_G9',
      version='2.4',
      description='The vital Chemical Kinetics packages - a life-changing module.',
      url='https://github.com/cs207group9/cs207-FinalProject/tree/master/chemkin_CS207_G9',
      author='Group 9 - CF, YX, JL, BJL',
      author_email='blemaire@g.harvard.edu',
      classifiers=['Programming Language :: Python :: 3 :: Only',],
      setup_requires=['pytest-runner',],
      tests_require=['pytest',],
      python_requires='>=3',
      #cmdclass = {'test': PyTest},
      package_data = {
                 '': ['*.txt', '*.xml','*.md','*.sqlite'],},      
      license='Harvard University',
      packages=find_packages(),
      zip_safe=False,)
