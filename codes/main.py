from os import listdir, path
from pick import pick
from construct_circuit import construct_circuit
from true_value_simulation import true_value_simulation
from deductive_fault_simulation import deductive_fault_simulation
from exhaustive_simulation import exhaustive_simulation

def list_files_in_directory(directory):
    file_list = [filename for filename in listdir(directory) if path.isfile(path.join(directory, filename))]
    return file_list

def get_file(file_name):
    file_path = "../bench files/" + file_name
    code = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('#') or not line:
                continue
            code.append(line)
    return code

def main():
    title = 'Please choose the appropriate phase: '
    options = ['Phase1', 'Phase2']
    _ , phase = pick(options, title, indicator='=> ')

    title = 'Please choose the appropriate bench file: '
    options = list_files_in_directory("../bench files")
    bench_file_name , _ = pick(options, title, indicator='=> ')
    # bench_file_name = input(bcolors.GREEN + "Please enter the bench file name: " + bcolors.YELLOW)

    bench_code = get_file(bench_file_name)
    
    if phase == 0:
        with open("input", 'r') as f:
            lines = f.readlines()
        line1 = lines[0].split()
        line2 = lines[1].split()
        user_input = [[line1[i], int(line2[i])] for i in range(len(line1))]        
        circuit = construct_circuit(bench_code, user_input)
        circuit = true_value_simulation(circuit)
        circuit = deductive_fault_simulation(circuit)
        gates = circuit.get_gates()
        for gate in gates:
            print(gate.get_gate_input_faults())
            print(gate.get_gate_output_faults())
            print('')
    elif phase == 1:
        circuit = construct_circuit(bench_code)
        exhaustive_list = exhaustive_simulation(circuit)
        pass #TODO:)

    else:
        print("Please run it again in correct format!")

if __name__ == "__main__":
    main()
