[![Build Status](https://travis-ci.org/cs207group9/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207group9/cs207-FinalProject.svg?branch=master)

[![Coverage Status](https://coveralls.io/repos/github/cs207group9/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/cs207group9/cs207-FinalProject?branch=master)


# CS207 Final Project - Chemical Kinetics Module - Group 9

This is the repository for the CS207 project for chemical kinetics.

Group 9: Camilo Fosco, Baptiste Lemaire, Jiejun Lu, Yiqi Xie

## Getting Started

Download the chemkin.py module. All the classes are there. Download the chemkin_tests.py module for the test suite.

### Installing

One can download the package by using the following command:

pip install chemkin_CS207_G9

However, to be able to enter the command "python setup.py test", it may be preferred to download the entire repo :

https://github.com/cs207group9/cs207-FinalProject/archive/v1.1-alpha.zip

The folder "chemkin_CS207_G9" contains the file setup.py that can be used to run the tes.


### Basic Usage and Examples

To calculate a reaction coefficient of a particular system, first we must create the ReactionSystem object that represents this system. ReactionSystem needs a list of Reaction objects and a concentration value for each specie in the array. Let's first create some Reactions and an array of concentrations:
```
# Reactions involving species A, B and C
reaction1 = Reaction(reactants={'A':1,'B':2}, products = {'C':1}, coeffLaw = 'const', coeffParams = 10)
reaction2 = Reaction(reactants={'A':1,'B':2}, products = {'C':1}, coeffLaw = 'const', coeffParams = 10)
reactions = [reaction1, reaction2]

# One concentration value is needed for each species of our reactions
concentrations = [1,2,1]
```
We can now create our ReactionSystem object:
```
rs = ReactionSystem(reactions, concentrations)
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
