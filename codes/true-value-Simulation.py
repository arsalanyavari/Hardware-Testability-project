import re
from gates import *

def build_circuit(file_path):
    circuit = {'inputs': [], 'outputs': [], 'gates': []}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#') or not line:
                continue  # Skip comments and empty lines
            
            tokens = line.split()
            # print(tokens)


            if re.match(r'^INPUT\((\d+)\)$', tokens[0]):
                input_value = int(tokens[0][6:-1])
                circuit['inputs'].append({input_value: "NAN"})

            elif re.match(r'^OUTPUT\(\d+\)$', tokens[0]):
                output_value = int(tokens[0][7:-1])
                circuit['outputs'].append({output_value: "NAN"})

            # TODO: fanout not handled!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # for past_gates in circuit['gates']:
            #     if gate_input[0] in past_gates["input"]:
            #         fanout_gate = {}
            #     if gate_input[1] in past_gates["input"]:
            #         pass
                
            else: 
                pattern = r"\b(?:AND|OR|NAND|NOR|XOR|XNOR|NOT|BUFFER)\((\d+)"
                input1 = re.match(pattern, tokens[2]).group(1)
                input1 = {input1: "NAN"}
                input2 = tokens[3][0:-1]
                input2 = {input2: "NAN"}

                gate_input = [input1, input2]
                gate_output = {tokens[0]: "NAN"}
                pattern = r'^.*?\('
                on_hand = re.match(pattern, tokens[2])
                gate_type = on_hand.group()[:-1]
                gate = {"input": gate_input, "output": gate_output, "type": gate_type}
                circuit['gates'].append(gate)

    return circuit

def circuit_initializer(gate_values, circuit):
    for i in gate_values:
        for item in circuit["inputs"]:
            if list(i.keys())[0] == list(item.keys())[0]:
                item[list(i.keys())[0]] = i[list(i.keys())[0]]
        for item in circuit["gates"]:
            for input_item in item["input"]:
                if i == list(input_item.keys())[0]:
                    input_item[list(i.keys())[0]] = i[list(i.keys())[0]]
            # for output_item in item["output"]:
            #     pass  

def main():
    # user_input = input("Please enter the bench file name: ")
    user_input = "c17"
    circuit = build_circuit("../bench files/" + user_input + ".bench")
    
    print(circuit)
    print("\n")
    
    # TODO handle inputs :D

    # gate_index = input("Please enter the gate indexes")
    # gate_values = input("Please enter the gate values")
    gate_values = [{1:1}, {3:0}, {6:1}, {2:0}, {7:0}]

    circuit_initializer(gate_values, circuit)

    print(circuit)


if __name__ == "__main__":
    main()
