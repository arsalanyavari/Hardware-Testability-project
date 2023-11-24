from re import findall
from gates import *
from ansii_colors import bcolors


class Circuit:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.gates = []
        self.input_faults = []
        self.output_faults = []
        self.nets = []

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

    def set_input_faults(self, _input_faults):
        self.input_faults = _input_faults

    def get_input_faults(self):
        return self.input_faults

    def set_output_faults(self, _output_faults):
        self.output_faults = _output_faults

    def get_output_faults(self):
        return self.output_faults

    def set_nets(self, _nets):
        self.nets = _nets

    def get_nets(self):
        return self.nets


class Gate:
    def __init__(self):
        self.gate_inputs = []
        self.gate_output = {}
        self.gate_type = ''
        self.gate_input_faults = []
        self.gate_output_faults = []

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

    def set_gate_input_faults(self, _gate_input_faults):
        self.gate_input_faults = _gate_input_faults

    def get_gate_input_faults(self):
        return self.gate_input_faults

    def set_gate_output_faults(self, _gate_output_faults):
        self.gate_output_faults = _gate_output_faults

    def get_gate_output_faults(self):
        return self.gate_output_faults


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
    circuit_input_faults = []
    circuit_outputs = []
    circuit_output_faults = []
    circuit_gates = []

    for i in range(len(code)):
        if code[i].startswith('INPUT'):
            input_wire_name = findall(r'\d+', code[i])
            if user_input == []:
                input_wire_value = input('please enter value for ' + input_wire_name[0] + ' : ')
            else:
                index = -1
                for line_number in user_input:
                    index += 1
                    if line_number[0] == input_wire_name[0]:
                        input_wire_value = user_input[index][1]
                        break

            if input_wire_value != 'Z' and input_wire_value != 'U':
                input_wire_value = int(input_wire_value)

            circuit_inputs.append([input_wire_name[0], input_wire_value])
            circuit_input_faults.append([input_wire_name[0], []])

        elif code[i].startswith('OUTPUT'):
            output_wire_name = findall(r'\d+', code[i])
            circuit_outputs.append([output_wire_name[0], 'U'])
            circuit_output_faults.append([output_wire_name[0], []])

        else:
            gate = Gate()
            input_wires = []
            fault_wires = []

            string_pattern = r'\b[A-Z]+\b'
            int_pattern = r'\d+'

            gate_type = findall(string_pattern, code[i])
            gate_wire_names = findall(int_pattern, code[i])

            gate.set_gate_type(gate_type)
            gate.set_output([gate_wire_names[0], 'U'])
            gate.set_gate_output_faults([gate_wire_names[0], []])
            gate_wire_names.pop(0)

            for input_name in gate_wire_names:
                input_wires.append([input_name, 'U'])

            for input_fault_name in gate_wire_names:
                fault_wires.append([input_fault_name, []])

            gate.set_inputs(input_wires)
            gate.set_gate_input_faults(fault_wires)

            circuit_gates.append(gate)

    circuit.set_inputs(circuit_inputs)
    circuit.set_input_faults(circuit_input_faults)
    circuit.set_outputs(circuit_outputs)
    circuit.set_output_faults(circuit_output_faults)
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

        for gate in gates:
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

    return circuit


def true_value_simulation(bench_file_name = 'c17', input_file_name = 'input'):
    code = get_file(bench_file_name)

    with open(input_file_name, 'r') as f:
        lines = f.readlines()
    line1 = lines[0].split()
    line2 = lines[1].split()
    user_input = [[line1[i], int(line2[i])] for i in range(len(line1))]
    
    circuit = construct_circuit(code, user_input)
    circuit = evaluate_circuit(circuit)

    return circuit

if __name__ == "__main__":
    circuit = true_value_simulation()
    print(bcolors.RED + circuit.get_outputs() + bcolors.RESET)
