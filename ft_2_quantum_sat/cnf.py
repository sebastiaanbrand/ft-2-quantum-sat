from pysat.solvers import Glucose3

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

    def get_new_var(self):
        self.num_vars += 1
        return self.num_vars

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
            The added variable `c`.
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
            The added variable `c`.
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
            The added variable `c`.
        """
        if (b is None):
            b = self.get_new_var()
        self.add_clause([a, b])
        self.add_clause([-a, -b])
        return b
    
    def _solve_glucose_3(self):
        g = Glucose3()
        for clause in self.clauses:
            g.add_clause(list(clause))
        return (g.solve(), g.get_model())
    
    def solve(self, method=None):
        return self._solve_glucose_3()
