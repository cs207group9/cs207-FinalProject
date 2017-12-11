[![Build Status](https://travis-ci.org/cs207group9/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207group9/cs207-FinalProject.svg?branch=master)

[![Coverage Status](https://coveralls.io/repos/github/cs207group9/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/cs207group9/cs207-FinalProject?branch=master&service=github)


# CS207 Final Project - Chemical Kinetics Module - Group 9

This is the repository for the CS207 project for chemical kinetics.

Group 9: Camilo Fosco, Baptiste Lemaire, Jiejun Lu, Yiqi Xie

## Problem Solving

This project aims to derive and evalutate the evolutionary equation for a set of M chemical reactions involving N species. The reactions are of the form: 

<p align="center">
  <img width="330" height="60" src="https://github.com/cs207group9/cs207-FinalProject/blob/master/pic/Eq_Rev_1.png">
</p>

where <img width="13" height="15" src="https://github.com/cs207group9/cs207-FinalProject/blob/master/pic/Si.png"> represents the species, <img width="13" height="15" src="https://github.com/cs207group9/cs207-FinalProject/blob/master/pic/nuP.png"> is the stoichiometric coefficient matrix for reactants, and 
<img width="16" height="15" src="https://github.com/cs207group9/cs207-FinalProject/blob/master/pic/nuPP.png"> is the stoichiometric matrix for products. Here we put a double sided arrow in between to indicate that in general we allow the reactions to be reversible. 

To calculate the reaction rates, we use the following formula:
<p align="center">
  <img width="300" height="60" src="https://github.com/cs207group9/cs207-FinalProject/blob/master/pic/Eq_Rev_2.png">
</p>

This is also the equation of evolution. Here <img width="13" height="8" src="https://github.com/cs207group9/cs207-FinalProject/blob/master/pic/omega.png">, the progress rate, is:
<p align="center">
  <img width="430" height="55" src="https://github.com/cs207group9/cs207-FinalProject/blob/master/pic/Eq_Rev_3.png">
</p>

`kf` and `kb` denote for the forward reaction rate coefficient and the backward reaction rate coefficient, respectively. Their ratio should be fixed as the equilibrium constant. For irreversible reactions, the equilibrium constant is theoretically very large so that one can mannually set `kb=0`. The forward coefficient `kf` can be obtained in multiple ways. Implemented forward coefficients are:
- Constant coefficient
- Coefficient for Arrhenius reaction
- Coefficient for modified Arrhenius reaction

The equilibrium constant can be inferred from a set of NASA coefficients. Once we obtained the forward coefficient and the equilibrium constant, we have the backward coefficient, thus the specific equation of evolution.

Note that the relation between reaction rate `f` and concentration `x` turns out to be quite simple. We can derive their jacobian mannually if we want.

For practice, we built several classes to read in the reaction information and calculate the righthand side of the equation of evolution; we implemented some methods to solve the evolution numerically; and we also provided some easy-using interfaces for reaction visuallization.



## Required modules

To run this library, you will need to download and install (if not installed yet) the following modules:

```numpy, xml, sqlite3, copy, more_itertools, scipy, matplotlib, graphviz``` .

You can download and install these modules by using the following commande:

`pip install MODULENAME`.

The `scipy` package needs to have `solve_ivp` method in its `integrate` module. To make sure, one'd better upgrade the package if (s)he already have it:

`pip intall --upgrade scipy`

## Installing and Getting Started

One can download the package by using the following command:

`pip3 install chemkin_CS207_G9`

or

`pip install chemkin_CS207_G9`

One can also download and install the library from GitHub by entering the following commands:

`git clone https://github.com/cs207group9/cs207-FinalProject.git`  
`cd cs207-FinalProject`  
`python setup.py install`  


## Test Coverage

The fastest way to check the coverage of our library is to run the following commands in the terminal:

`git clone https://github.com/cs207group9/cs207-FinalProject.git`  
`cd cs207-FinalProject`  
`python setup.py test`  

As can be seen on the screenshot below, **our test coverage is 94%**.

![Test Coverage](/TestCoverage.png "Test Coverage")

## Basic Usage and Examples

Basic usage of this library starts with importing:
```
from chemkin_CS207_G9.reaction.Reaction import Reaction
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem
from chemkin_CS207_G9.parser.database_query import CoeffQuery
```

To calculate a reaction coefficient of a particular system, first we must create the ReactionSystem object that represents this system. ReactionSystem needs a list of Reaction objects and some related informations. Let's first create those essential ingredients:
```
# Some reactions involving species H2, O2, OH, HO2 and H2O
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
# (this is just an example, you should specify your own path to the file)
nasa_query = CoeffQuery('nasa_thermo_all.sqlite')
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
It is also possible to directly ask the system to evolute:
```
time_evolute = 1e-10
rs.evolute(time_evolute)
```
This calls the ode solvers to update the concentrations. The default solver is `LSODA` implemented in `scipy` library, and there are plenty of other options. The evolution progress can be monitored by applying:
```
rs.get_concs()
```
Furthermore, one may utlize the `chemkin_CS207_G9.plotting` module to get more insights into the reaction systems through quickly generated visualizations. Please refer to later sections for more details.

For most cases it would be much easier to import the reactions from other files instead of typing them in manually. We currently provide one method to allow users import from formatted `.xml` file:
```
from chemkin_CS207_G9.parser.xml2dict import xml2dict

# (this is just an example, you should specify your own path to the file)
species, reactions_info = xml2dict().parse('rxns_reversible.xml')
```
Now `species` is a list of species names, and `reactions_info` is another list of dictionary which can be used to create the `Reaction` objects:
```
reactions = [Reaction(**info) for info in reaction_info]
```

## Example Data
Along with the package there are two additional files of example data - one is `nasa_thermo_all.sqlite`, the database containing all the nasa coefficients, and the other is `rxns_reversible.xml`, the `.xml` file of some reactions and species. Users may access them by:
```
import os
import chemkin_CS207_G9
BASE_DIR = os.path.dirname(os.path.abspath(chemkin_CS207_G9.data.__file__))

path_xml = os.path.join(BASE_DIR, 'rxns_reversible.xml') # path to the .xml file
path_sql = os.path.join(BASE_DIR, 'nasa_thermo_all.sqlite')  # path to the .sqlite file
```
Then `path_xml` and `path_sql` can be fed to the above `xml2dict` object and `CoeffQuery` object directly.


## Organization

Our library is structured as followed:

``` 
chemkin_CS207_G9/
	__init__.py
	auxiliary/
		__init__.py
		check_and_response.py
		mathematical_science.py
		useful_structure.py
	data/
		__init__.py
		nasa_thermo_all.sqlite
		nasa_thermo.sqlite
		rxns_reversible.xml
	parser/
		__init__.py
		database_query.py
		xml2dict.py
	plotting/
		__init__.py
		NonNetworkPlot.py
	reaction/
		__init__.py
		CoeffLaw.py
		Reaction.py
		ReactionSystem.py
						
```

# Authors

* **Camilo Fosco**
[cfosco](https://github.com/cfosco)
* **Baptiste Lemaire**
[bjlemaire](https://github.com/bjlemaire)
* **Jiejun Lu**
[gwungwun](https://github.com/gwungwun)
* **Yiqi Xie**
[yiqixie94](https://github.com/yiqixie94)

See also the list of [contributors](https://github.com/cs207group9/cs207-FinalProject/pulse) who participated in this project.

## License

This project is licensed under the Harvard License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* David Sondak and the CS207 teaching staff.
