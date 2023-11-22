import re
from gates import *
from ansii_colors import bcolors

class Circuit:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.gates = []

    def set_inputs(self, _inputs): 
        self.inputs = _inputs

    def get_inputs(self): 
        return self.inputs

    def set_outputs(self, _outputs): 
        self.outputs = _outputs

    def get_outputs(self): 
        return self.outputs

    def set_gates(self, _gates): 
        self.gates = _gates

    def get_gates(self): 
        return self.gates

class Gate:
    def __init__(self):
        self.gate_inputs = []
        self.gate_output = {}
        self.gate_type = ''

    def set_inputs(self, _inputs): 
        self.gate_inputs = _inputs

    def get_inputs(self): 
        return self.gate_inputs

    def set_output(self, _output): 
        self.gate_output = _output

    def get_output(self): 
        return self.gate_output

    def set_gate_type(self, _gate_type): 
        self.gate_type = _gate_type

    def get_gate_type(self): 
        return self.gate_type
    
def get_file(file_name):
    file_path = "../bench files/" + file_name + ".bench"
    code = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('#') or not line:
                continue
            code.append(line)
    return code

def construct_circuit(code, user_input=[]):
    circuit = Circuit()

    circuit_inputs = []
    circuit_outputs = []
    circuit_gates = []

    for i in range(len(code)):
        if code[i].startswith('INPUT'):
            input_wire_name = re.findall(r'\d+', code[i])
            if user_input == []:
                input_wire_value = input('please enter value for ' + input_wire_name[0] + ' : ')
            else:
                index = -1
                for line_number in user_input:
                    index += 1
                    if line_number[0] == input_wire_name[0]:
                        input_wire_value = user_input[index][1]
                        break

            circuit_inputs.append([input_wire_name[0], int(input_wire_value)])

        elif code[i].startswith('OUTPUT'):
            output_wire_name = re.findall(r'\d+', code[i])
            circuit_outputs.append([output_wire_name[0], 'U'])

        else:
            gate = Gate()
            input_wires = []

            string_pattern = r'\b[A-Z]+\b'
            int_pattern = r'\d+'

            gate_type = re.findall(string_pattern, code[i])
            gate_wire_names = re.findall(int_pattern, code[i])

            gate.set_gate_type(gate_type)
            gate.set_output([gate_wire_names[0], 'U'])
            gate_wire_names.pop(0)

            for input_name in gate_wire_names:
                input_wires.append([input_name, 'U'])

            gate.set_inputs(input_wires)

            circuit_gates.append(gate)

    circuit.set_inputs(circuit_inputs)
    circuit.set_outputs(circuit_outputs)
    circuit.set_gates(circuit_gates)

    return circuit

def gate_function(gate_type, input_list):
    if gate_type == 'AND':
        return and_gate(input_list)

    if gate_type == 'NAND':
        return nand_gate(input_list)

    if gate_type == 'OR':
        return or_gate(input_list)

    if gate_type == 'NOR':
        return nor_gate(input_list)

    if gate_type == 'XOR':
        return xor_gate(input_list)

    if gate_type == 'XNOR':
        return xnor_gate(input_list)

    if gate_type == 'NOT':
        return not_gate(input_list)

    if gate_type == 'BUFFER':
        return buffer_gate(input_list)

def evaluate_circuit(circuit):
    gates = circuit.get_gates()
    inputs = circuit.get_inputs()
    
    # TODO: initializer
    updated_gates = []
    for gate in gates:
        gate_inputs = gate.get_inputs()
        for gate_input_index in range(len(gate_inputs)):
            for g_input in inputs:
                if g_input[0] == gate_inputs[gate_input_index][0]:
                    gate_inputs[gate_input_index][1] = g_input[1]
                    gate.set_inputs(gate_inputs)
        updated_gates.append(gate)

    circuit.set_gates(updated_gates)

    iterator = len(circuit.get_gates())
    for _ in range(iterator):
        for gate in gates:
            input_value_list = []
            gate_inputs = gate.get_inputs()
            gate_output = gate.get_output()
            gate_type = gate.get_gate_type()
            for gate_input in gate_inputs:
                input_value_list.append(gate_input[1])

            gate_output[1] = gate_function(gate_type[0], input_value_list)
            gate.set_output(gate_output)

        gate_outputs = []
        for gate in gates:
            gate_outputs.append(gate.get_output())

        for gate in gates:                              # TODO: makes it function
            gate_inputs = gate.get_inputs()
            for index in range(len(gate_inputs)):
                for gate_output in gate_outputs:
                    if gate_inputs[index][0] == gate_output[0]:
                        gate_inputs[index][1] = gate_output[1]
            gate.set_inputs(gate_inputs)

    circuit.set_gates(gates)

    circuit_outputs = circuit.get_outputs()
    for circuit_output_index in range(len(circuit_outputs)):
        for gate in gates:
            gate_output = gate.get_output()
            if circuit_outputs[circuit_output_index][0] == gate_output[0]:
                circuit_outputs[circuit_output_index][1] = gate_output[1]
        circuit.set_outputs(circuit_outputs)


def true_value_simulation():
    pass

def main():
    # file_name = input("Please enter the bench file name: ")
    file_name = "c17"
    code = get_file(file_name)

    # wire_names = input(bcolors.GREEN + "Please enter the wires names >> " + bcolors.PROMPT)
    # wire_values = input(bcolors.RED + "Please enter each wire value >>" + bcolors.PROMPT)

    user_input = [["1",1],["3",1],["6",1],["2",1],["7",1]]
    circuit = construct_circuit(code, user_input)

    evaluate_circuit(circuit)

    print(circuit.get_inputs())
    print("")
    for gate in circuit.get_gates():
        print(gate.get_gate_type())
        print(gate.get_inputs())
        print(gate.get_output())
        print("")

    print(circuit.get_outputs())

if __name__ == "__main__":
    main()
