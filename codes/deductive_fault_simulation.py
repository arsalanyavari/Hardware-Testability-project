from true_value_simulation import *


file_name = input("Please enter the bench file name")
circuit = true_value_simulation()

def specify_fault_lists(gate_type, gate_inputs, gate_output):
    if gate_type == "AND":
        #sec1
        counter_1 = 0
        for i in gate_inputs:
            if i[1] == 1:
                counter_1 += 1
        
        if counter_1 == len(gate_inputs):
            return ['u'] + [sublist[0] for sublist in gate_inputs]
        else:
            return_list = ['i']
            for i in gate_inputs:
                if i[1] == 0:
                    return_list.append(i[0])
            return return_list
                    
        
        #sec2 [['0', 1], ['03', 1]]
            

        #sec3
        
        # return [], [], []
    if gate_type == "NAND":
        inversion = True
        l_list = []
        s_list = []
        #section 1
        for g_input in gate_inputs:
            if g_input[1] == 0:
                s_list.append(g_input)
            else: 
                l_list.append(g_input)
        
        
    if gate_type == "OR":
        pass
    if gate_type == "NOR":
        pass
    if gate_type == "XOR":
        pass
    if gate_type == "XNOR":
        pass
    if gate_type == "NOT":
        pass
    if gate_type == "BUFFER":
        pass
     

def calculate_faults():
    wire = Wire()
    gates = circuit.get_gates()
        
    for g_input in inputs:
        pass
    for gate in gates:
        inputs = gate.get_inputs()
        for gate_input in inputs:
            faults = []
            wire.set_name(gate_input[0])
            wire.set_value(gate_input[1])
            
            
        
class Wire:
    def __init__(self):
        self.value = ''
        self.name = ''
        self.faults = []

    def set_value(self, value_):
        self.value = value_
        
    def get_value(self):
        return self.value

    def set_name(self, name_):
       self.name = name_ 
    
    def get_name(self):
        return self.name
        
    def set_faults(self, fault_):
        self.faults = fault_
    
    def get_faults(self):
        return self.faults