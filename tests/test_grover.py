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

    # assert classical results first
    count = f._count_glucose_3()
    assert count

    # test grover with myqlm backend
    sat, assignment = f.solve(method='grover-myqlm')
    assert sat is True
    assert assignment == [1, -2, 3]
