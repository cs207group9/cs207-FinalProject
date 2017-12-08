[![Build Status](https://travis-ci.org/cs207group9/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207group9/cs207-FinalProject.svg?branch=master)

[![Coverage Status](https://coveralls.io/repos/github/cs207group9/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/cs207group9/cs207-FinalProject?branch=master&service=github)


# CS207 Final Project - Chemical Kinetics Module - Group 9

This is the repository for the CS207 project for chemical kinetics.

Group 9: Camilo Fosco, Baptiste Lemaire, Jiejun Lu, Yiqi Xie

### Installing and Getting Started

One can download the package by using the following command:

`pip install chemkin_CS207_G9`

However, to be able to enter the command `python setup.py test`, it may be preferred to download the entire release:

https://github.com/cs207group9/cs207-FinalProject/archive/v1.8.zip

The root directory contains the file `setup.py` that can be used to run the test command.

### External Dependencies

To run this library, you will need following packages: 
```numpy, xml, sqlite3, copy, more_itertools```

### Test Coverage

As can be seen, **our test coverage is 94%**.

![Test Coverage](/TestCoverage.png "Test Coverage")

### Basic Usage and Examples

Basic usage of this library starts with importing:
```
from chemkin_CS207_G9.chemkin.reaction.Reaction import Reaction
from chemkin_CS207_G9.chemkin.reaction.ReactionSystem import ReactionSystem
from chemkin_CS207_G9.chemkin.parser.database_query import CoeffQuery
```

To calculate a reaction coefficient of a particular system, first we must create the ReactionSystem object that represents this system. ReactionSystem needs a list of Reaction objects and some related informations. Let's first create those essential ingredients:
```
# Reactions involving species A, B and C
reaction1 = Reaction(
    reactants={'H2':2,'O2':1}, products = {'OH':2,'H2':1}, 
    coeffLaw = 'Constant', coeffParams = {'k':10}, 
    reversible='no')
reaction2 = Reaction(
    reactants={'OH':1,'HO2':1}, products = {'H2O':1,'O2':1}, 
    coeffLaw = 'Arrhenius', coeffParams = {'A':5, 'E':-10}, 
    reversible='yes')
reactions = [reaction1, reaction2]

# Species specified in order
species = ['H2', 'O2', 'OH', 'HO2', 'H2O']

# One concentration value is needed for each species of our reactions
concentrations = {'H2':1, 'O2':2, 'OH':2, 'HO2':1, 'H2O':1}

# And the temperature under which they react
temperature = 300

# Database connection object to the nasa coefficients
nasa_query = CoeffQuery('nasa_thermo.sqlite')
```
We can now create our ReactionSystem object:
```
rs = ReactionSystem(
    reactions, species, nasa_query, 
    initial_concs=concentrations, initial_T=temperature)
```
And call the get_reac_rate() function that returns the reaction rate value for each specie.
```
reac_rate = rs.get_reac_rate()
```
It is also possible to obtain the progress rate for each reaction:
```
progress_rate = rs.get_progress_rate()
```
This gives us a 1 dimensional list with one element per reaction.

For most cases one may want to import the reactions from other files instead of typing them in manually. We currently provide one method to allow users import from formatted `.xml` file:
```
from chemkin_CS207_G9.xml2dict import xml2dict

reader = xml2dict()
reader.parse('rxns_reversible.xml')
info = reader.get_info()
```
`info` will be a well-organized python structure, from which you can retrieve the species and the reactions:
```
species = info[0]
reactions = [Reaction(**r) for r in info[1]]
```

### Additional Files
Along with the package there are two additional files - one is `nasa_thermo.sqlite` which is the database containing all the nasa coefficients, and the other is `rxns_reversible.xml` which is the example `.xml` file of reactions and species. Users may access them by:
```
import os
import chemkin_CS207_G9
BASE_DIR = os.path.dirname(os.path.abspath(chemkin_CS207_G9.__file__))

path_xml = os.path.join(BASE_DIR, 'rxns_reversible.xml') # path to the .xml file
path_sql = os.path.join(BASE_DIR, 'nasa_thermo.sqlite')  # path to the .sqlite file
```

## Authors

* **Camilo Fosco**
[cfosco](https://github.com/cfosco)
* **Baptiste Lemaire**
[bjlemaire](https://github.com/bjlemaire)
* **Jiejun Lu**
[gwungwun](https://github.com/gwungwun)
* **Yiqi Xie**
[yiqixie94](https://github.com/yiqixie94)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* David Sondak and the CS207 teaching staff.
