import re

def build_circuit(file_path):
    circuit = {'inputs': {}, 'outputs': {}, 'gates': {}}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#') or not line:
                continue  # Skip comments and empty lines
            
            tokens = line.split()
            print(tokens)


            if re.match(r'^INPUT\((\d+)\)$', tokens[0]):
                input_id = int(tokens[0][6:-1])
                circuit['inputs'][input_id] = len(circuit['inputs']) + 1 

            if re.match(r'^OUTPUT\(\d+\)$', tokens[0]):
                output_id = int(tokens[0][7:-1])
                circuit['outputs'][len(circuit['outputs']) + 1] = output_id

            # TODO: not complete

    return circuit

def main():
    # TODO get file name from the input
    circuit = build_circuit("../bench files/c17.bench")
    
    print("\n------------------------------\nInputs:")
    input_ids = list(circuit['inputs'].keys())
    print(', '.join(map(str, input_ids)))

    print("\nOutputs:")
    output_ids = list(circuit['outputs'].keys())
    output_gate_ids = list(circuit['outputs'].values())
    print(', '.join(map(str, output_gate_ids)))

    print("\nGates:")
    for gate_id, gate_info in circuit['gates'].items():
        gate_type = gate_info['type']
        inputs = gate_info['inputs']
        input_names = [f"Input {input_id}" if input_id in circuit['inputs'] else f"Gate {input_id}" for input_id in inputs]
        print(f"Gate {gate_id} ({gate_type}): Inputs {', '.join(input_names)}")
        

    print("\n\n", circuit)
if __name__ == "__main__":
    main()
