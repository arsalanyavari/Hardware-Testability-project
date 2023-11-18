import re
from gates import *

class Circuit:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.gates = []
    def append_input(self, _input):
        self.inputs.append(_input)
    def append_output(self, _output):
        self.outputs.append(_output)        
    def set_gate(self, _gate):
        self.gates.append(_gate)
    def get_input(self):
        return self.inputs
    def get_output(self):
        return self.outputs
    def get_gate(self):
        return self.gates
class Gate:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.type = ''
    def append_input(self, _input):
        self.inputs.append(_input)
    def append_output(self, _output):
        self.outputs.append(_output)
    def set_type(self, _type):
        self.type = _type
    def get_input (self):
        return self.inputs
    def set_output (self, _output):
         self.outputs[0] = _output
    def get_output (self):
        return self.outputs
    def get_type (self):
        return self.type

def build_circuit(file_path):
    # circuit = {'inputs': [], 'outputs': [], 'gates': []}
    circuit = Circuit()

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            
            if line.startswith('#') or not line:
                continue  # Skip comments and empty lines
            tokens = line.split()

            if re.match(r'^INPUT\((\d+)\)$', tokens[0]):
                input_value = int(tokens[0][6:-1])
                circuit.append_input({input_value: 'U'})

            elif re.match(r'^OUTPUT\(\d+\)$', tokens[0]):
                output_value = int(tokens[0][7:-1])
                circuit.append_output({output_value: 'U'})

            # TODO: fanout not handled!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # for past_gates in circuit['gates']:
            #     if gate_input[0] in past_gates["input"]:
            #         fanout_gate = {}
            #     if gate_input[1] in past_gates["input"]:
            #         pass
                
            else: 
                pattern = r"\b(?:AND|OR|NAND|NOR|XOR|XNOR|NOT|BUFFER)\((\d+)"
                input1 = int(re.match(pattern, tokens[2]).group(1))
                input1 = {input1: 'U'}
                input2 = int(tokens[3][0:-1])
                input2 = {input2: 'U'}

                gate_output = {tokens[0]: 'U'}
                pattern = r'^.*?\('
                on_hand = re.match(pattern, tokens[2])
                gate_type = on_hand.group()[:-1]
                gate = Gate()
                gate.append_input(input1)
                gate.append_input(input2)
                gate.append_output(gate_output)
                gate.set_type(gate_type)
                circuit.set_gate(gate)

    return circuit

def update_dict(obj, value):
    obj[list(obj.keys())[0]] = value

def circuit_initializer(gate_values, circuit):
    for i in gate_values:
        for item in circuit.inputs:
            if i[0] == list(item.keys())[0]:
                update_dict(item, i[1])
                
        for gate in circuit.gates:
            for item in gate.inputs:
               if i[0] == list(item.keys())[0]:
                   update_dict(item, i[1])

    return circuit

# def circuit_evaluator(gates_array, circuit):
#     while len(gates_array) != 0:
#         for i in gates_array:
#             for j in i.get_input():
#                 if (j==0 or j==1):
                    

def define_gate_value(gate_type, gate_inputs):
    if gate_type == "AND":
        return and_gate(list(gate_inputs[0].values())[0], list(gate_inputs[1].values())[0])    
    if gate_type == "NAND":
        return nand_gate(list(gate_inputs[0].values())[0], list(gate_inputs[1].values())[0])
    if gate_type == "OR":
        return or_gate(list(gate_inputs[0].values())[0], list(gate_inputs[1].values())[0])
    if gate_type == "NOR":
        return nor_gate(list(gate_inputs[0].values())[0], list(gate_inputs[1].values())[0])
    if gate_type == "XOR":
        return xor_gate(list(gate_inputs[0].values())[0], list(gate_inputs[1].values())[0])
    if gate_type == "XNOR":
        return xnor_gate(list(gate_inputs[0].values())[0], list(gate_inputs[1].values())[0])
    if gate_type == "NOT":
        return not_gate(list(gate_inputs[0].values())[0])
    if gate_type == "BUFFER":
        return buffer_gate(list(gate_inputs[0].values())[0])



    # return gate_output

def circuit_evaluator(circuit):
    for _ in range(len(circuit.get_gate())):
        for gate in circuit.get_gate():
            gate_inputs = gate.get_input()
            gate_outputs = gate.get_output()
            gate_type = gate.get_type()
            output_value = define_gate_value(gate_type, gate_inputs)
            gate.set_output(output_value)

            # print(list(gate_inputs[1].values())[0])                   


def main():
    # user_input = input("Please enter the bench file name: ")
    user_input = "c17"
    circuit = build_circuit("../bench files/" + user_input + ".bench")



    # print(circuit.get_input())
    # print(circuit.get_output())
    # print(circuit.get_gate()[0].get_input())
    # print("\n")
    
    # TODO handle inputs :D

    # gate_index = input("Please enter the gate indexes")
    # gate_values = input("Please enter the gate values")
    gate_values = [(1,1), (3,0), (6,1), (2,0), (7,0)]

    circuit = circuit_initializer(gate_values, circuit)

    # print(circuit.get_input())
    # print(circuit.get_output())
    # print(circuit.get_gate()[0].get_input())
    # print("\n")

    circuit_evaluator(circuit)

if __name__ == "__main__":
    main()
