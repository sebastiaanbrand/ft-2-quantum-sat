#import xml.etree.ElementTree as ET

from ft_2_quantum_sat import fault_tree
from ft_2_quantum_sat import cnf

if __name__ == '__main__':
    #file = 'mef-examples-master/Lift/lift.xml'
    #fault_tree = FaultTree.from_xml(file, 'Lift')

    #fault_tree.to_string()
    f = cnf.CNF()
    #f.add_clause([3,2,1])
    #f.add_clause([1,4,-3])
    #f.add_clause([3,3,2])

    v1 = f.get_new_var()
    v2 = f.get_new_var()
    v3 = f.add_tseitin_AND(v1, v2)
    v4 = f.get_new_var()
    v5 = f.add_tseitin_OR(v3, v4)
    v6 = f.add_tseitin_NOT(v5)

    print(f)

    
    car_ft = fault_tree.FaultTree()
    car_ft.set_top_event('car breaks')
    car_ft.add_gate('car breaks', 'or', ['engine breaks', 'wheel issue'])
    car_ft.add_gate('wheel issue', 'and', ['wheel breaks', 'no spare'])
    car_ft.save_as_image('car_ft.png')
