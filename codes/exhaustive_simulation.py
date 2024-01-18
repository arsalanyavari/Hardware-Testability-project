from copy import deepcopy
from deductive_fault_simulation import deductive_fault_simulation
from ansii_colors import *

def exhaustive_simulation(circuit):
    exhaustive_simulation_values = []
    num_input_lines = len(circuit.inputs)
    
    for i in range(2**num_input_lines):
        binary_value = str(bin(i))[2:]
        binary_value = '0'*(num_input_lines-len(binary_value)) + binary_value
        for i in range(num_input_lines):
            circuit.inputs[i][1] = binary_value[i]

        circuit = deductive_fault_simulation(circuit)
        exhaustive_simulation_values.append([deepcopy(circuit.get_inputs()), deepcopy(circuit.get_outputs()), binary_value])
    
    return exhaustive_simulation_values

def print_exhaustive(exhaustive_list):
    for state in exhaustive_list:
        for i in state[0]:
            print(bcolors.GREEN + i[1], end='')
        print(":" + bcolors.RESET)
        stuck_ats = set()
        for i in state[1]:
            stuck_ats = stuck_ats | set(i[1])
        state.append(stuck_ats)
        for k in stuck_ats:
            print(k, end=' ') 
        print('') 
    return exhaustive_list

def print_fault_collapsing(exhaustive_list):
    collapsing_table = []
    for faults in exhaustive_list:
        for fault in faults[3]:
            index = None
            for i, inner_list in enumerate(collapsing_table):
                if inner_list and inner_list[0] == fault:
                    index = i
                    break
            
            if index is not None:
                collapsing_table[index].append(faults[2])
            else:
                collapsing_table.append([fault, faults[2]])
            
    collapsing_table = sorted(collapsing_table, key=len)
    result = []
    for stuck_at_index in range(len(collapsing_table)):
        result.append(collapsing_table[stuck_at_index][0])
        for inputs in collapsing_table[stuck_at_index][1:]:
            for index in range(stuck_at_index+1, len(collapsing_table)):
                if inputs in collapsing_table[index]:
                    collapsing_table.pop[index]
    return result