import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import ImageClip, concatenate_videoclips
import random 
from graphviz import Digraph
from chemkin_CS207_G9.parser.database_query import CoeffQuery
from chemkin_CS207_G9.parser.xml2dict import xml2dict
from chemkin_CS207_G9.reaction.Reaction import Reaction
from chemkin_CS207_G9.reaction.ReactionSystem import ReactionSystem
import numpy as np
import os


class RSGraph():
    """
    THIS IS A BASE CLASS
    
    RSGraph is basically the parent class of two types of network graph: BipartiteRSGraph and HierarchicalRSGraph, which are to generate a graph to visualize one or multiple reactions.
    The base class RSGraph builds some basic settings of the graph plot.
    
    ATTRIBUTES
    ===========
    rs: ReactionSystem object, pass in the reaction system to be built graph
    top: graphviz Digraph, dot graph to be plotted graph
    default_style: a dictionary with 3 sub-dictionaries of "graph", "node", "edge", default setting of graph
    
    INITIALIZATION
    ===============
    __init__(self, reaction_sys, format="pdf",style=None)
    
    
    INPUTS: 
    ---------------
        reaction_sys: ReactionSystem object, reaction system to build network graph
        format: Optional string, graph format to be expected to show, initilizaed to be "pdf"
        style: Optional, a dictionary with 3 sub-dictionaries of "graph", "node", "edge", initialized to default_style as follows.
    
    METHODS
    =======
    modify_current_style(self, style):
        modify the current style of graph
        Inputs: 
            style: a dictionary with 3 sub-dictionaries of "graph", "node", "edge", initialized to default_style as follows.
    
    reset_default_style(self):
        reset the style (self.current_style) to be default (self.default_style)
    
    plot(self,method='jupyter',path=""):
        Displays current top graph in jupyter or pdf version. If pdf selected, also saves the image. 
        If no path has been specified, the image is saved in the current directory.
        Inputs:
            method: optional string, "jupyter" or "pdf", default to be "jupyter"
            path: optional string, saved path, default to be the current directory.
        
    
    EXAMPLE
    ========
    rs = ReactionSystem(reactions)
    graph = RSGraph(rs)
    graph.plot()   # Displays a graph with customized setting on a jupyter notebook without saving to pdf
    
    """
    
    def __init__(self, reaction_sys, format="pdf",style=None):
        self.rs = reaction_sys
        
        self.default_style = {
        'graph': {
            'fontsize': '16',
            'fontcolor': 'white',
            'bgcolor': '#333333',
            'rankdir': 'LR',
            'pad':'1'
        },
        'nodes': {
            'fontname': 'Helvetica',
            'shape': 'circle',
            'fontcolor': 'white',
            'color': 'white',
            'style': 'filled',
            'fillcolor': 'black',
        },
        'edges': {
            'style': 'dashed',
            'color': 'white',
            'arrowhead': 'open',
            'fontname': 'Courier',
            'fontsize': '12',
            'fontcolor': 'white',
        }
        }
        
        self.color_list = ['#feff6f', '#d2ff6f', '#b5ff6f', '#98ff6f', '#6fff71',
                            '#ff9300','#fb5f02','#b83709','#fbf23d','#ffaf04',
                            '#4285f4', '#ea4335','#fbbc05','#34a853','#ffffff']
        
        
        self.current_style = self.default_style
        self.initialize_top_graph(format)
    
    
    def initialize_top_graph(self, format="pdf", label=''):
        self.top = Digraph(format = format)
        self.apply_style(self.current_style)
        self.top.graph_attr.update(label = label)
    

    def apply_style(self, style):
        """
        Changes the style of the top graph. Input style should be a dictionary with 3 sub-dictionaries:
        one for graph, one for nodes and one for edges.
        """
        self.top.graph_attr.update(('graph' in style and style['graph']) or {})
        self.top.node_attr.update(('nodes' in style and style['nodes']) or {})
        self.top.edge_attr.update(('edges' in style and style['edges']) or {})
        self.bg_color = ('bgcolor' in style['graph'] and style['graph']['bgcolor']) or '#333333'
        self.node_color = ('fillcolor' in style['graph'] and style['graph']['fillcolor']) or '#667766'
    
    def get_random_color(self):
        """
        Generates a random hexadecimal color.
        """
        return '#%02X%02X%02X' % (random.randint(0,255),random.randint(0,255),random.randint(0,255))
         
    def reset_default_style(self):
        self.modify_current_style(self.default_style)
      
    def modify_current_style(self, style):
        self.current_style = style
    
    def plot(self,method = 'jupyter',path="RSGraph", view=True):
        """
        Displays current top graph in jupyter or pdf/png/jpeg version. If jupyter is not selected, also saves the image. 
        If no path has been specified, the image is saved in the current directory.
        """
        if method == 'jupyter':
            return self.top
        else:
            self.top.render(filename=path, view=view)
    

        
class BipartiteRSGraph(RSGraph):
    """
    This class generates a graph to visualize the whole reaction system. 
    It builds nodes for both species and id of equation and seperate them into two parts.
    We construct a bipartite graph with species as nodes (u,1) in one side, and reactions as nodes (u,2) in another side. 
    Build directed edges (u,1) to (v,2) if edge u is the reactant of equation v. 
    Build directed edges (u,2) to (v,1) if edge v is the product of equation u. 
    Set edges to be dashed if the equation is reversible, otherwise filled.
    From this graph, we could recompute the reaction equations.
    The graph assigns a color to each equation (can be defined by the user) and can show concentration of a given specie in the set of reactions by size of the node.
    The reactions can be plotted with different grouping options and style options.
    
    METHODS
    =======
    plot_system(self, method='jupyter', path=""):
        plot the bipartite graph for the whole reaction system with optional parameters method and path passed to plot function.
        Inputs:
            method: optional string, "jupyter" or "pdf", default to be "jupyter"
            path: optional string, saved path, default to be the current directory.

    EXAMPLES
    ========
    rs = ReactionSystem(reactions)
    b_graph = BipartiteRSGraph(rs)
    b_graph.plot_system(method='jupyter') 

    
    """
    
    def plot_system(self, method='jupyter', path="", view =True):
        self.initialize_top_graph()
        
        self.top.graph_attr.update(rankdir='LR')
        
        self.top.graph_attr.update(ranksep='2')
        
        with self.top.subgraph(name='cluster_1') as c:
#             c.attr(label='Reaction', labelloc = 'b')
            c.attr(label='Reaction')
            c.attr(color='white')
            for idx in range(len(self.rs.get_reactions())):
                c.node(str(idx))

        with self.top.subgraph(name='cluster_0') as c:
            c.attr(color='white')
            c.attr(label='Species')
            for s in self.rs.get_species():
                c.node(s)
        
        for idx, r in enumerate(self.rs.get_reactions()):
            c = self.get_random_color()
            if r.is_reversible():
                for k1 in r.getReactants():
                    self.top.edge(k1, str(idx), color = c)
                for k2 in r.getProducts():
                    self.top.edge(str(idx), k2, color = c)
            else:
                for k1 in r.getReactants():
                    self.top.edge(k1, str(idx), color = c, style = "filled")
                for k2 in r.getProducts():
                    self.top.edge(str(idx), k2, color = c, style = "filled")
        
        return self.plot(method=method, path=path,view=view)    
    




class HierarchicalRSGraph(RSGraph):
    """
    This class generates a graph to visualize one or multiple reactions. The graph assigns a color to each equation 
    (can be defined by the user) and can show concentration of a given specie in the set of reactions by size of the node.
    The reactions can be plotted all at once or separately, with different grouping options and style options.
    
    ATTRIBUTES
    ==========
    reac_system: ReactionSystem object to represent.
    target_file: Optional. File path indicating where to save the generated graph.
    
    METHODS
    =======
    build_reaction_graph(self, reaction, prefix = "cluster", color = None):
        Creates a graph for one reaction. If the prefix cluster is sent, the reaction 
        gets plotted in its own cluster, and is a subgraph of the main plot. Color
        sets the color of the edges.
    
    plot_reactions(self, method = 'jupyter', path = "RSGraph", idxs = []):
        Plots all the reactions on the current ReactionSystem on different clusters.
        the varibale idxs can be used to plot certain reactions and not others.
        For example, idxs=[2,3] only plots the reactions with index 2 and 3 in the 
        reaction list of the ReactionSystem.
   
    plot_system(self,method='jupyter',path="RSGraph",colors=None):
        Plots the Reaction system as a whole, without separation between reactions. Shows how each specie interacts 
        In the full reaction system. If the amount of reactions in the system is less than 4, the plot will be generated
        With 2 columns of species, representing on the left the species that are more reactant than product, and on the right
        the species that are more product than reactant. If the system has more than 4 reactions, an automatic organization
        of nodes is performed instead.
        
    set_edges(self, g, reaction, color, node_prefix = ""):
        Generates the edges for a reaction. Edges are dotted for Reactant to Product and filled for product to reactant.

    save_evolution_mp4(self, solver_step_size = 1e-14, timesteps=5, path="HGRSVideo")L:
        Generates and saves and mp4 with the evolution of the system on n timesteps, 
        with an ODE step size defined by the user. 
    
    EXAMPLES
    ========
    rs = ReactionSystem([Reaction(), Reaction()])
    h_graph = HierarchicalRSGraph(rs)
    h_graph.plot_system(method='jupyter')   # Displays on a jupyter notebook without saving to pdf
    
    """
    
    
           
    def build_reaction_graph(self, reaction, prefix = "cluster", color = None):
        """
        Creates a graph for one reaction. If the prefix cluster is sent, the reaction 
        gets plotted in its own cluster, and is a subgraph of the main plot. Color
        sets the color of the edges.
        """
        
        if color == None:
            color =self.get_random_color()
            
        r_graph = Digraph(prefix+'Reaction')
        r_graph.graph_attr.update(label = reaction.get_reaction_equation())
        
        for s in reaction.getReactants().keys():
            r_graph.node(reaction.get_reaction_equation()+' --- '+s, label = s, rank = 'min')
        for s in reaction.getProducts().keys():
            r_graph.node(reaction.get_reaction_equation()+' --- '+s, label = s, rank = 'max')
        
        
        r_graph = self.set_edges(r_graph, reaction, color, node_prefix=reaction.get_reaction_equation()+' --- ')
            
        return r_graph

            
            
    def plot_reactions(self, method = 'jupyter', path = "RSGraph", idxs = [], view=True):
        """
        Plots individual graphs for each reaction in the ReactionSystem. The variable idxs allows the user
        to select specific reactions from the RS system to plot.
        """
        
        if not idxs:
            idxs = list(range(len(self.rs.get_reactions())))
        
        if method != 'jupyter':
            self.initialize_top_graph(format=method)
        else:
            self.initialize_top_graph()
        
            
        r_graph = []
        for i,r in enumerate([self.rs.get_reactions()[i] for i in idxs]):
            r_graph.append( self.build_reaction_graph(r, prefix = 'cluster'+str(i)) )
            self.top.subgraph(r_graph[i])
        
        return self.plot(method = method, path=path,view=view) 

        
    def plot_system(self,method='jupyter',path="RSGraph",colors=None,view=True):
        """
        Plots the Reaction system as a whole, without separation between reactions. Shows how each specie interacts 
        In the full reaction system. If the amount of reactions in the system is less than 4, the plot will be generated
        With 2 columns of species, representing on the left the species that are more reactant than product, and on the right
        the species that are more product than reactant. If the system has more than 4 reactions, an automatic organization
        of nodes is performed instead.
        """
        if method != 'jupyter':
            self.initialize_top_graph(format=method, 
            label='Reaction System Graph\n'+str(len(self.rs.get_reactions()))+' Reactions')
        else:
            self.initialize_top_graph(label='Reaction System Graph\n'+str(len(self.rs.get_reactions()))+' Reactions')
        if colors == None:
            colors = self.color_list        
        self.top.graph_attr.update(rankdir='LR')
        concs = self.rs.get_concs()
        init_concs = self.rs.get_init_concs()
        suffix={}
        concs_dev={}
        for s in self.rs.get_species():
            if concs and init_concs:
                suffix[s]='\n'+"{0:.2f}".format(concs[s])
                concs_dev[s] = 1 / (1 + np.exp(-4*(concs[s]-init_concs[s])))
                if concs_dev[s] < 0.01:
                    concs_dev[s] = 0.01
            else:
                suffix[s]=''
                concs_dev[s] = 0.01
        
        
        if len(self.rs.get_reactions()) <=4:
            self.top.graph_attr.update(ranksep='2')
            reac = Digraph('Reactant graph')
            prod = Digraph('Product graph')
            reac.graph_attr.update(rank = 'source')
            prod.graph_attr.update(rank = 'sink')
            reactant_count = {}
            product_count = {}
            for s in self.rs.get_species():
                reactant_count[s]=0
                product_count[s]=0
                for r in self.rs.get_reactions():
                    if s in r.getReactants().keys():
                        reactant_count[s]+=1
                    if s in r.getProducts().keys():
                        product_count[s]+=1
            for s in self.rs.get_species(): 
                if reactant_count[s] >= product_count[s]:
                    reac.node(s, label = s+suffix[s], style='filled', 
                              fillcolor=self.fillcolor_string(concs_dev[s],self.bg_color, self.node_color),gradientangle='90')
                elif reactant_count[s] < product_count[s]:
                    prod.node(s, label = s+suffix[s], style='filled', 
                              fillcolor=self.fillcolor_string(concs_dev[s],self.bg_color, self.node_color),gradientangle='90')
            self.top.subgraph(reac)
            self.top.subgraph(prod)
        else:
            self.top.graph_attr.update(splines = 'ortho')
            for s in self.rs.get_species():
                self.top.node(s, label = s+suffix[s], style='filled', 
                              fillcolor=self.fillcolor_string(concs_dev[s],self.bg_color, self.node_color),gradientangle='90')
        
        
        for i,reaction in enumerate(self.rs.get_reactions()):
            if colors == None:
                color = self.get_random_color()
            else:
                color = colors[i%len(colors)]
            self.top = self.set_edges(self.top, reaction, color)
    
        return self.plot(method=method, path=path,view=view)
   
    
    def fillcolor_string(self, th, bg_color, node_color):
        return node_color+';'+'{0:.2f}'.format(th)+':'+bg_color
    
    def set_edges(self, g, reaction, color, node_prefix = ""):
        """
        Generates the edges for a reaction. Edges are dotted for Reactant to Product and filled for product to reactant.
        """
        for idx, s1 in enumerate(reaction.getReactants().keys()):
            for s2 in reaction.getProducts().keys():
                if reaction.is_reversible():
                    g.edge(node_prefix+s1, node_prefix+s2, dir='both', color = color, penwidth='2')
                else:
                    g.edge(node_prefix+s1, node_prefix+s2, color = color)
            for jdx, s2 in enumerate(reaction.getReactants().keys()):
                if s1 != s2 and jdx > idx:
                    g.edge(node_prefix+s1, node_prefix+s2, arrowhead = 'none', color = color, style = 'filled',  penwidth='1.5') 
        return g
                    
    
    def save_evolution_movie(self, solver_step_size = 1e-14, timesteps=5, path="HGRSVideo", format = 'gif', colors = None, system=True):
        """
        Generates and saves an mp4 with the evolution of the system on n timesteps, 
        with an ODE step size defined by the user. 
        """
        clip_paths = []        
        for n in range(timesteps):
            self.rs.evolute(solver_step_size)
            if system:
                self.plot_system(method = 'png', path = path + "_img"+str(n), colors=self.color_list,view=False)
            else:
                self.plot_reactions( method = 'png', path = path + "_img"+str(n), view=False)
            clip_paths.append(path + "_img"+str(n)+'.png')
        frames = [ImageClip(img).set_duration(0.1) for img in clip_paths]
        movie = concatenate_videoclips(frames, method="compose")
        if format == 'gif':
            movie.write_gif(path+".gif", fps=30)
        elif format == 'mp4':
            movie.write_videofile(path+".mp4", fps=30)
        else:
            raise ValueError('Wrong format. Formats accepted are gif and mp4.')
        
        
        for n in range(timesteps):
            os.remove( path + "_img"+str(n))
            os.remove( path + "_img"+str(n)+'.png')