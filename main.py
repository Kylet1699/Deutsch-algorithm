import qiskit
import matplotlib.pyplot as plt

# Deutsch algorithm for a single qubit
# Takes in an Oracle (QuantumCircuit) with 2 qubits
def deutsch(oracle):
    program = qiskit.QuantumCircuit(2, 1)  # 2 qubits, 1 bit
    program.x(1)  # Prepare qubit 2 into state |1>

    program.h(0)  # Hadamard all qubits
    program.h(1)

    program.barrier() # Making it look better, idea from https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html

    program.compose(oracle, inplace=True)

    program.barrier()

    program.h(0)  # Hadamard the first part
    program.measure(0, 0)  # Measure the first part (0) into the only classical register (0)
    return program


# Defining an Oracle
oracle = qiskit.QuantumCircuit(2)       # 2 qubits, 0 bits
oracle.cnot(0,1)

# Adding the oracle to the deutsch algorithm
program = deutsch(oracle)

# Visualizing the circuit
program.draw(output='mpl')
plt.show()

# Running the circuit, getting the results
job = qiskit.execute( program, qiskit.BasicAer.get_backend('qasm_simulator'))
print( job.result().get_counts() )