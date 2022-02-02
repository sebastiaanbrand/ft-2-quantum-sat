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

    sat, assignment = f.solve()
    print(sat, assignment)

    sat, assignment = f.solve(method='grover')
    print(sat, assignment)

    ft = fault_tree.FaultTree()
    cutsets = ft.compute_min_cutsets(m=4, method='classical', cnf=f)
    print("cutsets:", cutsets)

    ft = fault_tree.FaultTree()
    cutsets = ft.compute_min_cutsets(m=2, method='grover', cnf=f)
    print("cutsets:", cutsets)

