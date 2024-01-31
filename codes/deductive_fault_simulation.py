import copy


def remove_duplicates(input_list):
    seen = set()
    result = []

    for item in input_list:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


def propagate_input_to_output(gates):
    for gate in gates:
        gate_input_faults = gate.get_gate_input_faults()
        gate_type = gate.get_gate_type()[0]
        gate_inputs = gate.get_inputs()
        output_fault_list = []
        l_list = []
        s_list = []

        if gate_type == "NAND" or gate_type == "AND":
            for gate_input in gate_inputs:
                if gate_input[1] == 0:
                    s_list.append(gate_input[0])
                elif gate_input[1] == 1:
                    l_list.append(gate_input[0])

            if not s_list:
                for gate_input_fault in gate_input_faults:
                    faults = gate_input_fault[1]
                    for fault in faults:
                        output_fault_list.append(fault)

                if gate_type == 'NAND' and gate.get_output()[1] == 0:
                    fault = str(gate.get_output()[0]) + '-s-a-1'
                else:
                    fault = str(gate.get_output()[0]) + '-s-a-0'

                output_fault_list.append(fault)

            else:
                s_i_list = []
                l_u_list = []
                for gate_input_fault in gate_input_faults:
                    if '_' in gate_input_fault[0]:
                        if gate_input_fault[0][:-2] in s_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                s_i_list.append(fault)
                        elif gate_input_fault[0][:-2] in l_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                l_u_list.append(fault)
                    else:
                        if gate_input_fault[0] in s_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                s_i_list.append(fault)
                        elif gate_input_fault[0] in l_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                l_u_list.append(fault)

                if len(s_list) > 1:
                    s_i_list = [x for x in s_i_list if s_i_list.count(x) == len(s_list)]
                output_fault_list = [x for x in s_i_list if x not in l_u_list]

                if gate.get_output()[1] == 0:
                    fault = str(gate.get_output()[0]) + '-s-a-1'
                else:
                    fault = str(gate.get_output()[0]) + '-s-a-0'

                output_fault_list.append(fault)

            on_hand = gate.get_gate_output_faults()
            on_hand[1] = remove_duplicates(output_fault_list)
            gate.set_gate_output_faults(on_hand)

        if gate_type == "OR" or gate_type == "NOR":
            for gate_input in gate_inputs:
                if gate_input[1] == 1:
                    s_list.append(gate_input[0])
                elif gate_input[1] == 0:
                    l_list.append(gate_input[0])

            if not s_list:
                for gate_input_fault in gate_input_faults:
                    faults = gate_input_fault[1]
                    for fault in faults:
                        output_fault_list.append(fault)

                if gate_type == 'NOR' and gate.get_output()[1] == 1:
                    fault = str(gate.get_output()[0]) + '-s-a-0'
                else:
                    fault = str(gate.get_output()[0]) + '-s-a-1'

                output_fault_list.append(fault)

            else:
                s_i_list = []
                l_u_list = []
                for gate_input_fault in gate_input_faults:
                    if '_' in gate_input_fault[0]:
                        if gate_input_fault[0][:-2] in s_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                s_i_list.append(fault)
                        elif gate_input_fault[0][:-2] in l_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                l_u_list.append(fault)
                    else:
                        if gate_input_fault[0] in s_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                s_i_list.append(fault)
                        elif gate_input_fault[0] in l_list:
                            faults = gate_input_fault[1]
                            for fault in faults:
                                l_u_list.append(fault)

                if len(s_list) > 1:
                    s_i_list = [x for x in s_i_list if s_i_list.count(x) == len(s_list)]
                output_fault_list = [x for x in s_i_list if x not in l_u_list]

                if gate_type == 'NOR' and gate.get_output()[1] == 1:
                    fault = str(gate.get_output()[0]) + '-s-a-0'
                else:
                    fault = str(gate.get_output()[0]) + '-s-a-1'

                output_fault_list.append(fault)

            on_hand = gate.get_gate_output_faults()
            on_hand[1] = remove_duplicates(output_fault_list)
            gate.set_gate_output_faults(on_hand)

        if gate_type == "XOR" or gate_type == "XNOR":
            faults = []
            for gate_input_fault in gate_input_faults:
                for gif in gate_input_fault[1]:
                    faults.append(gif)

            output_fault_list = [x for x in faults if faults.count(x) % 2 == 1]

            if gate.get_output()[1] == 0:
                fault = str(gate.get_output()[0]) + '-s-a-1'
            else:
                fault = str(gate.get_output()[0]) + '-s-a-0'

            output_fault_list.append(fault)

            on_hand = gate.get_gate_output_faults()
            on_hand[1] = remove_duplicates(output_fault_list)
            gate.set_gate_output_faults(on_hand)


        if gate_type == "NOT" or gate_type == "BUFFER":
            for gate_input_fault in gate_input_faults:
                faults = gate_input_fault[1]
                for fault in faults:
                    output_fault_list.append(fault)

            if gate.get_output()[1] == 0:
                fault = str(gate.get_output()[0]) + '-s-a-1'
            else:
                fault = str(gate.get_output()[0]) + '-s-a-0'

            output_fault_list.append(fault)

            on_hand = gate.get_gate_output_faults()
            on_hand[1] = remove_duplicates(output_fault_list)
            gate.set_gate_output_faults(on_hand)

    return gates


def resolve_circuit_input_faults(initial_input_faults, circuit):
    initial_inputs = circuit.get_inputs()
    for index in range(len(initial_input_faults)):
        for initial_input in initial_inputs:
            if initial_input[0] == initial_input_faults[index][0]:
                if initial_input[1] == 0:
                    initial_input_faults[index][1] = [str(initial_input[0]) + '-s-a-1']
                else:
                    initial_input_faults[index][1] = [str(initial_input[0]) + '-s-a-0']
        circuit.set_input_faults(initial_input_faults)


def resolve_circuit_output_faults(circuit, gates):
    circuit.set_gates(gates)
    circuit_output_faults = circuit.get_output_faults()

    for circuit_output_fault_index in range(len(circuit_output_faults)):
        for gate in gates:
            gate_output_fault = gate.get_gate_output_faults()
            if circuit_output_faults[circuit_output_fault_index][0] == gate_output_fault[0]:
                circuit_output_faults[circuit_output_fault_index][1] = gate_output_fault[1]
        circuit.set_output_faults(circuit_output_faults)


def initiate_first_layer_faults(initial_input_faults, gates, fan_outs, circuit):
    resolved_gates = []
    for gate in gates:
        g_input_faults = gate.get_gate_input_faults()
        delete = True
        for initial_input_fault in initial_input_faults:
            for index in range(len(g_input_faults)):
                if g_input_faults[index][0] == initial_input_fault[0]:
                    g_input_faults[index][1] = initial_input_fault[1]
        gate.set_gate_input_faults(g_input_faults)

        for g_input_fault in g_input_faults:
            if not g_input_fault[1]:
                delete = False

        if delete:
            resolved_gates.append(gate)
    gates_to_remove = set(resolved_gates)
    gates = [x for x in gates if x not in gates_to_remove]

    for fan_out in fan_outs:
        _a = 1
        for gate in resolved_gates:
            g_input_faults = gate.get_gate_input_faults()
            for index in range(len(g_input_faults)):
                if g_input_faults[index][0] == fan_out:
                    g_input_faults[index][0] = g_input_faults[index][0] + '_' + str(_a)
                    _a += 1
            gate.set_gate_input_faults(g_input_faults)

    for gate in resolved_gates:
        input_faults = copy.deepcopy(gate.get_gate_input_faults())
        for index in range(len(input_faults)):
            if '_' in input_faults[index][0]:
                new_sa = input_faults[index][0] + input_faults[index][1][-1][-6:]
                if new_sa not in input_faults[index][1]:
                    input_faults[index][1].append(new_sa)
        gate.set_gate_input_faults(input_faults)

    resolved_gates = propagate_input_to_output(resolved_gates)

    for resolved_gate in resolved_gates:
        circuit_output_faults = circuit.get_output_faults()
        resolved_gate_output_faults = resolved_gate.get_gate_output_faults()

        for index in range(len(circuit_output_faults)):
            if circuit_output_faults[index][0] == resolved_gate_output_faults[0]:
                circuit_output_faults[index][1] = resolved_gate_output_faults[1]
            circuit.set_output_faults(circuit_output_faults)

        for gate in gates:
            gate_input_faults = gate.get_gate_input_faults()
            for index in range(len(gate_input_faults)):
                if gate_input_faults[index][0] == resolved_gate_output_faults[0]:
                    gate_input_faults[index][1] = resolved_gate_output_faults[1]
            gate.set_gate_input_faults(gate_input_faults)

    return gates


def propagate_mid_circuit_faults(gates, fan_outs):
    this_step_gates = []
    for gate in gates:
        extra = False
        inputs = gate.get_gate_input_faults()
        for g_input in inputs:
            if not g_input[1]:
                extra = True

        if not extra:
            this_step_gates.append(gate)

    gates_to_remove = set(this_step_gates)
    gates = [x for x in gates if x not in gates_to_remove]

    for fan_out in fan_outs:
        _a = 1
        for gate in this_step_gates:
            g_input_faults = gate.get_gate_input_faults()
            for index in range(len(g_input_faults)):
                if g_input_faults[index][0] == fan_out:
                    g_input_faults[index][0] = g_input_faults[index][0] + '_' + str(_a)
                    _a += 1
            gate.set_gate_input_faults(g_input_faults)

    for gate in this_step_gates:
        input_faults = copy.deepcopy(gate.get_gate_input_faults())
        for index in range(len(input_faults)):
            if '_' in input_faults[index][0]:
                new_sa = input_faults[index][0] + input_faults[index][1][-1][-6:]
                if new_sa not in input_faults[index][1]:
                    input_faults[index][1].append(new_sa)
        gate.set_gate_input_faults(input_faults)

    this_step_gates = propagate_input_to_output(this_step_gates)

    for this_step_gate in this_step_gates:
        resolved_this_step_gate_output_faults = this_step_gate.get_gate_output_faults()
        if not gates:
            return this_step_gates
        else:
            for gate in gates:
                gate_input_faults = gate.get_gate_input_faults()
                for index in range(len(gate_input_faults)):
                    if gate_input_faults[index][0] == resolved_this_step_gate_output_faults[0]:
                        gate_input_faults[index][1] = resolved_this_step_gate_output_faults[1]
                gate.set_gate_input_faults(gate_input_faults)

    return gates


def get_fanout_names(gates):
    all_gate_input_names = []
    for gate in gates:
        inputs = gate.get_inputs()
        for g_input in inputs:
            all_gate_input_names.append(g_input[0])
    fan_outs = [x for x in all_gate_input_names if all_gate_input_names.count(x) > 1]
    fan_outs = list(set(fan_outs))
    return fan_outs


def deductive_fault_simulation(circuit):
    initial_input_faults = circuit.get_input_faults()
    gates = circuit.get_gates()

    resolve_circuit_input_faults(initial_input_faults, circuit)

    fan_outs = get_fanout_names(gates)

    gates = initiate_first_layer_faults(initial_input_faults, gates, fan_outs, circuit)

    gates = propagate_mid_circuit_faults(gates, fan_outs)

    for _ in range(circuit.get_depth() * 5):
        gates = propagate_mid_circuit_faults(gates, fan_outs)

    resolve_circuit_output_faults(circuit, gates)

    return circuit

def print_deductive_fault(circuit):
    gates = circuit.get_gates()
    for gate in gates:
        print(gate.get_gate_input_faults())
        print(gate.get_gate_output_faults())
        print('')


if __name__ == "__main__":
    pass
