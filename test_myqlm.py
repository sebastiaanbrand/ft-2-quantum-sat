"""
(Just for testing some suff, remove later).
"""
from ft_2_quantum_sat.cnf import CNF

if __name__ == '__main__':
    cnf = CNF()
    cnf.add_clause([1,2,-3])
    cnf.add_clause([-2,4,5])
    cnf.add_clause([4,5,-6])
    cnf.solve(method='grover-myqlm')
