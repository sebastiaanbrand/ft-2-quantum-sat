
from ft_2_quantum_sat import cnf

def test_solve():
    """
    Testing solve() function
    """
    f = cnf.CNF()
    f.add_clause([1, 2])
    f.add_clause([-2])
    f.add_clause([3, 2, -1])
    sat, assignment = f.solve()
    assert sat == True
    assert assignment == [1, -2, 3]


    f = cnf.CNF()
    f.add_clause([1, 2])
    f.add_clause([-2])
    f.add_clause([-1,3])
    f.add_clause([-3, 2])
    sat, assignment = f.solve()
    assert sat == False