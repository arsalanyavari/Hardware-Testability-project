from gates import *

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


def true_value_simulation(circuit):
    circuit = evaluate_circuit(circuit)
    return circuit
