
import random
import graphviz 
from graphviz import Digraph

class RSGraph():
    """
    THIS IS A BASE CLASS
    
    RSGraph is basically the parent class of two types of network graph: BipartiteRSGraph and HierarchicalRSGraph,
    which are to generate a graph to visualize one or multiple reactions.
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
        format: string, graph format to be expected to show, initilizaed to be "pdf"
        style: a dictionary with 3 sub-dictionaries of "graph", "node", "edge",
                initialized to default_style as follows.
                
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
                'rankdir': 'BT',
                'pad':'1'
            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'octagon',
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
        
        self.initialize_top_graph(format,style)
    
    
    def initialize_top_graph(self, format="pdf", style = None):
        self.top = Digraph(format = format)
        if style == None:
            self.change_style(self.default_style)
        else:
            self.change_style(style)
            
    
    def build_reaction_graph(self, reaction, prefix = "cluster", color = None):
        raise NotImplementedError
        
        
    def change_style(self, style):
        """
        Changes the style of the top graph. Input style should be a dictionary with 3 sub-dictionaries:
        one for graph, one for nodes and one for edges.
        """
        self.top.graph_attr.update(('graph' in self.default_style and self.default_style['graph']) or {})
        self.top.node_attr.update(('nodes' in self.default_style and self.default_style['nodes']) or {})
        self.top.edge_attr.update(('edges' in self.default_style and self.default_style['edges']) or {})
       
    
    def get_random_color(self):
        """
        Generates a random hexadecimal color.
        """
        return '#%02X%02X%02X' % (random.randint(0,255),random.randint(0,255),random.randint(0,255))
         

    def plot(self,method='jupyter',path=""):
        """
        Displays current top graph in jupyter or pdf version. If pdf selected, also saves the image. 
        If no path has been specified, the image is saved in the current directory.
        """
        if method == 'jupyter':
            return self.top
        
        elif method == 'format':
            self.top.view()
        
        else:
            raise ValueError('Unknown method. Valid methods are "jupyter" or "pdf".')
    
    
    def plot_reactions(self, method = 'jupyter', path = "", idxs = []):
        """
        Plots individual graphs for each reaction in the ReactionSystem.
        """
        raise NotImplementedError
        
    def plot_system(self,method='format',path=""):
        """
        Plots the Reaction system as a whole, without separation between reactions. Shows how each specie interacts 
        """
        raise NotImplementedError
        
    def save_evolution_mp4(self,system,reactions,timesteps=5, path = ""):
        raise NotImplementedError
        
    def set_edges(self, reaction, color):
        raise NotImplementedError
        
    def save_mp4(self,imgs, path):
        raise NotImplementedError

        
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
        plot the bipartite graph for the whole reaction system

    
    EXAMPLES
    ========
    rs = ReactionSystem(reactions)
    b_graph = BipartiteRSGraph(rs)
    b_graph.plot_system(method='jupyter')   # Displays on a jupyter notebook without saving to pdf

    
    """
    
    def plot_system(self, method='jupyter', path=""):
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
        
        return self.plot(method=method, path=path)      