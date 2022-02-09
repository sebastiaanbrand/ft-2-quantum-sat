"""
Definition of FaultTree class to hold all fault tree functionality.
"""

import xml.etree.ElementTree as ElementTree
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from ft_2_quantum_sat.cnf import CNF

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
        self._suported_gates = {'and', 'or'}


    def set_top_event(self, name):
        """
        Sets the top event to the node with the given name.
        """
        self.top_event = name


    def add_basic_event(self, name, prob):
        """
        Adds a basic event with the given name and probability.
        """
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
        """
        Get the inputs of the given gate.
        """
        return self.graph.successors(gate_name)


    def number_of_nodes(self):
        """
        Returns the number of nodes in the fault tree.
        """
        return self.graph.number_of_nodes()


    def to_cnf(self):
        """
        Converts the FT to a CNF expression.
        """
        f = CNF()

        # 1. assign var numbers to all the events (and gates)
        input_vars = {}     # map : var_name -> var_number
        internal_vars = {}  # map : var_name -> var_number
        for node in self.graph.nodes:
            v = f.get_new_var(name=node)
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

        return f, all_vars, input_vars.values()


    def compute_min_cutsets(self, m, method, formula=None):
        """
        Computes the `m` smallest cut sets of this fault tree.

        Args:
            m: The number of cutsets to compute.
            method: String in ['grover', 'classical', 'min-sat']
            formula: (Optional) If set, computes minimal cutsets for the given
              CNF formula, instead of for self (mostly for debugging purposes).

        Returns:
            The cut set as a list of sets of basic event names.
        """

        if formula is None:
            f, _, input_vars = self.to_cnf()
        else:
            f = formula.copy()
            input_vars = formula.get_vars()

        cutsets = []
        for k in range(1, len(input_vars) + 1):
            f_k = f.copy()

            # we don't need a cardinality constraint if we solve with min-sat
            if method != 'min-sat':
                f_k.add_cardinality_constraint(at_most=k, variables=input_vars)

            sat = True
            while len(cutsets) < m:
                sat, model = f_k.solve(method=method, minimize_vars=input_vars)
                if not sat:
                    break
                cutset = model[:len(input_vars)]

                # Block this cutset from current f_k and future f_k.
                # Only block the positive literals (i.e. the actual cutset),
                # this makes sure that only *minimal* cut sets are computed.
                f_k.block_positive_only(cutset)
                f.block_positive_only(cutset)

                # add cutset and return if enough
                cutsets.append(cutset)
                if len(cutsets) == m:
                    return f.assignments_to_sets(cutsets)

        return f.assignments_to_sets(cutsets)


    @classmethod
    def load_from_xml(cls, filepath):
        """
        Loads an FT from a given XML file in the Open-PSA Model Exchange Format.
        """

        # 1. create new FaultTree
        ft = FaultTree()

        # 2. load xml
        xml = ElementTree.parse(filepath)

        # 3. get all basic events
        basic_events = xml.iter('define-basic-event')
        for e in basic_events:
            ft._parse_basic_event_xml(e)

        # 4. get all gates
        gates = xml.iter('define-gate')
        for g in gates:
            ft._parse_gate_xml(g)

        # 5. get top event
        ft._parse_top_event_xml(xml)

        return ft


    def _parse_basic_event_xml(self, xml_element):
        """
        Gets the relevant info from a <define-basic-event> XML element.
        Currently only gets the event name, not the probability.
        """
        self.add_basic_event(xml_element.attrib['name'], prob=0)


    def _parse_gate_xml(self, xml_element):
        """
        Gets the relevant info from <define-gate> xml element.
        """

        # gate name
        name = xml_element.attrib['name']

        # gate type (or / and)
        children = list(xml_element)

        gate = None
        gate_type = ''
        for child in children:
            if child.tag == 'label': # there might be a <label> element
                continue             # just skip these
            else:
                gate = child
                gate_type = gate.tag

        if gate_type not in self._suported_gates:
            raise ValueError(f"Gate type '{gate_type}' currently not supported")

        # gate inputs
        inputs = []
        for i in gate: # (the xml element is enumerable)
            inputs.append(i.attrib['name'])

        self.add_gate(name, gate_type, inputs)

    def _parse_top_event_xml(self, xml_element):
        """
        Sets the top event of the fault tree, assuming the first gate under
        the <define-fault-tree> element is the top event.
        """
        ft_defs = list(xml_element.iter('define-fault-tree'))
        assert len(ft_defs) == 1
        event_name = list(ft_defs[0])[0].attrib['name']
        self.set_top_event(event_name)


    def save_as_image(self, output_file):
        """
        Saves the fault tree as image to the the given output file, using
        graphviz and pydot.
        """

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
        plt.clf()
