"""
(Just for testing some suff, remove later).
"""
from ft_2_quantum_sat.cnf import CNF

if __name__ == '__main__':
    cnf = CNF()
    cnf.add_clause([-1,2,-3])
    cnf.add_clause([-1,-2,3])
    cnf.add_clause([1,-2,4])
    cnf.add_clause([2,3,-4])
    cnf.add_clause([-1,-2,-3])
    sat, model = cnf.solve(method='grover-qiskit')
    print(sat)
    print(model)

    sat, model = cnf.solve(method='grover-myqlm')
    print(sat)
    print(model)

"""
# Some small test to see if everything imports correctly
prog = Program()
qbools = prog.qalloc(2, QBoolArray)
for q in qbools:
    H(q)
expr = qbools[0]# & qbools[1]
expr = expr & qbools[1]
expr.phase()
print(type(expr))
print(expr)
print(qbools[0])

job = prog.to_circ().to_job(nbshots=1000)
result = get_default_qpu().submit(job)
for sample in result:
    print(sample.state, sample.probability)
"""