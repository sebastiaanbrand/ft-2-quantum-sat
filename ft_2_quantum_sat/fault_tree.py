import xml.etree.ElementTree as ET

class FaultTree: 
    def __init__(self, name, gate, value=0):
        self.name  = name
        self.value = value
        self.gate  = gate
        self.child = []
    
    @staticmethod
    def from_xml(filename, name):
        gate_tags = {'and', 'or'}
    
        xml_tree = ET.parse(filename)
        xml_root = xml_tree.getroot()
        ft_def   = xml_root[0]
        model_data = xml_root[1]
        
        assert (ft_def.tag == 'define-fault-tree')
        assert (model_data.tag == 'model-data')
        print(xml_root)
        print(ft_def)
        print(model_data)
        print("\n")

        fault_tree = FaultTree(name, "root")

        for gate_def in ft_def:
            assert (gate_def.tag == 'define-gate')
            event_name = gate_def.attrib["name"]
            
            # loop over child elements of this <define-gate>
            # to find whether this is an 'and' or an 'or' gate
            gate_tag = ''
            gate_inputs = []
            for child in gate_def:
                if (child.tag == 'label'):
                    continue # ignore labels for now
                if (child.tag in gate_tags):
                    gate_tag = child.tag
                    gate_inputs = child.getchildren()
            
            # add this gate node to FT if not exists yet,
            # otherwise look up existing node
            node = fault_tree.get_child(event_name)
            if node == None:
                fault_tree.insert_child(event_name, gate_tag)
                node = fault_tree.get_child(event_name)
            else:
                node.gate = gate_def.tag

            # add the inputs to this gate to the FT
            # TODO: should we not check whether these nodes
            # already exist?
            for input_node in gate_inputs:
                node.insert_child(input_node.attrib['name'], '')
            print(gate_def[0])
            #for x in gate_def[0]:
            #    print(x.attrib["name"])
            #    node.insert_child(x.attrib["name"], "") 
            #elif gate_def.tag == "define-basic-event":
            #    continue
            #elif gate_def.tag == "exponential":
            #    continue
            #break
        return fault_tree

    
    def insert_child(self, name, gate, value=0):
        self.child.append(FaultTree(name,gate,value))
        
    
    def get_child(self, name):
        for k in self.child:
            if k.name==name:
                return k
        return None
    
    def get_child(self,name):
        if self.name == name:
            return self
        else:
            for k in self.child:
                child_ = k.get_child(name)
                if child_ != None :
                    return child_
        return None
    
    def to_string(self, indent=0):
        _indent = '\t'*indent
        print(_indent, "---------------------")
        print(_indent, "Name     : ", self.name)
        print(_indent, "Value    : ", self.value)
        print(_indent, "Gate     : ", self.gate)
        print(_indent, "Children : ", len(self.child))
        print(_indent, "---------------------")
        for i in self.child:
            i.to_string(indent=indent+1)
        
    
    def _print_values(self):
        print("Value: ", self.value)
        for c in self.child:
            c._print_values()
