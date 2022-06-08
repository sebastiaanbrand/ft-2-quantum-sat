"""
MyQLM functionality needed for SAT solving
"""

from qat.lang.AQASM import QRoutine, H, X, Z
from qat.lang.AQASM import QBoolArray
#from qat.qpus import get_default_qpu


def _lit_to_qbool(lit, qbools):
    """
    For a CNF literal, returns the corresponding QBool literal.

    The CNF literals are numbered from 1 to n, while qbools start at 0, so
    the index is shifted by -1.

    E.g. 3 --> q[2], -5 --> ~q[4]
    """
    if lit > 0:
        return qbools[lit-1]
    else:
        return ~qbools[abs(lit)-1]


def _clause_to_qbool_clause(clause, qbools):
    """
    For a CNF clause, return the corresponding QClause expression.
    """
    lit_iterator = iter(clause)

    # set qclause to first literal
    qclause = _lit_to_qbool(next(lit_iterator), qbools)

    # add OR of other literals
    for lit in lit_iterator:
        qclause = qclause | _lit_to_qbool(lit, qbools)

    return qclause


def _cnf_to_qbool_expression(n, clauses, qbools):
    """
    Returns a MyQLM QBool expression (QClause) of this CNF formula.
    """
    if len(qbools) < n:
        raise ValueError(f"Too few QBools ('{len(qbools)}') for CNF vars '{n}'")

    clause_iterator = iter(clauses)

    # set expr to first clause
    expr = _clause_to_qbool_clause(next(clause_iterator), qbools)

    # add AND of other clauses
    for clause in clause_iterator:
        expr = expr & _clause_to_qbool_clause(clause, qbools)

    return expr


def oracle_from_cnf(n, clauses):
    """
    Constructs a phase oracle from the given CNF formula.
    """
    routine = QRoutine()
    qbools = routine.new_wires(n, QBoolArray)

    for wire in qbools:
        H(wire)
    expr = _cnf_to_qbool_expression(n, clauses, qbools)
    expr.phase()

    return routine


def diffusion(n):
    """
    Diffusion operator for n variables.

    ```
    --[H]--[X]--*--[X]--[H]--
                |
    --[H]--[X]--*--[X]--[H]--
                |
    --[H]--[X]--*--[X]--[H]--
                |
                .
                |
    --[H]--[X]--*--[X]--[H]--
    ```
    """
    routine = QRoutine()
    wires = routine.new_wires(n)

    for wire in wires:
        H(wire)
        X(wire)
    Z.ctrl(n - 1)(wires) # should this be n-1 or n?
    for wire in wires:
        H(wire)
        X(wire)

    return routine


def grover_var_map(n):
    """
    Creates a map: var_num -> qubit_num.
    (Needed when parsing the measurement results.)
    """
    res = {}
    for i in range(n):
        res[i+1] = i
    return res
