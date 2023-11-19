import re


class Circuit:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.gates = []

    def set_inputs(self, _inputs): self.inputs = _inputs

    def get_inputs(self): return self.inputs

    def set_outputs(self, _outputs): self.outputs = _outputs

    def get_outputs(self): return self.outputs

    def set_gates(self, _gates): self.gates = _gates

    def get_gates(self): return self.gates


class Gate:
    def __init__(self):
        self.gate_inputs = []
        self.gate_output = {}
        self.gate_type = ''

    def set_inputs(self, _inputs): self.gate_inputs = _inputs

    def get_inputs(self): return self.gate_inputs

    def set_output(self, _output): self.gate_output = _output

    def get_output(self): return self.gate_output

    def set_gate_type(self, _gate_type): self.gate_type = _gate_type

    def get_gate_type(self): return self.gate_type


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


def construct_circuit(code):
    circuit = Circuit()

    circuit_inputs = []
    circuit_outputs = []
    circuit_gates = []

    for i in range(len(code)):
        if code[i].startswith('INPUT'):
            input_wire_name = re.findall(r'\d+', code[i])
            input_wire_value = input('please enter value for ' + input_wire_name[0] + ' : ')
            # todo : unaccepted values not handled
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


def gate_function(gate_type, input_0_1_count):
    if gate_type == 'AND':
        if input_0_1_count[0] > 0:
            return 0
        else:
            return 1

    if gate_type == 'NAND':
        if input_0_1_count[1] > 0:
            return 0
        else:
            return 1

    if gate_type == 'OR':
        if input_0_1_count[1] > 0:
            return 1
        else:
            return 0

    if gate_type == 'NOR':
        if input_0_1_count[1] > 0:
            return 0
        else:
            return 1

    if gate_type == 'XOR':
        if input_0_1_count[1] % 2 == 1:
            return 1
        elif input_0_1_count[1] % 2 == 0:
            return 0

    if gate_type == 'XNOR':
        if input_0_1_count[1] % 2 == 0:
            return 1
        elif input_0_1_count[1] % 2 == 1:
            return 0

    if gate_type == 'NOT':
        if input_0_1_count[0] > 0:
            return 1
        elif input_0_1_count[1] > 0:
            return 0

    if gate_type == 'BUFFER':
        if input_0_1_count[0] > 0:
            return 0
        elif input_0_1_count[1] > 0:
            return 1


def evaluate_circuit(circuit):
    gates = circuit.get_gates()
    inputs = circuit.get_inputs()
    updated_gates = []

    for gate in gates:
        gate_inputs = gate.get_inputs()
        for gate_input_index in range(len(gate_inputs)):
            for input in inputs:
                if input[0] == gate_inputs[gate_input_index][0]:
                    gate_inputs[gate_input_index][1] = input[1]
                    gate.set_inputs(gate_inputs)
        updated_gates.append(gate)

    circuit.set_gates(updated_gates)

    iterator = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # todo : figure out iteration value
    for _ in iterator:
        for gate in gates:
            gate_inputs = gate.get_inputs()
            gate_0_1_input_count = [0, 0, '']
            gate_output = gate.get_output()
            gate_type = gate.get_gate_type()
            for input in gate_inputs:
                if input[1] == 'U':
                    gate_0_1_input_count[2] = 'U'
                    gate_output[1] = 'U'
                elif input[1] == 'Z':
                    gate_0_1_input_count[2] = 'Z'
                    gate_output[1] = 'Z'
                elif input[1] == 0:
                    gate_0_1_input_count[2] = ''
                    gate_0_1_input_count[0] += 1
                elif input[1] == 1:
                    gate_0_1_input_count[2] = ''
                    gate_0_1_input_count[1] += 1

            if gate_0_1_input_count[2] != 'U' and gate_0_1_input_count[2] != 'Z':
                gate_output[1] = gate_function(gate_type[0], gate_0_1_input_count)

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


def main():
    file_name = input('please enter file name : ')  # todo : unaccepted file name not handled
    code = get_file(file_name)

    circuit = construct_circuit(code)

    evaluate_circuit(circuit)

    print(circuit.get_outputs())


main()
