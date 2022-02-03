from ft_2_quantum_sat import fault_tree

def test_ft_and():
    """
    Test a fault tree which is a sinlge AND gate with 2 inputs.
    """

    # build fault tree
    and_ft = fault_tree.FaultTree()
    and_ft.set_top_event('out')
    and_ft.add_basic_event('x1', 0.1)
    and_ft.add_basic_event('x2', 0.3)
    and_ft.add_gate('out', 'and', ['x1', 'x2'])

    # convert to CNF and solve
    and_cnf, var_mapping, _ = and_ft.to_cnf()
    sat, assignment = and_cnf.solve()
    assert sat == True
    assert var_mapping['x1'] in assignment
    assert var_mapping['x2'] in assignment
    assert var_mapping['out'] in assignment

def test_ft_or():
    """
    Test a fault tree which is a single OR gate with 2 inputs.
    """

    # build fault tree
    or_ft = fault_tree.FaultTree()
    or_ft.set_top_event('out')
    or_ft.add_basic_event('x1', 0.1)
    or_ft.add_basic_event('x2', 0.3)
    or_ft.add_gate('out', 'or', ['x1', 'x2'])

    # convert to CNF and solve
    or_cnf, vm, _ = or_ft.to_cnf()
    sat, a = or_cnf.solve()
    assert sat == True
    assert vm['x1'] in a or vm['x2'] in a
    assert vm['out'] in a

def test_ft_multi_and():
    """
    Test multi fan-in AND gate.
    """

    # build fault tree AND(x1, x2, x3)
    and_3_ft = fault_tree.FaultTree()
    and_3_ft.set_top_event('out')
    and_3_ft.add_basic_event('x1', 0.1)
    and_3_ft.add_basic_event('x2', 0.3)
    and_3_ft.add_basic_event('x3', 0.05)
    and_3_ft.add_gate('out', 'and', ['x1', 'x2', 'x3'])

    # convert to CNF and solve
    and_cnf, var_mapping, _ = and_3_ft.to_cnf()
    sat, assignment, = and_cnf.solve()
    assert sat == True
    assert var_mapping['x1'] in assignment
    assert var_mapping['x2'] in assignment
    assert var_mapping['x3'] in assignment
    assert var_mapping['out'] in assignment

    # build fault tree AND(x1, x2, x3, x4)
    and_4_ft = fault_tree.FaultTree()
    and_4_ft.set_top_event('out')
    and_4_ft.add_basic_event('x1', 0.1)
    and_4_ft.add_basic_event('x2', 0.3)
    and_4_ft.add_basic_event('x3', 0.05)
    and_4_ft.add_basic_event('x4', 0.2)
    and_4_ft.add_gate('out', 'and', ['x1', 'x2', 'x3', 'x4'])

    # convert to CNF and solve
    and_cnf, var_mapping, _ = and_4_ft.to_cnf()
    sat, assignment, = and_cnf.solve()
    assert sat == True
    assert var_mapping['x1'] in assignment
    assert var_mapping['x2'] in assignment
    assert var_mapping['x3'] in assignment
    assert var_mapping['x4'] in assignment
    assert var_mapping['out'] in assignment

    # build fault tree AND(x1, x2, x3, x4, x5)
    and_5_ft = fault_tree.FaultTree()
    and_5_ft.set_top_event('out')
    and_5_ft.add_basic_event('x1', 0.1)
    and_5_ft.add_basic_event('x2', 0.3)
    and_5_ft.add_basic_event('x3', 0.05)
    and_5_ft.add_basic_event('x4', 0.2)
    and_5_ft.add_basic_event('x5', 0.2)
    and_5_ft.add_gate('out', 'and', ['x1', 'x2', 'x3', 'x4', 'x5'])

    # convert to CNF and solve
    and_cnf, var_mapping, _ = and_5_ft.to_cnf()
    sat, assignment, = and_cnf.solve()
    assert sat == True
    assert var_mapping['x1'] in assignment
    assert var_mapping['x2'] in assignment
    assert var_mapping['x3'] in assignment
    assert var_mapping['x4'] in assignment
    assert var_mapping['x5'] in assignment
    assert var_mapping['out'] in assignment

def test_ft_multi_or():
    """
    Test multi fan-in OR gate.
    """

    # build fault tree OR(x1, x2, x3)
    or_3_ft = fault_tree.FaultTree()
    or_3_ft.set_top_event('out')
    or_3_ft.add_basic_event('x1', 0.1)
    or_3_ft.add_basic_event('x2', 0.3)
    or_3_ft.add_basic_event('x3', 0.2)
    or_3_ft.add_gate('out', 'or', ['x1', 'x2', 'x3'])

    # convert to CNF and solve
    or_cnf, vm, _ = or_3_ft.to_cnf()
    sat, a = or_cnf.solve()
    assert sat == True
    assert (vm['x1'] in a) or (vm['x2'] in a) or (vm['x3'] in a)
    assert vm['out'] in a

    # build fault tree OR(x1, x2, x3, x4)
    or_4_ft = fault_tree.FaultTree()
    or_4_ft.set_top_event('out')
    or_4_ft.add_basic_event('x1', 0.1)
    or_4_ft.add_basic_event('x2', 0.3)
    or_4_ft.add_basic_event('x3', 0.2)
    or_4_ft.add_basic_event('x4', 0.1)
    or_4_ft.add_gate('out', 'or', ['x1', 'x2', 'x3', 'x4'])

    # convert to CNF and solve
    or_cnf, vm, _ = or_4_ft.to_cnf()
    sat, a = or_cnf.solve()
    assert sat == True
    assert  (vm['x1'] in a) or (vm['x2'] in a) or \
            (vm['x3'] in a) or (vm['x4'] in a)
    assert vm['out'] in a

    # build fault tree OR(x1, x2, x3, x4, x5)
    or_5_ft = fault_tree.FaultTree()
    or_5_ft.set_top_event('out')
    or_5_ft.add_basic_event('x1', 0.1)
    or_5_ft.add_basic_event('x2', 0.3)
    or_5_ft.add_basic_event('x3', 0.2)
    or_5_ft.add_basic_event('x4', 0.1)
    or_5_ft.add_basic_event('x5', 0.05)
    or_5_ft.add_gate('out', 'or', ['x1', 'x2', 'x3', 'x4', 'x5'])

    # convert to CNF and solve
    or_cnf, vm, _ = or_5_ft.to_cnf()
    sat, a = or_cnf.solve()
    assert sat == True
    assert  (vm['x1'] in a) or (vm['x2'] in a) or \
            (vm['x3'] in a) or (vm['x4'] in a) or (vm['x5'] in a)
    assert vm['out'] in a



def test_ft_example_1():
    """
    Test translation of fault tree to CNF formula on example.
    """

    # build simple fault tree
    car_ft = fault_tree.FaultTree()
    car_ft.set_top_event('car breaks')
    car_ft.add_basic_event('engine breaks', 0.05)
    car_ft.add_basic_event('wheel breaks', 0.1)
    car_ft.add_basic_event('no spare', 0.3)
    car_ft.add_gate('car breaks', 'or', ['engine breaks', 'wheel issue'])
    car_ft.add_gate('wheel issue', 'and', ['wheel breaks', 'no spare'])

    # convert to CNF
    car_cnf, var_mapping, input_vars = car_ft.to_cnf()

    # solve without cardinality constraint 
    sat, assignment = car_cnf.solve()
    assert sat == True
    assert var_mapping['car breaks'] in assignment

    # cardinality constraint of 3 *over input vars only*
    car_cnf3 = car_cnf.copy()
    car_cnf3.add_cardinality_constraint(3, variables=input_vars.values())
    sat, assignment = car_cnf3.solve()
    assert sat == True
    assert var_mapping['car breaks'] in assignment

    # cardinality constraint of 2 *over input vars only*
    car_cnf2 = car_cnf.copy()
    car_cnf2.add_cardinality_constraint(2, variables=input_vars.values())
    sat, assignment = car_cnf2.solve()
    print(sat, assignment)
    assert sat == True
    assert var_mapping['car breaks'] in assignment

    # cardinality constraint of 1 *over input vars only*
    car_cnf1 = car_cnf.copy()
    car_cnf1.add_cardinality_constraint(1, variables=input_vars.values())
    sat, assignment = car_cnf1.solve()
    print(sat, assignment)
    assert sat == True
    assert var_mapping['car breaks'] in assignment
    
def test_ft_example_2():
    """
    Test translation of fault tree to CNF formula on example.
    """

    # build simple fault tree
    pc_ft = fault_tree.FaultTree()
    pc_ft.set_top_event('pc fails')
    pc_ft.add_basic_event('high cpu load', 0.5)
    pc_ft.add_basic_event('fan breaks', 0.1)
    pc_ft.add_basic_event('power out', 0.1)
    pc_ft.add_basic_event('battery fail', 0.2)
    pc_ft.add_gate('too hot', 'and', ['high cpu load', 'fan breaks'])
    pc_ft.add_gate('no power', 'and', ['power out', 'battery fail'])
    pc_ft.add_gate('pc fails', 'or', ['too hot', 'no power'])

    # convert to CNF
    pc_cnf, var_mapping, input_vars = pc_ft.to_cnf()

    # solve without cardinality constraint 
    sat, assignment = pc_cnf.solve()
    assert sat == True
    assert var_mapping['pc fails'] in assignment

    # cardinality constraint of 3 *over input vars only*
    pc_cnf3 = pc_cnf.copy()
    pc_cnf3.add_cardinality_constraint(3, variables=input_vars.values())
    sat, assignment = pc_cnf3.solve()
    assert sat == True
    assert var_mapping['pc fails'] in assignment

    # cardinality constraint of 2 *over input vars only*
    pc_cnf2 = pc_cnf.copy()
    pc_cnf2.add_cardinality_constraint(2, variables=input_vars.values())
    sat, assignment = pc_cnf2.solve()
    assert sat == True
    assert var_mapping['pc fails'] in assignment

    # cardinality constraint of 1 *over input vars only*
    pc_cnf1 = pc_cnf.copy()
    pc_cnf1.add_cardinality_constraint(1, variables=input_vars.values())
    sat, assignment = pc_cnf1.solve()
    assert sat == False
