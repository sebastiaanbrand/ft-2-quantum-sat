import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import xml.etree.ElementTree as ElementTree

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


    def compute_min_cutsets(self, n, method, cnf=None):
        """ Computes the `n` smallest number of cutsets of this fault tree. """

        if cnf is None:
            cnf, _, input_vars = self.to_cnf()
        else:
            input_vars = cnf.get_vars()

        k = 1
        cutsets = []
        for k in range(1, len(input_vars) + 1):
            f_k = cnf.copy()
            f_k.add_cardinality_constraint(at_most=k, variables=input_vars)
            models = f_k.solve_n(n=n, method=method)
            for model in models:
                cutset = model[:len(input_vars)]
                if cutset not in cutsets:
                    cutsets.append(cutset)
                    if len(cutsets) == n:
                        return cutsets
        return cutsets


    def load_from_xml(self, filepath):
        # 1. make sure all fields are empty
        self.__init__()

        # 2. load xml
        xml = ElementTree.parse(filepath)

        # 3. get all basic events
        basic_events = xml.iter('define-basic-event')
        for e in basic_events:
            self._parse_basic_event_xml(e)
        
        # 4. get all gates
        gates = xml.iter('define-gate')
        for g in gates:
            self._parse_gate_xml(g)
        
        # 5. get top event
        self._parse_top_event_xml(xml)


    def _parse_basic_event_xml(self, xml_element):
        # TODO: also parse prob
        self.add_basic_event(xml_element.attrib['name'], prob=0)


    def _parse_gate_xml(self, xml_element):
        """ Gets the relevant info from <define-gate> xml element """

        # gate name
        name = xml_element.attrib['name']

        # gate type (or / and)
        children = xml_element.getchildren()
        assert len(children) == 1
        gate = children[0]
        gate_type = gate.tag

        # gate inputs
        inputs = []
        for i in gate.getchildren():
            inputs.append(i.attrib['name'])

        self.add_gate(name, gate_type, inputs)

    def _parse_top_event_xml(self, xml_element):
        """ Assumes the first gate under <define-fault-tree> is top event """
        ft_defs = list(xml_element.iter('define-fault-tree'))
        assert len(ft_defs) == 1
        event_name = ft_defs[0].getchildren()[0].attrib['name']
        self.set_top_event(event_name)


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
        nx.draw_networkx_labels(self.graph, pos, font_size=6)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
    


    
