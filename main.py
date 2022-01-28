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
    car_ft.add_basic_event('engine breaks', 0.05)
    car_ft.add_basic_event('wheel breaks', 0.1)
    car_ft.add_basic_event('no spare', 0.3)
    car_ft.add_gate('car breaks', 'or', ['engine breaks', 'wheel issue'])
    car_ft.add_gate('wheel issue', 'and', ['wheel breaks', 'no spare'])

    car_cnf, var_mapping, input_vars = car_ft.to_cnf()
    print(var_mapping)
    print(input_vars)
    print(list(input_vars.values()))

    # solve without cardinality constraint 
    sat, assignment = car_cnf.solve()
    print(sat, assignment)
    assert sat == True
    assert var_mapping['car breaks'] in assignment
