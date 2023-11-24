from true_value_simulation import *
from deductive_fault_simulation import *


def main():

    bench_file_name = input(bcolors.GREEN + "Please enter the bench file name: " + bcolors.YELLOW)
    circuit = true_value_simulation(bench_file_name)

    deductive_fault_simulation(circuit)


if __name__ == "__main__":
    main()
