
# Class for Hierarchical graph

class BipartiteRSGraph():
        
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
    
        
    def get_random_color(self):
        """
        Generates a random hexadecimal color.
        """
        return '#%02X%02X%02X' % (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
            
    def change_style(self, style):
        """
        Changes the style of the top graph. Input style should be a dictionary with 3 sub-dictionaries:
        one for graph, one for nodes and one for edges.
        """
        self.top.graph_attr.update(('graph' in self.default_style and self.default_style['graph']) or {})
        self.top.node_attr.update(('nodes' in self.default_style and self.default_style['nodes']) or {})
        self.top.edge_attr.update(('edges' in self.default_style and self.default_style['edges']) or {})
        

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
        """
        self.initialize_top_graph()
        
        self.top.graph_attr.update(rankdir='LR')
        
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
        
        self.plot(method=method, path=path)
                    
    def save_mp4(self,imgs, path):
        frames = [ImageClip(img).set_duration(0.1) for img in imgs]
        movie = concatenate_videoclips(frames, method="compose")
        movie.write_videofile(path+".mp4", fps=30)