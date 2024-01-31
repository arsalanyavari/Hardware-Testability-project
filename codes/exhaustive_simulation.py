from copy import deepcopy
from random import choice
from construct_circuit import construct_circuit
from deductive_fault_simulation import deductive_fault_simulation
from ansii_colors import *
from true_value_simulation import true_value_simulation

def exhaustive_simulation(code, circuit):
    exhaustive_simulation_values = []
    circuit_inputs = circuit.get_inputs()
    num_input_lines = len(circuit.inputs)
    
    for i in range(2**num_input_lines):
        # inputs = bin(i)[2:].zfill(len(circuit_inputs))
        inputs = str(bin(i))[2:]
        inputs = '0'*(num_input_lines-len(inputs)) + inputs
        for i in range(len(circuit_inputs)):
            circuit_inputs[i][1] = inputs[i]

        circuit = construct_circuit(code ,circuit_inputs)
        circuit = true_value_simulation(circuit)
        circuit = deductive_fault_simulation(circuit)
        exhaustive_simulation_values.append([deepcopy(circuit.get_inputs()), deepcopy(circuit.get_output_faults()), inputs])
    
    return exhaustive_simulation_values

def print_exhaustive(exhaustive_list):
    for state in exhaustive_list:
        print(bcolors.GREEN + "The circuit input is: " ,end='')
        for i in state[0]:
            print(i[1], end='')
        print(bcolors.RESET)
        stuck_ats = set()
        stuck_ats.clear()
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
    stuck_at_index = 0
    while stuck_at_index < len(collapsing_table):
        inputs = choice(collapsing_table[stuck_at_index][1:]) 
        result.append(inputs)
        index = stuck_at_index+1
        while index < len(collapsing_table):
            if inputs in collapsing_table[index]:
                collapsing_table.pop(index)
            else:
                index += 1
        stuck_at_index += 1
    print(' '.join(map(str, result)))
    return result
