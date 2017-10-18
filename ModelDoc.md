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

```
import chemkin
import chemkin_tests
```

## Basic Usage and Examples

First of all, we need to turn an input file (XML file) into dictionaries and data readable by Python. Therefore we first implemented a class xml2dict.
This class has the method "parse" that takes the input file as an argument, that reads the XML file and store all the data into arrays and dictionaries of strings and number. The class xml2dict has another method, get_info(). This method returns two object: an array of all the species involved in the reaction system, and a list of dictionaries. There is one dictionary for every single reaction written in the system of reactions (XML file). A given dictionary includes all the information about the reaction it refers to, such as the products, the reactants, the law followed by the reaction rate (Arrhenius, Constant, Modified Arrhenius), the value of the coefficients included in this law, and so forth.
   

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

## Extensibility

Our library is basically working on irreversible elementary reaction systems, supporting reation rate coefficient laws including constant, Arrhenius, and modified Arrhenius. Once a user tries to set thing out of this range, a `NotImplementedError` is expected to get raised. However, we have built up some frames for user to extend a little bit on this library. We have formed a base class named `MathModel`, from which a user may derive some more rate coefficient laws as they wish. Once a new law is built, the user can add that law to the Reaction class. The whole process goes like:

```
# Build some self-defined law
class SomeLaw(MathModel):
	# specify the members...
	@staticmethod
	def _kernel(param1, param2, ..., **other_params):
		# do the calculation
		return reaction_rate_coeff

# Update self-defined law into the Reaction class
Reaction._CoeffLawsDict.update('SomeLaw', SomeLaw)
```

Then you can create Reaction instance with `'SomeLaw'`:
```
r = Reaction(
	..., 
	coeffLaw = 'SomeLaw', 
	coeffParams = {
		SomeLaw_param1 : value1, 
		SomeLaw_param2 : value2 
	},
	...
)
```

and then the `ReactionSystem` instance constructed with this reaction `r` would automatically call `SomeLaw` with the specified parameters when computing the reaction rate coefficients.

Here we emphasize that you must at least specify the The `_kernel` method. As seen in the above example, the `_kernel` method is the exact function that mathematically do the computation. You are expected to make this `_kernel` method as efficient as possible - forget about input check, do not use too many fancy keyword arguments, reduce your function calls...In case you really need input check, you can take the following implementation:

```
# Build some self-defined law
class SomeLaw(MathModel):
	# specify the members...
	@staticmethod
	def _kernel(param1, param2, param3, ..., **other_params):
		# do the calculation
		return reaction_rate_coeff
	@staticmethod
	def check_coeffparams(param1, param2,...):
		# some check
		# raise error if needed
		# defaults doing nothing
	def check_stateparams(self, param3,...):
		# some check
		# raise error if needed
		# defaults doing nothing
```


Here `check_coeffparams` defaults to get called when initializing the `SomeLaw` instance. It checks the validity of your model parameters, such as Arrhenius prefactor and ideal gas constant - you need to define them at the begining, specifying a certain reaction, and keep them fixed after that. `check_stateparams` defaults to get called when doing runtime computation - it check the validity of your model inputs, such as concentration, temperature, pressure - you might want to update them frequently when running your program. In the end, there are also some tricks you can play with `MathModel` subclasses to bypass the input check during computation. Check these up in the `MathModel` documentation, and read through `Constant`, `Arrhenius`, and `modArrhenius` for more example.

Besides this `MathModel`, you may want to learn more about the `_CoeffLawDict` attribute of `Reaction` class. `_CoeffLawDict` is a structure we designed by ourselves, it is basically a dictionary with two parts: one part is always fixed and the other part is subjected to all kinds of change. We have applied its fixed part to store the built-in laws for reaction rate coefficients, *i.e.* constant, Arrhenius and modified Arrhenius, with their names as the keys to access them. With the interfaces of `_CoeffLawDict`, users are not able to change these built-in laws. What they can do is adding and manipulating their self-defined laws using `update`, `remove`, `reset` and many other interfaces provided by this `_CoeffLawDict` -  and they basically come from a base class named `PartialLockedDict`. Check the documantation of `PartialLockedDict` and `_CoeffLawDict` for more details.