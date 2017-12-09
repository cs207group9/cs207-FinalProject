
# Class for Hierarchical graph

class HierarchicalRSGraph():
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
    
    
    
    EXAMPLES
    ========
    >>> rs = ReactionSystem(reactions)
    >>> h_graph = HierarchicalRSGraph(rs)
    >>> h_graph.view(method='jupyter')   # Displays on a jupyter notebook without saving to pdf
    
    """
    
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
    
    
    def __init__(self,reaction_sys,format="pdf",style=None):
        self.rs = reaction_sys
        self.initialize_top_graph(format,style)
            
    def initialize_top_graph(self, format="pdf", style = None):
        self.top = Digraph(format = format)
        if style == None:
            self.change_style(self.default_style)
        else:
            self.change_style(style)
        
    def build_reaction_graph(self, reaction, prefix = "cluster", color = None):
        """
        Builds a graph for one reaction.
        """
        
        if color == None:
            color = get_random_color()
            
        r_graph = Digraph(prefix+'Reaction')
        r_graph.graph_attr.update(label = reaction.get_reaction_equation())
        
        for s in reaction.get_species():
            r_graph.node(s)
            
        self.set_edges(reaction, color)
            
        return r_graph
    
        
    def get_random_color(self):
        """
        Generates a random hexadecimal color.
        """
        return '#%02X%02X%02X' % (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
        
    def plot_reactions(self, method = 'jupyter', path = "", idxs = []):
        """
        Plots individual graphs for each reaction in the ReactionSystem.
        """
        
        if not idxs:
            idxs = range(len(self.rs.get_reactions()))
        for i,r in enumerate(self.rs.get_reactions()):
            if i in idxs:
                r_graph = build_reaction_graph(r,prefix = 'cluster')
                self.top.subgraph(r_graph)
                r_graph.graph_attr.update(rank='same')
        
        self.plot(method = method, path=path)
        
            
    def change_style(self, style):
        """
        Changes the style of the top graph. Input style should be a dictionary with 3 sub-dictionaries:
        one for graph, one for nodes and one for edges.
        """
        top.graph_attr.update(('graph' in styles and styles['graph']) or {})
        top.node_attr.update(('nodes' in styles and styles['nodes']) or {})
        top.edge_attr.update(('edges' in styles and styles['edges']) or {})
        

    def plot(self,method='format',path=""):
        """
        Displays current top graph in jupyter or pdf version. If pdf selected, also saves the image. 
        If no path has been specified, the image is saved in the current directory.
        """
        if method == 'jupyter':
            self.top
        elif method == 'format':
            self.top.view()
        else:
            raise ValueError('Unknown method. Valid methods are "jupyter" or "pdf".')
            
    
    def plot_system(self,method='jupyter',path=""):
        """
        Plots the Reaction system as a whole, without separation between reactions. Shows how each specie interacts 
        In the full reaction system. If the amount of reactions in the system is less than 4, the plot will be generated
        With 2 columns of species, representing on the left the species that are more reactant than product, and on the right
        the species that are more product than reactant. If the system has more than 4 reactions, an automatic organization
        of nodes is performed instead.
        """
        self.initialize_top_graph()
        
        self.top.graph_attr.update(rankdir='LR')
        
        if len(self.rs.get_reactions()) <=4:
            self.top.graph_attr.update(ranksep='2')
            reac = Digraph('Reactant graph')
            prod = Digraph('Product graph')
            reactant_count = {}
            product_count = {}
            for s in self.rs.get_species():
                for r in self.rs.get_reactions():
                    if s in r.getReactants().keys():
                        reactant_count[s]+=1
                    if s in r.getProducts().keys():
                        product_count[s]+=1
            for s in self.rs.get_species():
                if reactant_count[s] == 0:
                    reac.node(s)
                elif product_count[s] == 0:
                    prod.node(s)
                elif reactant_count[s] >= product_count[s]:
                    reac.node(s)
                elif reactant_count[s] < product_count[s]:
                    prod.node(s)
            reac.node_attr.update(rank = 'same')
            prod.node_attr.update(rank = 'same')
            top.subgraph(reac)
            top.subgraph(prod)
            
        else:
            for s in self.rs.get_species():
                self.top.node(s)
        
        for reaction in self.rs.get_reactions():
            color = get_random_color()
            self.set_edges(reaction, color)
    
        self.plot(method=method, path=path)
        
        
    def save_evolution_mp4(self,system,reactions,timesteps=5, path = ""):
        
        for n in range(timesteps):
            self.rs.concentration_step()
            imgs.append(self.plot_system())
        
        self.save_gif(imgs)
    
    def set_edges(self, reaction, color):
        for idx, r1 in enumerate(reaction.getReactants().keys()):
            for r2 in reaction.getProducts().keys():
                if reaction.is_reversible():
                    r_graph.edge(r1, r2, arrowhead = 'none', color = color)
                else:
                    r_graph.edge(r1, r2, color = color)
            for jdx, r2 in enumerate(reaction.getReactants().keys()):
                if r1 != r2 and jdx > idx:
                    top.edge(k1, k2, arrowhead = 'none', color = color, style = 'filled') 
                    
    def save_mp4(self,imgs, path):
        frames = [ImageClip(img).set_duration(0.1) for img in imgs]
        movie = concatenate_videoclips(frames, method="compose")
        movie.write_videofile(path+".mp4", fps=30)

    