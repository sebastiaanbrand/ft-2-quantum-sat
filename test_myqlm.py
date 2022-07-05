"""
(Just for testing some suff, remove later).
"""
from ft_2_quantum_sat.cnf import CNF

if __name__ == '__main__':
    cnf = CNF()

    # unique sat [1, 2, 3]
    """
    cnf.add_clause([ 1, 2, 3])
    cnf.add_clause([ 1,-2, 3])
    cnf.add_clause([ 1,-2,-3])
    cnf.add_clause([-1, 2,-3])
    cnf.add_clause([-1,-2, 3])
    cnf.add_clause([ 1, 2,-3])
    cnf.add_clause([ 1,-2, 3])
    cnf.add_clause([-1, 2, 3])
    """

    # unique sat [1, 2, -3]
    cnf.add_clause([ 1, 2,-3])
    cnf.add_clause([ 1,-2,-3])
    cnf.add_clause([ 1,-2, 3])
    cnf.add_clause([-1, 2, 3])
    cnf.add_clause([-1,-2,-3])
    cnf.add_clause([ 1, 2, 3])
    cnf.add_clause([ 1,-2,-3])
    cnf.add_clause([-1, 2,-3])

    count = cnf._count_glucose_3()
    _, model = cnf.solve(method='classical')
    print("model count: ", count)
    print(model)

    sat, model = cnf.solve(method='grover-myqlm')
    print(sat)
    print(model)
