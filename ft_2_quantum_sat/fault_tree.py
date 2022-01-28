import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

class FaultTree:
    """
    Note that a Fault Tree is not really a tree, it is a DAG. This class is
    mostly just a wrapper around NetworkX's DiGraph keeping track of the 
    probabilities of basic events and the types of the gate nodes.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.top_event = None # should be one of the gate names
        self.basic_events = set()
        self.probs = {} # event name -> prob
        self.gates = {} # gate name -> {and, or, ...}
    
    def set_top_event(self, name):
        """ Sets the top event to the node with the given name """
        self.top_event = name

    def add_basic_event(self, name, prob):
        """ Adds a basic event with the given name and probability. """
        self.basic_events.add(name)
        self.graph.add_node(name)
        self.probs[name] = prob
    
    def add_gate(self, name, gate_type, inputs):
        """ 
        Adds a gate node to the fault tree, with type in {'and', 'or', ...}, 
        and given inputs
        """
        self.graph.add_node(name)
        self.gates[name] = gate_type
        for inpt in inputs:
            self.graph.add_edge(name, inpt)
    
    def get_inputs(self, gate_name):
        """ Get the inputs of the given gate """
        return self.graph.successors(gate_name)
    
    def save_as_image(self, output_file):
        """ Saves the fault tree as image to the the given output file """
        # split the nodes into and-gates, or-gates, and basic events
        and_nodes   = []
        or_nodes    = []
        input_nodes = []
        for node in self.graph:
            if node in self.gates.keys():
                if self.gates[node] == 'and':
                    and_nodes.append(node)
                elif self.gates[node] == 'or':
                    or_nodes.append(node)
            else:
                input_nodes.append(node)
        
        # draw the graph
        pos = graphviz_layout(self.graph, prog='dot')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=and_nodes, node_shape='^')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=or_nodes, node_shape='v')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=input_nodes, node_shape='s')
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        plt.savefig(output_file)
    


    
