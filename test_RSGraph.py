
# Testing
import os
import sqlite3
from chemkin_CS207_G9.parser.database_query import CoeffQuery
from chemkin_CS207_G9.parser.xml2dict import xml2dict
from chemkin_CS207_G9.reaction.Reaction import Reaction
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem
import chemkin_CS207_G9.data as data_folder
import numpy as np
from RSGraph import RSGraph, BipartiteRSGraph
import graphviz
from graphviz import Digraph

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(data_folder.__file__))
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
    rs = ReactionSystem(reactions)
    graph = RSGraph(rs)
    graph.plot()

def test_BipartiteGraph():
    rs = ReactionSystem(reactions)
    b_graph = BipartiteRSGraph(rs)
    b_graph.plot_system(method='jupyter')

def test_plot_system_on_notebook():
    h_graph = BipartiteRSGraph(rs1)
    h_graph.plot_system(method = 'jupyter')

def test_plot_system_pdf():
    h_graph = BipartiteRSGraph(rs1)
    h_graph.plot_system(method = 'format')
    
def test_changing_styles():
    h_graph = BipartiteRSGraph(rs1)
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
    
    h_graph.change_style(new_style)
    g = h_graph.plot_system()
    assert(type(g)==Digraph)
    g
