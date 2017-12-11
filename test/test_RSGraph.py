
# Testing
from chemkin_CS207_G9.parser.xml2dict import xml2dict
from chemkin_CS207_G9.parser.database_query import CoeffQuery
from chemkin_CS207_G9.reaction.CoeffLaw import BackwardLaw
from chemkin_CS207_G9.reaction.Reaction import Reaction
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem
import numpy as np
import sys
import os

import numpy as np
from chemkin_CS207_G9.plotting.RSGraph import *
import graphviz
from graphviz import Digraph

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_xml = os.path.join(BASE_DIR, 'rxns_reversible.xml') # path to the .xml file
path_sql = os.path.join(BASE_DIR, 'nasa_thermo.sqlite')  # path to the .sqlite file

# Loading Reactions and Species from xml file
reader = xml2dict()
reader.parse(path_xml)
info = reader.get_info()
species = info[0]
reactions = [Reaction(**r) for r in info[1]]
cq = CoeffQuery(path_sql)
rs1 = ReactionSystem(reactions[:4], nasa_query = cq)
rs2 = ReactionSystem(reactions, species_ls = species, nasa_query = cq)


def test_RSGraph():
    graph = RSGraph(rs2)
    graph.plot()

def test_BipartiteGraph():
    b_graph = BipartiteRSGraph(rs2)
    b_graph.plot_system(method='jupyter')
    
def test_HierarchicalGraph():
    h_graph = HierarchicalRSGraph(rs2)
    h_graph.plot_system(method='jupyter')

def test_plot_system_on_notebook():
    b_graph = BipartiteRSGraph(rs2)
    b_graph.plot_system(method = 'jupyter')

def test_plot_system_pdf():
    h_graph = BipartiteRSGraph(rs2)
    h_graph.plot_system(method = 'pdf')

def test_plot_reactions_notebook():
    h_graph = HierarchicalRSGraph(rs1)
    g=h_graph.plot_reactions(method = 'jupyter')
    assert(type(g) == Digraph)
    return g    
    
def test_wrong_plot_method():
    graph = RSGraph(rs2)
    try:
        graph.plot(method = 'wrong_format')
    except Exception as err:
        assert(type(err) == ValueError)
        
def test_plot_system_more_than_4_reactions():
    h_graph = HierarchicalRSGraph(rs2)
    g= h_graph.plot_system(method = 'jupyter')
    assert(type(g) == Digraph)
    return g

def test_plot_only_2_reactions():
    h_graph = HierarchicalRSGraph(rs1)
    g=h_graph.plot_reactions(method = 'jupyter', idxs = [2,1])
    assert(type(g) == Digraph)
    return g

def test_plot_single_reaction():
    h_graph = HierarchicalRSGraph(rs1)
    g= h_graph.plot_reactions(method = 'jupyter', idxs = [1])
    assert(type(g)==Digraph)
    return g    

def test_plot_reaction_idx_out_of_range():
    h_graph = HierarchicalRSGraph(rs1)
    try:
        h_graph.plot_reactions(method = 'jupyter', idxs = [7])
    except Exception as err:
        assert(type(err)==IndexError)
    
def test_changing_styles():
    b_graph = BipartiteRSGraph(rs1)
    new_style = {
        'graph': {
            'fontsize': '16',
            'fontcolor': 'white',
            'bgcolor': '#333333',
            'rankdir': 'BT',
            'pad':'1'
        },
        'nodes': {
            'fontname': 'Courier',
            'shape': 'circle',
            'fontcolor': 'white',
            'color': 'white',
            'style': 'dashed',
            'fillcolor': 'black',
        },
        'edges': {
            'style': 'bold',
            'color': 'white',
            'arrowhead': 'empty',
            'fontname': 'Courier',
            'fontsize': '12',
            'fontcolor': 'white',
        }
    }
    
    b_graph.modify_current_style(new_style)
    g = b_graph.plot_system()
    assert(type(g)==Digraph)
    g
