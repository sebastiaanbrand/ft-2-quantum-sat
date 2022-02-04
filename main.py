#from ft_2_quantum_sat import cnf, fault_tree
from ft_2_quantum_sat.cnf import CNF
from ft_2_quantum_sat.fault_tree import FaultTree

if __name__ == '__main__':
    
    # parse from XML
    #ft = fault_tree.FaultTree()
    ft = FaultTree.load_from_xml("models/BSCU/BSCU.xml")
    ft.save_as_image('BSCU.pdf')
    cutsets = ft.compute_min_cutsets(m=3, method='classical')
    print("cutsets:", cutsets)

    #bscu_cnf, _, _ = ft.to_cnf()
    #sat, _ = bscu_cnf.solve()
    #print(bscu_cnf)
    #print(sat)
