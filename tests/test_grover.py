"""
Tests solving with Grover.
"""

from ft_2_quantum_sat.cnf import CNF

def test_grover_myqlm():
    """
    Test simple unique-SAT instance
    """

    # unique sat [1, -2, 3]
    f = CNF()
    f.add_clause([ 1,-2, 3])
    f.add_clause([ 1, 2, 3])
    f.add_clause([ 1, 2,-3])
    f.add_clause([-1,-2,-3])
    f.add_clause([-1, 2, 3])
    f.add_clause([ 1,-2,-3])
    f.add_clause([ 1, 2, 3])
    f.add_clause([-1,-2, 3])

    # test grover with myqlm backend
    sat, assignment = f.solve(method='grover')
    assert sat is True
    assert assignment == [1, -2, 3]
