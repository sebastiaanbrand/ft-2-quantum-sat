import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

from ft_2_quantum_sat import cnf

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
        self.node_types = {} # gate name -> {input, and, or, ...}


    def set_top_event(self, name):
        """ Sets the top event to the node with the given name """
        self.top_event = name


    def add_basic_event(self, name, prob):
        """ Adds a basic event with the given name and probability. """
        self.graph.add_node(name)
        self.basic_events.add(name)
        self.node_types[name] = 'input'
        self.probs[name] = prob


    def add_gate(self, name, gate_type, inputs):
        """ 
        Adds a gate node to the fault tree, with type in {'and', 'or', ...}, 
        and given inputs
        """
        self.graph.add_node(name)
        self.node_types[name] = gate_type
        for _input in inputs:
            self.graph.add_edge(name, _input)


    def get_gate_inputs(self, gate_name):
        """ Get the inputs of the given gate """
        return self.graph.successors(gate_name)


    def to_cnf(self):
        """ Converts the FT to a CNF expression """
        f = cnf.CNF()

        # 1. assign var numbers to all the events (and gates)
        input_vars = {}
        internal_vars = {}
        for node in self.graph.nodes:
            v = f.get_new_var()
            if self.node_types[node] == 'input':
                input_vars[node] = v
            else:
                internal_vars[node] = v
        all_vars = input_vars.copy()
        all_vars.update(internal_vars)
        
        # 2. for every non-input node, add tseitin constraints to f
        for gate_name, output_var in internal_vars.items():
            input_names = self.get_gate_inputs(gate_name)
            gate_input_vars = []
            for input_name in input_names:
                gate_input_vars.append(all_vars[input_name])
            gate_type = self.node_types[gate_name]
            f.add_tseitin_multi(gate_type, gate_input_vars, output_var)

        # 3. add clause containing only the top event as (positive) literal
        f.add_clause([all_vars[self.top_event]])

        return f, all_vars, input_vars


    def save_as_image(self, output_file):
        """ Saves the fault tree as image to the the given output file """
        # split the nodes into and-gates, or-gates, and basic events
        and_nodes   = []
        or_nodes    = []
        input_nodes = []
        for node in self.graph:
            if self.node_types[node] == 'input':
                input_nodes.append(node)
            if self.node_types[node] == 'and':
                and_nodes.append(node)
            elif self.node_types[node] == 'or':
                or_nodes.append(node)
        
        # draw the graph
        pos = graphviz_layout(self.graph, prog='dot')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=and_nodes, node_shape='^')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=or_nodes, node_shape='v')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=input_nodes, node_shape='s')
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        plt.savefig(output_file)
    


    
