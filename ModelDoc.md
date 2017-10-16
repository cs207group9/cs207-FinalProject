1. Introduction:  Describe what problem the code is solving.  You may borrow the Latex
   expressions from my lecture notes.  Discuss in broad strokes what the purpose of the
   code is along with any features.  Do not describe the details of the code yet.
2. Installation:  Describe where the code can be found and downloaded.  Tell the user
   how to run the test suite.  We are not releasing this code as a package yet, but
   when we do that this section will include instructions how how to install the package.
3. Basic Usage and Examples:  Provide a few examples on using your software in some
   common situations.  You may want to show how the code works with a small set of
   reactions.


# Model Document for the CS207 project

## Introduction
This project aims to calculate reaction coefficients for a set of M chemical reactions involving N species. The reactions are of the form:

$$\begin{align}
\sum_{i=1}^{N}{\nu_{ij}^{\prime}\mathcal{S}_{i}} \longrightarrow
\sum_{i=1}^{N}{\nu_{ij}^{\prime\prime}\mathcal{S}_{i}}, \qquad j = 1, \ldots, M
\end{align}$$

where $S_i$ represents the species, $\nu^\prime$ is the stoichiometric coefficient matrix for reactants, and $\nu^{\prime\prime}$ is the stoichiometric matrix for products. To calculate the reaction coefficients, we use the following equation:
$$\begin{align}
f_{i} = \sum_{j=1}^{M}{\nu_{ij}\omega_{j}}, \qquad i = 1, \ldots, N
\end{align}$$

were $\omega$, the progress rate, is:
$$\begin{align}
\omega_{j} = k_{j}\prod_{i=1}^{N}{x_{i}^{\nu_{ij}^{\prime}}}, \qquad j = 1, \ldots, M
\end{align}$$

And $k_{j}$ is the forward reaction rate coefficient. This coefficient can be obtained in multiple ways. Implemented coefficients are:
- Constant coefficient
- Coefficient for Arrhenius reaction
- Coefficient for modified Arrhenius reaction

## Installation

This module is currently composed of one main file, chemkin.py, that can be downloaded and imported at will. The file is located in the main folder of this repository. Download the file and import it in your project.

To run the test suite, download and run chemkin_tests.py. This file must be located in the same folder as your chemkin.py file.

## Basic Usage and Examples

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
