import qiskit


def example_one():
    oracle = qiskit.QuantumCircuit(2)
    return oracle

def example_two():
    oracle = qiskit.QuantumCircuit(2)
    oracle.cnot(0, 1)
    return oracle

def example_three():
    oracle = qiskit.QuantumCircuit(2)
    oracle.reset(0)
    return oracle

def example_four():
    oracle = qiskit.QuantumCircuit(2)
    oracle.reset(0)
    oracle.x(0)
    return oracle

def example_five():
    oracle = qiskit.QuantumCircuit(2)
    oracle.x(0)
    return oracle

def jozsa_example_one():
    oracle = qiskit.QuantumCircuit(4)
    oracle.h(0)
    oracle.cnot(1, 0)
    oracle.z(2)
    oracle.h(0)
    return oracle, 3

# these return an oracle using 2 qubits
deutsch_examples = [example_one, example_two, example_three, example_four, example_five]

# these return an oracle using n qubits, as well as the integer n
deutsch_jozsa_examples = [jozsa_example_one]