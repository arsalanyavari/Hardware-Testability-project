from true_value_simulation import *
from deductive_fault_simulation import *


def main():
    circuit = true_value_simulation()

    deductive_fault_simulation(circuit)


if __name__ == "__main__":
    main()
