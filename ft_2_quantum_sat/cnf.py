"""
Definition of CNF class to hold some custom CNF functionality (the CNF class in
pysat.formula doesn't quite do everyting we need).
"""

from pysat.solvers import Glucose3
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library.phase_oracle import PhaseOracle


class CNF:
    """
    CNF formula. Variables are given as positive integers. Positive (negative)
    literals are given by the positive (negative) integer corresponding to the
    variable number.

    Variables are assumed to be numbered consecutively starting from 1, i.e. if
    num_vars = 5, then the variables are [1, 2, 3, 4, 5].
    """

    def __init__(self):
        self.num_vars = 0
        self.clauses = set()
        self.var_names = {} # map: var_number -> var_name


    def __str__(self):
        fields = {}
        fields['clauses'] = self.clauses.__str__()
        fields['var_names'] = self.var_names.__str__()
        return fields.__str__()


    def copy(self):
        """
        Return a copy of self.
        """
        f = CNF()
        f.num_vars = self.num_vars
        f.clauses = self.clauses.copy()
        f.var_names = self.var_names.copy()
        return f


    def get_vars(self):
        """
        Get all the variables as a list.
        """
        return list(range(1, self.num_vars + 1))


    def get_new_var(self, name=''):
        """
        Gets a new variable (integer) and sets its name to the given string.

        Args:
            name: Some string to identify the variable

        Returns:
            The new variable.
        """
        self.num_vars += 1
        self.var_names[self.num_vars] = name
        return self.num_vars


    def get_new_vars(self, n):
        """
        Get `n` new variables.

        Args:
            n: The number of new variables

        Returns:
            The new variables as a list.
        """
        new_vars = list(range(self.num_vars + 1, self.num_vars + n + 1))
        self.num_vars += (n + 1)
        return new_vars


    def add_var(self, var):
        """
        Adds the given variable to the the list of variables. Note that if there
        are currently e.g. 5 variables, the only valid input to this function is
        6.

        Args:
            var: The variable number to be added.
        """
        if abs(var) > self.num_vars + 1:
            print(f'Variable {var} cannot be added:')
            print(f'Current number of variables is {self.num_vars}, ', end='')
            print(f'new variable must be {self.num_vars + 1}')
            raise ValueError("Invalid variable number for new variable")
        if abs(var) == self.num_vars + 1:
            self.num_vars += 1


    def add_clause(self, clause):
        """
        Adds the given clause to the formula.

        Args:
            clause: The clause to be added as an iterable of literals.
        """
        variables = [abs(lit) for lit in clause]
        variables.sort()
        for var in variables:
            self.add_var(var)
        self.clauses.add(frozenset(clause))


    def add_tseitin_and(self, a, b, c=-1):
        """
        Adds clauses such that c <==> a ^ b. If the variable `c` is not given,
        creates a new variable.

        Returns:
            The variable `c`.
        """
        if c == -1:
            c = self.get_new_var()
        self.add_clause([-a, -b, c])
        self.add_clause([a, -c])
        self.add_clause([b, -c])
        return c


    def add_tseitin_or(self, a, b, c=-1):
        """
        Adds clauses such that c <==> a v b. If the variable `c` is not given,
        creates a new variable.

        Returns:
            The variable `c`.
        """
        if c == -1:
            c = self.get_new_var()
        self.add_clause([a, b, -c])
        self.add_clause([-a, c])
        self.add_clause([-b, c])
        return c


    def add_tseitin_not(self, a, b=-1):
        """
        Adds clauses such that b <==> ~a. If the variable `b` is not given,
        creates a new variable.

        Returns:
            The variable `c`.
        """
        if b == -1:
            b = self.get_new_var()
        self.add_clause([a, b])
        self.add_clause([-a, -b])
        return b


    def add_tseitin_multi_and(self, inputs, output=-1):
        """
        Adds clauses such that BIG_AND(inputs) <==> output. If the variable
        `output` is not given, creates a new variable.

        Returns:
            The variable `output`.
        """
        if len(inputs) < 1:
            raise ValueError("at least one input expected")
        elif len(inputs) == 1:
            if (output == -1):
                return inputs[0]
            else:
                raise ValueError("please don't add unnecessary identities")
        elif len(inputs) == 2:
            return self.add_tseitin_and(inputs[0], inputs[1], output)
        else:
            # if more than 2 inputs: do AND of left and right
            l_inputs = inputs[:int(len(inputs)/2)]
            r_inputs = inputs[int(len(inputs)/2):]
            l_output = self.add_tseitin_multi_and(l_inputs)
            r_output = self.add_tseitin_multi_and(r_inputs)
            return self.add_tseitin_and(l_output, r_output, output)


    def add_tseitin_multi_or(self, inputs, output=-1):
        """
        Adds clauses such that BIG_OR(inputs) <==> output. If the variable
        `output` is not given, creates a new variable.

        Returns:
            The variable `output`.
        """
        if len(inputs) < 1:
            raise ValueError("at least one input expected")
        elif len(inputs) == 1:
            if (output == -1):
                return inputs[0]
            else:
                raise ValueError("please don't add unnecessary identities")
        elif (len(inputs) == 2):
            return self.add_tseitin_or(inputs[0], inputs[1], output)
        else:
            # if more than 2 inputs: do OR of left and right
            l_inputs = inputs[:int(len(inputs)/2)]
            r_inputs = inputs[int(len(inputs)/2):]
            l_output = self.add_tseitin_multi_or(l_inputs)
            r_output = self.add_tseitin_multi_or(r_inputs)
            return self.add_tseitin_or(l_output, r_output, output)


    def add_tseitin_multi(self, gate_type, inputs, output):
        """
        Adds clauses such that GATETYPE(inputs) <==> output. If the variable
        `output` is not given, creates a new variable.

        Returns:
            The variable `output`.
        """
        if gate_type == 'and':
            return self.add_tseitin_multi_and(inputs, output)
        elif gate_type == 'or':
            return self.add_tseitin_multi_or(inputs, output)
        else:
            raise ValueError(f"Gate type '{gate_type}' currently not supported")


    def add_cardinality_constraint(self, at_most, variables=None):
        """
        Adds a cardinality constraint to the CNF formula. If `variables` is
        given, the contraint is only over the given variables, otherwise it is
        over all variables.
        """
        if variables is None:
            variables = self.get_vars()
        card = CardEnc.atmost(variables, bound=at_most, top_id=self.num_vars)
        for clause in card.clauses:
            self.add_clause(clause)


    def assignment_to_set(self, assignment):
        """
        Takes an assignments and returns a set containing the names of variables
        set to True in the given assignment. E.g., if

            self.var_names = {1 : 'x', : 2 : 'y', 3 : 'z'}

        then the assignment [1, -2, 3] yields the set {'x', 'z'}.
        """
        res = set()
        for lit in assignment:
            if lit > 0:
                res.add(self.var_names[lit])
        return res


    def assignments_to_sets(self, assignments):
        """
        Runs assignment_to_set() on every assignment in assignments.
        """
        res = []
        for assignment in assignments:
            res.append(self.assignment_to_set(assignment))
        return res


    def _str_format_lit(self, lit):
        """
        Formats a literal as a string.
        """
        if (lit > 0):
            return f'x{lit}'
        elif (lit < 0):
            return f'~x{abs(lit)}'
        else:
            raise ValueError(f"Literal {lit} is invalid")


    def str_format_formula(self):
        """
        Formats the CNF formula as a string.
        """
        var_order = {} # keep track of appearance order of vars in the string
        i = 0
        cnf_str = ''
        for clause in self.clauses:
            cnf_str += '('
            for lit in clause:
                cnf_str += self._str_format_lit(lit) + ' | '
                if abs(lit) not in var_order:
                    var_order[abs(lit)] = i
                    i += 1
            cnf_str = cnf_str[:-3] # remove last ' | '
            cnf_str += ') & '
        cnf_str = cnf_str[:-3] # remove last ' & '
        return cnf_str, var_order


    def is_satisfying(self, assignment):
        """
        Checks if a given assignment is satisfying.
        """

        # Every clause must contain at least one literal in the assignment
        for clause in self.clauses:
            sat = False
            for lit in clause:
                if lit in assignment:
                    sat = True
                    break
            if sat is False:
                return False
        return True


    def block(self, a):
        """
        Block the given (partial) assignment.

        Args:
            a: a (partial) assignment given as an iterable of literals.
        """
        block = [-lit for lit in a]
        self.add_clause(block)


    def block_positive_only(self, a):
        """
        For an assignment a, blocks the partial assignment which is the
        positive literals in a.

        Args:
            a: a (partial) assignment given as an iterable of literals.
        """
        block = []
        for lit in a:
            if lit > 0:
                block.append(-lit)
        if len(block) > 0:
            self.add_clause(block)


    def solve(self, method='classical', minimize_vars=None, verbose=True):
        """
        Gets 1 satisfying assignments if it exists.

        Args:
            method: a string in ['grover', 'classical', 'min-sat']
        """
        if method == 'grover':
            return self._solve_grover_qiskit(verbose=verbose)
        elif method == 'classical':
            return self._solve_glucose_3()
        elif method == 'min-sat':
            return self._solve_min_sat(minimize_vars=minimize_vars)
        else:
            raise ValueError(f"Unknown method '{method}'")


    def _to_weighted_formula(self, weight_map):
        """
        Returns a weighted CNF formula, with the hard clauses being the original
        clauses of self, and the soft clauses the being variables variables in
        `weight_map`.
        """
        weighted = WCNF()
        # add every clause as a hard clause
        for clause in self.clauses:
            weighted.append(clause)

        # for every variable in weight_map, add a soft clause
        for var, weight in weight_map.items():
            weighted.append([var], weight=weight)

        return weighted


    def _solve_max_sat(self, weight_map):
        """
        Gets 1 satisfying assignment if it exists, maximizing the sum of weights
        of variables set to true.

        NOTE: RC2 seems to give incorrect results when weight_map contains
        negative weights.

        Args:
            weight_map: dictionary from (a subset of) variables to weights.
        """
        wcnf = self._to_weighted_formula(weight_map)
        rc2 = RC2(wcnf)
        model = rc2.compute()
        if model is not None:
            return True, model
        else:
            return False, model


    def _solve_min_sat(self, minimize_vars=None):
        """
        Gets 1 satisfying assignment if it exists, which minimizes the number of
        variables in `minimize_vars` set to True. If `minimize_vars` is not
        given, minimizes over all variables.

        Args:
            minimize_vars: an iterable of variables (ints).
        """

        # NOTE: Because RC2 seems to have issues with negative weights, instead
        # of (A) maximizing the sum of *negative* weights of *positive*
        # literals, we (B) maximize the sum of *positive* weights of *negative*
        # literals. I.e. we "reward" variables set to False, rather than
        # "punish" variables set to True. This should yield the same result.
        weight_map = {}
        for var in minimize_vars:
            weight_map[-var] = 1
        return self._solve_max_sat(weight_map=weight_map)


    def _solve_glucose_3(self):
        """
        Gets 1 satisfying asignment if it exists, using a classical SAT solver.
        """

        # create initial formula
        g = Glucose3()
        for clause in self.clauses:
            g.add_clause(list(clause))

        sat = g.solve()
        model = g.get_model()
        return sat, model


    def _solve_grover_qiskit(self, shots=100, verbose=True):
        """
        Gets 1 satisfying assignment if it exists, using Qiskit's Grover.
        """

        expression, var_order = self.str_format_formula()
        oracle = PhaseOracle(expression) # oracle.data contains circuit info
        problem = AmplificationProblem(oracle,
                                       is_good_state=oracle.evaluate_bitstring)
        backend = Aer.get_backend('aer_simulator')
        quantum_instance = QuantumInstance(backend, shots=shots)

        if verbose:
            print(f"Grover oracle requires {oracle.num_qubits} qubits")

        # without specifying the number of iterations, the algorithm tries
        # different number of iteratsion, and after each iteration checks if a
        # good state has been measured using good_state.
        grover = Grover(quantum_instance=quantum_instance)
        result = grover.amplify(problem)

        # get the top-1 most frequent result
        assignments = self._process_grover_result(result, var_order, n=1)
        if len(assignments) == 0:
            return False, None
        else:
            return True, assignments[0]


    def _process_grover_result(self, result, var_order, n):
        """
        Helper to get relevant information from the measurement results.
        """

        # sort measurements by frequency
        m = result.circuit_results[0]
        sorted_m = sorted(m.items(), key=lambda x: x[1], reverse=True)

        # enumerate sorted measurements
        res = []
        done = False
        found = 0
        while (not done and found < n):
            # format assignment from bitstring to lits (e.g. 110 -> [1,2,-3])
            measurement, _ = sorted_m[found]
            measurement = measurement[::-1] # reverse so that q0 is index 0

            # NOTE: the qubit numbers from PhaseOracle(expression) correspond
            # to the order in which the variables apprear in `expression`.
            # Because of this, we keep track of the `var_order` in which the
            # variables apprear in `expression` and need to do a bit of juggling
            # while translating the measurement outcome to the assignment
            assignment = []
            for var in range(1, self.num_vars + 1):
                bit = measurement[var_order[var]]
                if bit == '0':
                    assignment.append(-var)
                else:
                    assignment.append(var)

            # check if assignment is actually satisfying
            sat = self.is_satisfying(assignment)
            if sat:
                found += 1
                res.append(assignment)
            else:
                done = True

        return res
