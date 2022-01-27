
from ft_2_quantum_sat import cnf


def test_new_vars():
    """
    Testing getting new vars for CNF formula
    """
    f = cnf.CNF()
    assert f.num_vars == 0

    # variables should be added consecutively starting from 1
    f.add_var(1)
    f.add_var(2)
    assert f.num_vars == 2

    # the new variable should only be allowed to be 3
    failed_to_add = False
    try:
        f.add_var(6)
    except:
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


def test_linking_tree():
    """
    Testing tree used to build cardinality constraint.
    """
    tree = cnf.LinkingTree([1,2,3,4,5])
    # TODO
