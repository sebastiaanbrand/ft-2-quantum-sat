"""
Tests for the fault_tree module.
"""

from ft_2_quantum_sat.fault_tree import FaultTree

def test_ft_and():
    """
    Test a fault tree which is a sinlge AND gate with 2 inputs.
    """

    # build fault tree
    and_ft = FaultTree()
    and_ft.set_top_event('out')
    and_ft.add_basic_event('x1', 0.1)
    and_ft.add_basic_event('x2', 0.3)
    and_ft.add_gate('out', 'and', ['x1', 'x2'])

    # convert to CNF and solve
    and_cnf, var_mapping, _ = and_ft.to_cnf()
    sat, assignment = and_cnf.solve()
    assert sat is True
    assert var_mapping['x1'] in assignment
    assert var_mapping['x2'] in assignment
    assert var_mapping['out'] in assignment


def test_ft_or():
    """
    Test a fault tree which is a single OR gate with 2 inputs.
    """

    # build fault tree
    or_ft = FaultTree()
    or_ft.set_top_event('out')
    or_ft.add_basic_event('x1', 0.1)
    or_ft.add_basic_event('x2', 0.3)
    or_ft.add_gate('out', 'or', ['x1', 'x2'])

    # convert to CNF and solve
    or_cnf, vm, _ = or_ft.to_cnf()
    sat, a = or_cnf.solve()
    assert sat is True
    assert vm['x1'] in a or vm['x2'] in a
    assert vm['out'] in a


def test_ft_multi_and():
    """
    Test multi fan-in AND gate.
    """

    # build fault tree AND(x1, x2, x3)
    and_3_ft = FaultTree()
    and_3_ft.set_top_event('out')
    and_3_ft.add_basic_event('x1', 0.1)
    and_3_ft.add_basic_event('x2', 0.3)
    and_3_ft.add_basic_event('x3', 0.05)
    and_3_ft.add_gate('out', 'and', ['x1', 'x2', 'x3'])

    # convert to CNF and solve
    and_cnf, var_mapping, _ = and_3_ft.to_cnf()
    sat, assignment, = and_cnf.solve()
    assert sat is True
    assert var_mapping['x1'] in assignment
    assert var_mapping['x2'] in assignment
    assert var_mapping['x3'] in assignment
    assert var_mapping['out'] in assignment

    # build fault tree AND(x1, x2, x3, x4)
    and_4_ft = FaultTree()
    and_4_ft.set_top_event('out')
    and_4_ft.add_basic_event('x1', 0.1)
    and_4_ft.add_basic_event('x2', 0.3)
    and_4_ft.add_basic_event('x3', 0.05)
    and_4_ft.add_basic_event('x4', 0.2)
    and_4_ft.add_gate('out', 'and', ['x1', 'x2', 'x3', 'x4'])

    # convert to CNF and solve
    and_cnf, var_mapping, _ = and_4_ft.to_cnf()
    sat, assignment, = and_cnf.solve()
    assert sat is True
    assert var_mapping['x1'] in assignment
    assert var_mapping['x2'] in assignment
    assert var_mapping['x3'] in assignment
    assert var_mapping['x4'] in assignment
    assert var_mapping['out'] in assignment

    # build fault tree AND(x1, x2, x3, x4, x5)
    and_5_ft = FaultTree()
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
    assert sat is True
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
    or_3_ft = FaultTree()
    or_3_ft.set_top_event('out')
    or_3_ft.add_basic_event('x1', 0.1)
    or_3_ft.add_basic_event('x2', 0.3)
    or_3_ft.add_basic_event('x3', 0.2)
    or_3_ft.add_gate('out', 'or', ['x1', 'x2', 'x3'])

    # convert to CNF and solve
    or_cnf, vm, _ = or_3_ft.to_cnf()
    sat, a = or_cnf.solve()
    assert sat is True
    assert (vm['x1'] in a) or (vm['x2'] in a) or (vm['x3'] in a)
    assert vm['out'] in a

    # build fault tree OR(x1, x2, x3, x4)
    or_4_ft = FaultTree()
    or_4_ft.set_top_event('out')
    or_4_ft.add_basic_event('x1', 0.1)
    or_4_ft.add_basic_event('x2', 0.3)
    or_4_ft.add_basic_event('x3', 0.2)
    or_4_ft.add_basic_event('x4', 0.1)
    or_4_ft.add_gate('out', 'or', ['x1', 'x2', 'x3', 'x4'])

    # convert to CNF and solve
    or_cnf, vm, _ = or_4_ft.to_cnf()
    sat, a = or_cnf.solve()
    assert sat is True
    assert  (vm['x1'] in a) or (vm['x2'] in a) or \
            (vm['x3'] in a) or (vm['x4'] in a)
    assert vm['out'] in a

    # build fault tree OR(x1, x2, x3, x4, x5)
    or_5_ft = FaultTree()
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
    assert sat is True
    assert  (vm['x1'] in a) or (vm['x2'] in a) or \
            (vm['x3'] in a) or (vm['x4'] in a) or (vm['x5'] in a)
    assert vm['out'] in a


def test_ft_example_1():
    """
    Test translation of fault tree to CNF formula on example.
    """

    # build simple fault tree
    car_ft = FaultTree()
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
    assert sat is True
    assert var_mapping['car breaks'] in assignment

    # cardinality constraint of 3 *over input vars only*
    car_cnf3 = car_cnf.copy()
    car_cnf3.add_cardinality_constraint(3, variables=input_vars)
    sat, assignment = car_cnf3.solve()
    assert sat is True
    assert var_mapping['car breaks'] in assignment

    # cardinality constraint of 2 *over input vars only*
    car_cnf2 = car_cnf.copy()
    car_cnf2.add_cardinality_constraint(2, variables=input_vars)
    sat, assignment = car_cnf2.solve()
    print(sat, assignment)
    assert sat is True
    assert var_mapping['car breaks'] in assignment

    # cardinality constraint of 1 *over input vars only*
    car_cnf1 = car_cnf.copy()
    car_cnf1.add_cardinality_constraint(1, variables=input_vars)
    sat, assignment = car_cnf1.solve()
    print(sat, assignment)
    assert sat is True
    assert var_mapping['car breaks'] in assignment

    # there is one cutset of size 1, and one cutset of size 2, asking for m = 1
    # cutsets should only yield the smallest one of the two
    cutsets = car_ft.compute_min_cutsets(m=1, method='classical')
    assert len(cutsets) == 1
    assert {'engine breaks'} in cutsets

    # asking for more cutsets should yield both
    cutsets = car_ft.compute_min_cutsets(m=5, method='classical')
    assert len(cutsets) == 2
    assert {'engine breaks'} in cutsets
    assert {'wheel breaks', 'no spare'} in cutsets


def test_ft_example_2():
    """
    Test translation of fault tree to CNF formula on example.
    """

    # build simple fault tree
    pc_ft = FaultTree()
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
    assert sat is True
    assert var_mapping['pc fails'] in assignment

    # cardinality constraint of 3 *over input vars only*
    pc_cnf3 = pc_cnf.copy()
    pc_cnf3.add_cardinality_constraint(3, variables=input_vars)
    sat, assignment = pc_cnf3.solve()
    assert sat is True
    assert var_mapping['pc fails'] in assignment

    # cardinality constraint of 2 *over input vars only*
    pc_cnf2 = pc_cnf.copy()
    pc_cnf2.add_cardinality_constraint(2, variables=input_vars)
    sat, assignment = pc_cnf2.solve()
    assert sat is True
    assert var_mapping['pc fails'] in assignment

    # cardinality constraint of 1 *over input vars only*
    pc_cnf1 = pc_cnf.copy()
    pc_cnf1.add_cardinality_constraint(1, variables=input_vars)
    sat, assignment = pc_cnf1.solve()
    assert sat is False

    # there should only be two minimal cut sets (both of size 2)
    cutsets = pc_ft.compute_min_cutsets(m=5, method='classical')
    assert len(cutsets) == 2
    assert {'power out', 'battery fail'} in cutsets
    assert {'high cpu load', 'fan breaks'} in cutsets


def test_parse_xml():
    """
    Test parsing of XML file on BSCU example.
    """
    ft = FaultTree.load_from_xml("models/BSCU/BSCU.xml")

    # node count
    assert ft.graph.number_of_nodes() == 15

    # top event
    assert ft.top_event == 'LossOfBrakingCommands'

    # basic event
    assert 'ValidityMonitorFailure' in ft.basic_events
    assert 'SwitchStuckInIntermediatePosition' in ft.basic_events
    assert 'SwitchStuckInPosition1' in ft.basic_events
    assert 'SwitchStuckInPosition2' in ft.basic_events
    assert 'System1ElectronicFailure' in ft.basic_events
    assert 'System2ElectronicFailure' in ft.basic_events
    assert 'LossOfSystem1PowerSupply' in ft.basic_events
    assert 'LossOfSystem2PowerSupply' in ft.basic_events

    # gates
    assert ft.node_types['LossOfBrakingCommands'] == 'or'
    assert ft.node_types['SwitchFailure'] == 'or'
    assert ft.node_types['SwitchFailsInPosition1AndSystem1Fails'] == 'and'
    assert ft.node_types['SwitchFailsInPosition2AndSystem2Fails'] == 'and'
    assert ft.node_types['Systems1And2DoNotOperate'] == 'and'
    assert ft.node_types['LossOfSystem1'] == 'or'
    assert ft.node_types['LossOfSystem2'] == 'or'

    # gate inputs
    assert 'ValidityMonitorFailure' in ft.get_gate_inputs('LossOfBrakingCommands')
    assert 'SwitchFailure' in ft.get_gate_inputs('LossOfBrakingCommands')
    assert 'Systems1And2DoNotOperate' in ft.get_gate_inputs('LossOfBrakingCommands')

    assert 'SwitchStuckInIntermediatePosition' in ft.get_gate_inputs('SwitchFailure')
    assert 'SwitchFailsInPosition1AndSystem1Fails' in ft.get_gate_inputs('SwitchFailure')
    assert 'SwitchFailsInPosition2AndSystem2Fails' in ft.get_gate_inputs('SwitchFailure')

    assert 'LossOfSystem1' in ft.get_gate_inputs('Systems1And2DoNotOperate')
    assert 'LossOfSystem2' in ft.get_gate_inputs('Systems1And2DoNotOperate')

    assert 'System1ElectronicFailure' in ft.get_gate_inputs('LossOfSystem1')
    assert 'LossOfSystem1PowerSupply' in ft.get_gate_inputs('LossOfSystem1')

    assert 'System2ElectronicFailure' in ft.get_gate_inputs('LossOfSystem2')
    assert 'LossOfSystem2PowerSupply' in ft.get_gate_inputs('LossOfSystem2')

    assert 'SwitchStuckInPosition1' in ft.get_gate_inputs('SwitchFailsInPosition1AndSystem1Fails')
    assert 'LossOfSystem1' in ft.get_gate_inputs('SwitchFailsInPosition1AndSystem1Fails')

    assert 'SwitchStuckInPosition2' in ft.get_gate_inputs('SwitchFailsInPosition2AndSystem2Fails')
    assert 'LossOfSystem2' in ft.get_gate_inputs('SwitchFailsInPosition2AndSystem2Fails')


def test_cutsets_theatre():
    """
    Testing finding the minimal cut sets of the theatre example.
    """
    ft = FaultTree.load_from_xml("models/Theatre/theatre.xml")

    # There are exactly two minimal cutsets, so if we ask for three we should
    # only get two.
    for method in ['classical', 'min-sat']:
        cutsets = ft.compute_min_cutsets(m=3, method=method)
        assert len(cutsets) == 2
        assert {'Mains_Fail', 'Gen_Fail'} in cutsets
        assert {'Mains_Fail', 'Relay_Fail'} in cutsets


def test_cutsets_smalltree():
    """
    Testing finding the minimal cut sets of the SmallTree example.
    """
    ft = FaultTree.load_from_xml("models/SmallTree/SmallTree.xml")

    # There are exactly two minimal cutsets, so if we ask for three we should
    # only get two.
    for method in ['classical', 'min-sat']:
        cutsets = ft.compute_min_cutsets(m=3, method=method)
        assert len(cutsets) == 2
        assert {'e1', 'e2'} in cutsets
        assert {'e3', 'e4'} in cutsets


def test_cutsets_bscu():
    """
    Testing finding the minimal cut sets of the BSCU example.
    """
    ft = FaultTree.load_from_xml("models/BSCU/BSCU.xml")

    # There are exactly two cutsets of size 1, so getting the m=2 smallest
    # cutsets should yield these two
    for method in ['classical', 'min-sat']:
        cutsets = ft.compute_min_cutsets(m=2, method=method)
        assert len(cutsets) == 2
        assert {'ValidityMonitorFailure'} in cutsets
        assert {'SwitchStuckInIntermediatePosition'} in cutsets
