from setuptools import setup, find_packages
import sys
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(name='chemkin_CS207_G9',
      version='1.88',
      description='The vital Chemical Kinetics packages - a life-changing module.',
      url='https://github.com/cs207group9/cs207-FinalProject/tree/master/chemkin_CS207_G9',
      author='Group 9 - CF, YX, JL, BJL',
      author_email='blemaire@g.harvard.edu',
      #setup_requires=['pytest-runner'],
      #tests_require=['pytest'],      
      tests_require=['pytest'],
      python_requires='>=3',
      cmdclass = {'test': PyTest},
      package_data = {
                 '': ['*.txt', '*.xml','*.md','*.sqlite'],},      
      license='Harvard University',
      packages=find_packages(),
      zip_safe=False)
