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
        exhaustive_simulation_values.append([deepcopy(circuit.get_inputs()), deepcopy(circuit.get_outputs())])
    
    return exhaustive_simulation_values

def print_exhaustive(exhaustive_list):
    for state in exhaustive_list:
        print(bcolors.GREEN + "The circuit input is: " ,end='')
        for i in state[0]:
            print(i[1], end='')
        print(bcolors.RESET)
        stuck_ats = set()
        for i in state[1]:
            stuck_ats = stuck_ats | set(i[1])
        state.append(stuck_ats)
        for k in stuck_ats:
            print(k, end=' ') 
        print('') 
    return exhaustive_list
