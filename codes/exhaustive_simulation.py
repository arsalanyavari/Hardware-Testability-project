import copy
from deductive_fault_simulation import *

def exhaustive_simulation(circuit):
    exhaustive_simulation_values = []
    num_input_lines = len(circuit.inputs)
    
    for i in range(2**num_input_lines):
        binary_value = str(bin(i))[2:]
        binary_value = '0'*(num_input_lines-len(binary_value)) + binary_value
        for i in range(num_input_lines):
            circuit.inputs[i][1] = binary_value[i]

        circuit = deductive_fault_simulation(circuit)
        exhaustive_simulation_values.append([copy.deepcopy(circuit.get_inputs()), copy.deepcopy(circuit.get_outputs())])
    
    return exhaustive_simulation_values

if __name__ == "__main__":      #TODO: complete the main function
    pass
