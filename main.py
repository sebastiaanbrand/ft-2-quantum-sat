from ft_2_quantum_sat import fault_tree
from ft_2_quantum_sat import cnf

if __name__ == '__main__':
    
    # parse from XML
    #ft = fault_tree.FaultTree()
    #ft.load_from_xml("models/BSCU/BSCU.xml")
    #ft.save_as_image('BSCU.png')

    #bscu_cnf, _, _ = ft.to_cnf()
    #sat, _ = bscu_cnf.solve()
    #print(bscu_cnf)
    #print(sat)

    f = cnf.CNF()
    f.add_clause([-1, -2, -3])
    f.add_clause([1, -2, 3])
    f.add_clause([1, 2, -3])
    f.add_clause([1, -2, -3])
    f.add_clause([-1, 2, 3])

    print(f)

    assignments = f.solve()
    print(assignments)

    assignments = f.solve_n(n=3)
    print(assignments)

    assignments = f.solve(method='grover')
    print(assignments)

    assignments = f.solve_n(n=3, method='grover')
    print(assignments)

    ft = fault_tree.FaultTree()
    cutsets = ft.compute_min_cutsets(n=2, method='classical', cnf=f)
    print("cutsets:", cutsets)

    ft = fault_tree.FaultTree()
    cutsets = ft.compute_min_cutsets(n=2, method='grover', cnf=f)
    print("cutsets:", cutsets)

