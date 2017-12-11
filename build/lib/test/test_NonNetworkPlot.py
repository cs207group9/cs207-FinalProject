import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from chemkin_CS207_G9.plotting.NonNetworkPlot import *

from chemkin_CS207_G9.parser.xml2dict import xml2dict
from chemkin_CS207_G9.parser.database_query import CoeffQuery
from chemkin_CS207_G9.reaction.CoeffLaw import BackwardLaw
from chemkin_CS207_G9.reaction.Reaction import Reaction
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem
import numpy as np
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_xml = os.path.join(BASE_DIR, 'rxns_reversible.xml') # path to the .xml file
path_sql = os.path.join(BASE_DIR, 'nasa_thermo.sqlite')  # path to the .sqlite file

reader = xml2dict()
reader.parse(path_xml)
species, r_info = reader.get_info()
nasa_query = CoeffQuery(path_sql)

reactions = [Reaction(**r) for r in r_info]
concentrations = dict(H=2, O=1, OH=0.5, H2=1, H2O=1, O2=1, HO2=0.5, H2O2=1)
temperature = 3000

rs = ReactionSystem(
    reactions, species, nasa_query, 
    initial_concs=concentrations, initial_T=temperature)

_,axes = plt.subplots(3,1)

def test_plot_concentration():
    plot_concentration(rs, np.arange(0,1e-13,1e-15), ax=axes[0])
    assert( rs.get_concs()==concentrations )

def test_plot_reaction_rate():
    plot_reaction_rate(rs, np.arange(0,1e-13,1e-15), ax=axes[1])
    assert( rs.get_concs()==concentrations )

def test_plot_modified_arrhenius():
    plot_modified_arrhenius(np.arange(0.01,2,0.01), np.arange(-2,2,1), ax=axes[2])
    assert( True )