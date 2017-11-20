# Proposed feature - documentation

## Motivation and description of the feature
Our feature is a visualization module that allows the user to observe different species of a certain reaction system in multiple ways. The main feature of the module is a graph visualization of the current reaction system, created with graphviz.
We will also provide functions for reaction rate visualization over time and over a range of temperatures, evolution of arrhenius coefficients, as well as plots of concentrations as a function of time. For that last element, we will implement an ODE solver to compute the concentrations. The plots will have multiple parameters for user customization, such as log scale options, selection of one or multiple species, visualization of several curves on one graph, real time visualization, etc.
As a bonus feature, we will also try to provide an easy to use GUI to visualize the different elements.

## How will the feature fit in our code
The feature will integrate with the Reaction and ReactionSystem class seamlessly, and will allow the user to input and XML file, generate ReactionSystem objects, and compute all the necessary visualizations with those.

## Modules that will be created
1. Module Plotting: will contain the different methods allowing for clean, seaborn powered graphs to be displayed. The curve plots and graphviz graphs will be generated here.
2. Module Math: Will contain the ODE solver and other math helper functions for the project.
3. Module GUI: Will contain the functions for generating the GUI and connecting with the rest of the functions of the project.


## Map out the methods you plan on implementing
```
plot_concentration(ReactionSystem, time_range, temp_range, logscale=False, species = None)
plot_arrhenius(T_range, E_range)
plot_reaction_rate(ReactionSystem, time_range, temp_range)
plot_network(ReactionSystem, species, type)
plot_path(ReactionSystem, element_filter, start = None, end = None)
plot_evolution(ReactionSystem, time_range)
ODE_solver()
boot_GUI()
plot_in_GUI(plot)
```

## How will the user use our feature?
The user will most likely load an xml file with reactions, generate ReactionSystem objects with that information, and then call our plotting functions to visulaize the evolution of the system. If the user prefers a GUI, the GUI will handle the XML loading, and will have a very straightforward button mapping that will generate the graphs and plots with a couple of clicks.

## External dependencies
The external dependencies will probably be limited, but there will be some critical inclusions, such as graphviz, the module for graph plotting and .DOT file creation; matplotlib, for plotting certain graphs, and probably other elements that will be determined as the project is constructed.
```
pip install graphviz
```
The module might also use an external module called more-itertools, a module for improved iterators. To be sure, remember to install it by using:
```
pip install more-itertools
```
Or, if you're using anaconda:
```
conda install -c auto more-itertools
```


## Details of Future Features
For the visualization, there are three main functions for users to visualize the graph network through different perspectives:      `plot_network`, `plot_path` and `plot_evolution`.

- `plot_network(species = “all”, ReactionSystem, type) `: plot the network graph of given species, default to be all.

`Type = “Bipartite”`:
We construct a bipartite graph with species as nodes (u,1) in one side, and reactions as nodes (u,2) in another side.
Build directed edges (u,1) to (v,2) if edge u is the reactant of equation v.
Build directed edges (u,2) to (v,1) if edge v is the product of equation u.
From this graph, we could recompute the reaction equations.

![Alt text](pic/demo1.png?raw=true "Title")
```
Example 1: Reaction System for Birpartite graph
#1: A + B = C
#2: C + D = A
#3: A + D = B
```

`Type = “Hierarchical”`:
We construct a network with species as nodes using graphviz.
Build undirected edges/line (u,v) if u and v are reactants in an equation.
Build directed edges/arrow (u,v) if v is u’s product in an equation.

Addtional option:
- Set size (height/weight) of nodes as concentration rate of species.
- Set weight of edges as progress rate in an equation.
- Color edges if they are from the same equation.

We may encounter imbalanced parameter if we try to set size/weight to the graph. If so, we could provide an option for user to separate major/minor species.

From this graph, we could have a basic understanding of the relationships among reactions.

![Alt text](pic/demo2.png?raw=true "Title")
```
Example 2: Reaction for Hierarchical graph
A + B = C + D
```


- `plot_path(element_filter, start = None, end = None, ReactionSystem)`: plot the path of species containig specific element
We construct a network with species under specific element filter using graphviz.
For elementary reaction:
Build directed edges (u,v) if v is u’s product in an equation.

Additional option:
- Add attribute “+ related_reactant” on edges.
- Set start species / end species for the graph.

![Alt text](pic/demo3.png?raw=true "Title")

For reversible reaction, we may use undirected edge or double arrows.

- `plot_evolution(graph, type, time_range)`: visualize the network graph dynamically
We plot the initial, intermidiate and final state of a graph within time_range to get the change of concentration.
Require ODE solver to calculate concentration (and/or progress rate)
Plot three different graph with same graph structure but different node size (and/or edge weight)
