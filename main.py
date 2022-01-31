from ft_2_quantum_sat import fault_tree
from ft_2_quantum_sat import cnf

if __name__ == '__main__':
    
    # parse from XML
    ft = fault_tree.FaultTree()
    ft.load_from_xml("models/BSCU/BSCU.xml")
    ft.save_as_image('BSCU.png')

    bscu_cnf, _, _ = ft.to_cnf()
    sat, _ = bscu_cnf.solve()
    print(bscu_cnf)
    print(sat)
