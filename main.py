from ft_2_quantum_sat import cnf, fault_tree

if __name__ == '__main__':
    
    # parse from XML
    #ft = fault_tree.FaultTree()
    ft = fault_tree.FaultTree.load_from_xml("models/BSCU/BSCU.xml")
    ft.save_as_image('BSCU.pdf')
    cutsets = ft.compute_min_cutsets(m=3, method='classical')
    print("cutsets:", cutsets)

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
    f.var_names = {1 : 'x1', 2 : 'x2', 3 : 'x3'}

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

