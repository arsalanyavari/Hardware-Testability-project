import copy


def resolve_gate_output_faults(gates):
    for gate in gates:
        gate_type = gate.get_gate_type()[0]
        if gate_type == "NAND" or "AND":
            output_fault_list = []
            l_list = []
            s_list = []
            gate_inputs = gate.get_inputs()
            gate_input_faults = gate.get_gate_input_faults()

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
                    s_i_list = [x for x in s_i_list if s_i_list.count(x) > 1]

                output_fault_list = [x for x in s_i_list if x not in l_u_list]

                if gate.get_output()[1] == 0:
                    fault = str(gate.get_output()[0]) + '-s-a-1'
                else:
                    fault = str(gate.get_output()[0]) + '-s-a-0'

                output_fault_list.append(fault)

            on_hand = gate.get_gate_output_faults()
            on_hand[1] = output_fault_list
            gate.set_gate_output_faults(on_hand)

        if gate_type == "OR" or "NOR":
            pass

        if gate_type == "XOR" or "XNOR":
            pass

        if gate_type == "NOT" or "BUFFER":
            pass


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
        circuit.set_outputs(circuit_output_faults)


def resolve_first_layer_gate_faults(initial_input_faults, gates, fan_outs):
    for initial_input_fault in initial_input_faults:
        _a = 1
        for gate in gates:
            g_input_faults = gate.get_gate_input_faults()
            for index in range(len(g_input_faults)):
                if g_input_faults[index][0] not in fan_outs:
                    if g_input_faults[index][0] == initial_input_fault[0]:
                        g_input_faults[index][1] = initial_input_fault[1]
                elif g_input_faults[index][0] in fan_outs:
                    if g_input_faults[index][0] == initial_input_fault[0]:
                        g_input_faults[index][0] = g_input_faults[index][0] + '_' + str(_a)
                        g_input_faults[index][1] = initial_input_fault[1]
                        _a += 1
            if _a == 3:
                _a = 0
                gate.set_gate_input_faults(g_input_faults)

    for gate in gates:
        input_faults = copy.deepcopy(gate.get_gate_input_faults())
        for index in range(len(input_faults)):
            if '_' in input_faults[index][0]:
                new_sa = input_faults[index][0] + input_faults[index][1][0][-6:]
                input_faults[index][1].append(new_sa)

        gate.set_gate_input_faults(input_faults)


def resolve_mid_circuit_input_faults(gate_output_faults, gates, fan_outs):
    for gate_output_fault in gate_output_faults:
        _a = 1
        for gate in gates:
            g_input_faults = gate.get_gate_input_faults()
            for index in range(len(g_input_faults)):
                if g_input_faults[index][0] not in fan_outs:
                    if g_input_faults[index][0] == gate_output_fault[0]:
                        g_input_faults[index][1] = gate_output_fault[1]
                elif g_input_faults[index][0] in fan_outs:
                    if g_input_faults[index][0] == gate_output_fault[0]:
                        g_input_faults[index][0] = g_input_faults[index][0] + '_' + str(_a)
                        g_input_faults[index][1] = gate_output_fault[1]
                        _a += 1
            if _a == 3:
                _a = 0
                gate.set_gate_input_faults(g_input_faults)

    for gate in gates:
        input_faults = copy.deepcopy(gate.get_gate_input_faults())
        for index in range(len(input_faults)):
            if '_' in input_faults[index][0]:
                new_sa = input_faults[index][0] + input_faults[index][1][-1][-6:]
                if new_sa != input_faults[index][1][-1]:
                    input_faults[index][1].append(new_sa)

        gate.set_gate_input_faults(input_faults)

    for gate in gates:
        gate_input_faults = gate.get_gate_input_faults()
        for index in range(len(gate_input_faults)):
            for gate_output_fault in gate_output_faults:
                if gate_input_faults[index][0] == gate_output_fault[0]:
                    gate_input_faults[index][1] = gate_output_fault[1]
        gate.set_gate_input_faults(gate_input_faults)


def get_fanout_names(gates):
    all_gate_input_names = []
    for gate in gates:
        inputs = gate.get_inputs()
        for g_input in inputs:
            all_gate_input_names.append(g_input[0])
    fan_outs = [x for x in all_gate_input_names if all_gate_input_names.count(x) > 1]
    return fan_outs


def deductive_fault_simulation(circuit):
    initial_input_faults = circuit.get_input_faults()
    gates = circuit.get_gates()

    resolve_circuit_input_faults(initial_input_faults, circuit)

    fan_outs = get_fanout_names(gates)

    resolve_first_layer_gate_faults(initial_input_faults, gates, fan_outs)

    for _ in range(len(gates)):

        resolve_gate_output_faults(gates)

        gate_output_faults = []
        for gate in gates:
            gate_output_faults.append(gate.get_gate_output_faults())

        resolve_mid_circuit_input_faults(gate_output_faults, gates, fan_outs)

    for gate in gates:
        print(gate.get_gate_input_faults())
        print(gate.get_gate_output_faults())
        print('')

    resolve_circuit_output_faults(circuit, gates)


class Net:
    def __init__(self):
        self.value = -1
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
