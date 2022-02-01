from black import InvalidInput
from pysat.solvers import Glucose3
from pysat.card import CardEnc

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library.phase_oracle import PhaseOracle
from qiskit.tools.visualization import plot_histogram


class CNF:
    """
    CNF formula. Variables are given as integers, negations as negative integers.

    Variables are assumed to be numbered consecutively starting from 1, i.e. if
    num_vars = 5, then the variables are [1,2,3,4,5].
    """

    # TODO: rename this class to avoid clash with stuff in pysat
    # TODO: map from var number to some label (string)

    def __init__(self):
        self.num_vars = 0
        self.clauses = set()


    def __str__(self):
        fields = {}
        fields['clauses'] = self.clauses.__str__()
        return fields.__str__()


    def copy(self):
        f = CNF()
        f.num_vars = self.num_vars
        f.clauses = self.clauses.copy()
        return f


    def get_vars(self):
        return list(range(1, self.num_vars + 1))


    def get_new_var(self):
        self.num_vars += 1
        return self.num_vars


    def get_new_vars(self, n):
        new_vars = list(range(self.num_vars + 1, self.num_vars + n + 1))
        self.num_vars += (n + 1)
        return new_vars


    def add_var(self, var):
        if (abs(var) > self.num_vars + 1):
            print('Variable {} cannot be added:'.format(var))
            print('Current number of variables is {}'.format(self.num_vars))
            print('New variable must be {}'.format(self.num_vars + 1))
            exit(1)
        if (abs(var) == self.num_vars + 1):
            self.num_vars += 1


    def add_clause(self, clause):
        variables = [abs(lit) for lit in clause]
        variables.sort()
        for var in variables:
            self.add_var(var)
        self.clauses.add(frozenset(clause))


    def add_tseitin_AND(self, a, b, c=None):
        """
        Adds clauses such that c <==> a ^ b. If the variable `c` is not given,
        creates a new variable.

        Returns:
            The variable `c`.
        """
        if (c is None):
            c = self.get_new_var()
        self.add_clause([-a, -b, c])
        self.add_clause([a, -c])
        self.add_clause([b, -c])
        return c


    def add_tseitin_OR(self, a, b, c=None):
        """
        Adds clauses such that c <==> a v b. If the variable `c` is not given,
        creates a new variable.

        Returns:
            The variable `c`.
        """
        if (c is None):
            c = self.get_new_var()
        self.add_clause([a, b, -c])
        self.add_clause([-a, c])
        self.add_clause([-b, c])
        return c


    def add_tseitin_NOT(self, a, b=None):
        """
        Adds clauses such that b <==> ~a. If the variable `b` is not given,
        creates a new variable.

        Returns:
            The variable `c`.
        """
        if (b is None):
            b = self.get_new_var()
        self.add_clause([a, b])
        self.add_clause([-a, -b])
        return b


    def add_tseitin_multi_AND(self, inputs, output=None):
        """
        Adds clauses such that BIG_AND(inputs) <==> output. If the variable
        `output` is not given, creates a new variable.

        Returns:
            The variable `output`.
        """
        if len(inputs) < 1:
            raise InvalidInput("at least one input expected")
        elif len(inputs) == 1:
            if (output is None):
                return inputs[0]
            else:
                raise InvalidInput("please don't add unnecessary identities")
        elif len(inputs) == 2:
            return self.add_tseitin_AND(inputs[0], inputs[1], output)
        else:
            # if more than 2 inputs: do AND of left and right
            l_inputs = inputs[:int(len(inputs)/2)]
            r_inputs = inputs[int(len(inputs)/2):]
            l_output = self.add_tseitin_multi_AND(l_inputs)
            r_output = self.add_tseitin_multi_AND(r_inputs)
            return self.add_tseitin_AND(l_output, r_output, output)


    def add_tseitin_multi_OR(self, inputs, output=None):
        """
        Adds clauses such that BIG_OR(inputs) <==> output. If the variable
        `output` is not given, creates a new variable.

        Returns:
            The variable `output`.
        """
        if len(inputs) < 1:
            raise InvalidInput("at least one input expected")
        elif len(inputs) == 1:
            if (output is None):
                return inputs[0]
            else:
                raise InvalidInput("please don't add unnecessary identities")
        elif (len(inputs) == 2):
            return self.add_tseitin_OR(inputs[0], inputs[1], output)
        else:
            # if more than 2 inputs: do OR of left and right
            l_inputs = inputs[:int(len(inputs)/2)]
            r_inputs = inputs[int(len(inputs)/2):]
            l_output = self.add_tseitin_multi_OR(l_inputs)
            r_output = self.add_tseitin_multi_OR(r_inputs)
            return self.add_tseitin_OR(l_output, r_output, output)


    def add_tseitin_multi(self, gate_type, inputs, output):
        """
        Adds clauses such that GATETYPE(inputs) <==> output. If the variable
        `output` is not given, creates a new variable.

        Returns:
            The variable `output`.
        """
        if gate_type == 'and':
            return self.add_tseitin_multi_AND(inputs, output)
        elif gate_type == 'or':
            return self.add_tseitin_multi_OR(inputs, output)
        else:
            raise InvalidInput("Gate type '{}' currently not supported".format(gate_type))


    def add_cardinality_constraint(self, at_most, variables=None):
        if variables is None:
            variables = self.get_vars()
        card = CardEnc.atmost(variables, bound=at_most, top_id=self.num_vars)
        for clause in card.clauses:
            self.add_clause(clause)
        
    
    def _str_format_lit(self, lit):
        """ Formats a literal as a string """
        if (lit > 0):
            return 'x{}'.format(lit)
        elif (lit < 0):
            return '~x{}'.format(abs(lit))
        else:
            raise InvalidInput("Literal {} is invalid".format(lit))

    
    def str_format_formula(self):
        """ Formats the CNF formula as a string. """
        cnf_str = ''
        for clause in self.clauses:
            cnf_str += '('
            for lit in clause:
                cnf_str += self._str_format_lit(lit) + ' | '
            cnf_str = cnf_str[:-3] # remove last ' | '
            cnf_str += ') & '
        cnf_str = cnf_str[:-3] # remove last ' & '
        return cnf_str
    

    def is_satisfying(self, assignment):
        """ Checks if a given assignment is satisfying. """

        # Every clause must contain at least one literal in the assignment
        for clause in self.clauses:
            sat = False
            for lit in clause:
                if lit in assignment:
                    sat = True
                    break
            if sat == False:
                return False
        return True


    def solve(self, method=None):
        if method == 'grover':
            return self._solve_grover_qiskit()
        else:
            return self._solve_glucose_3()


    def _solve_glucose_3(self):
        g = Glucose3()
        for clause in self.clauses:
            g.add_clause(list(clause))
        return (g.solve(), g.get_model())


    def _process_grover_result(self, result):
        
        # format assignment from bitstring to literals (e.g. 110 -> [1,2,-3])
        assignment = list(range(1, self.num_vars + 1))
        measurement = result.assignment[::-1] # reverse so that q0 is index 0
        for i, bit in enumerate(measurement):
            if (bit == '0'):
                assignment[i] *= -1

        # check if assignment is actually satisfying
        sat = self.is_satisfying(assignment)

        return sat, assignment


    def _solve_grover_qiskit(self, shots=1000):
        """ Find a satisfying assignment using Qiskit's Grover. """

        expression = self.str_format_formula()
        oracle = PhaseOracle(expression) # oracle.data contains circuit info
        problem = AmplificationProblem(oracle, 
                                       is_good_state=oracle.evaluate_bitstring)
        backend = Aer.get_backend('aer_simulator')
        quantum_instance = QuantumInstance(backend, shots=shots)

        # without specifying the number of iterations, the algorithm tries 
        # different number of iteratsion, and after each iteration checks if a 
        # good state has been measured using good_state.
        grover = Grover(quantum_instance=quantum_instance)
        result = grover.amplify(problem)
        
        return self._process_grover_result(result)

