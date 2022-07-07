import qiskit
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Deutsch algorithm for a single qubit
# Takes in an Oracle (QuantumCircuit) with 2 qubits
import example_oracles


def deutsch(oracle):
    program = qiskit.QuantumCircuit(2, 1)  # 2 qubits, 1 bit

    # Step 1, Apply Pauli-X gate to second qubit. |0> -> |1>
    program.x(1)

    # Step 2, Apply Hadamard gate to each qubit
    program.h(0)
    program.h(1)

    program.barrier() # Making it look better, idea from https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html

    # Step 3, Apply Oracle function
    program.compose(oracle, inplace=True)

    program.barrier()

    # Step 4, Apply Hadamard gate for interference
    program.h(0)
    program.measure(0, 0)
    return program

# Deutsch algorithm for n qubits
# Takes in an Oracle (QuantumCircuit) with n+1 qubits, and the integer n
def deutsch_jozsa(oracle, n):
    program = qiskit.QuantumCircuit(n+1, n)  # n+1 qubits, n bits

    # Step 1, prepare last qubit into state |1>
    program.x(n)

    # Step 2, Apply Hadamard gate to each qubit
    for i in range(n+1):
        program.h(i)

    # Step 3, Apply Oracle function
    program.barrier()
    program.compose(oracle, inplace=True)
    program.barrier()

    # Step 4, Apply Hadamard gate for interference
    for i in range(n):
        program.h(i)

    program.measure(range(n), range(n))
    return program


print("Running Deutsch Examples")
for example in example_oracles.deutsch_examples:
    oracle = example()
    program = deutsch(oracle)
    job = qiskit.execute(program, qiskit.BasicAer.get_backend('qasm_simulator'))
    result = job.result()
    print(result.get_counts())
    program.draw(output='mpl', filename='Deutsch_Imgs/'+example.__name__)
    plot_histogram(result.get_counts(), filename='Deutsch_Imgs/'+example.__name__+'_histogram')

print("Running Deutsch_Jozsa Examples")
for example in example_oracles.deutsch_jozsa_examples:
    oracle, n = example()
    program = deutsch_jozsa(oracle, n)
    job = qiskit.execute(program, qiskit.BasicAer.get_backend('qasm_simulator'))
    result = job.result()
    print(result.get_counts())
    program.draw(output='mpl', filename='Deutsch_Jozsa_Imgs/'+example.__name__)
    plot_histogram(result.get_counts(), filename='Deutsch_Jozsa_Imgs/'+example.__name__+'_histogram')


