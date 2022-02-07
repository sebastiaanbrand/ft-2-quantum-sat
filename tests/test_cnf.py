"""
Tests for the cnf module.
"""

from ft_2_quantum_sat.cnf import CNF

def test_new_vars():
    """
    Testing getting new vars for CNF formula.
    """
    f = CNF()
    assert f.num_vars == 0

    # variables should be added consecutively starting from 1
    f.add_var(1)
    f.add_var(2)
    assert f.num_vars == 2

    # the new variable should only be allowed to be 3
    failed_to_add = False
    try:
        f.add_var(6)
    except ValueError:
        failed_to_add = True
    assert failed_to_add

    # currently have 2 vars, next var should be 3
    v3 = f.get_new_var()
    assert v3 == 3

    # currently have 3 vars, the next 5 vars should be [3+1, ..., 3+5]
    vs = f.get_new_vars(5)
    assert vs == [4, 5, 6, 7, 8]


def test_solve():
    """
    Testing solve() function.
    """
    f = CNF()
    f.add_clause([1, 2])
    f.add_clause([-2])
    f.add_clause([3, 2, -1])
    sat, assignment = f.solve()
    assert sat is True
    assert assignment == [1, -2, 3]


    f = CNF()
    f.add_clause([1, 2])
    f.add_clause([-2])
    f.add_clause([-1,3])
    f.add_clause([-3, 2])
    sat, assignment = f.solve()
    assert sat is False


def test_cardinality_constraint():
    """
    Cardinality constraint test.
    """

    # F = (x1) ^ (~x1 v x2) ^ (~x1 ^ x2 ^ ~x3)
    # no constraint (should be satisfiable)
    f = CNF()
    f.add_clause([1])
    f.add_clause([-1, 2])
    f.add_clause([-1, 2, -3])
    sat, _ = f.solve()
    assert sat is True

    # constraint of 3 (should be satisfiable)
    f3 = f.copy()
    f3.add_cardinality_constraint(3)
    sat, _ = f3.solve()
    assert sat is True

    # constraint of 2 (should be satisfiable)
    f2 = f.copy()
    f2.add_cardinality_constraint(2)
    sat, _ = f2.solve()
    assert sat is True

    # constraint of 1 (should not be satisfiable)
    f1 = f.copy()
    f1.add_cardinality_constraint(1)
    sat, _ = f1.solve()
    assert sat is False
