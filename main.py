import qiskit
import matplotlib.pyplot as plt

# Deutsch algorithm for a single qubit
# Takes in an Oracle (QuantumCircuit) with 2 qubits
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


# Defining an Oracle
oracle = qiskit.QuantumCircuit(2)       # 2 qubits, 0 bits
oracle.cnot(0,1)

# Adding the oracle to the deutsch algorithm
program = deutsch(oracle)

# Visualizing the circuit
program.draw(output='mpl', filename='deutsch.pdf')
plt.show()

# Running the circuit, getting the results
job = qiskit.execute( program, qiskit.BasicAer.get_backend('qasm_simulator'))
print( job.result().get_counts() )

oracle2 = qiskit.QuantumCircuit(4)
oracle2.h(0)
oracle2.cnot(1,0)
oracle2.z(2)
oracle2.h(0)

program2= deutsch_jozsa(oracle2, 3)

program2.draw(output='mpl', filename='deutsch_jozsa.pdf')
plt.show()

job2 = qiskit.execute( program2, qiskit.BasicAer.get_backend('qasm_simulator'))
print( job2.result().get_counts() )



