import qiskit
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# for running it on IBM's computers
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit import assemble, transpile

# Deutsch's algorithm for a single qubit
# Takes in an Oracle (QuantumCircuit) with 2 qubits
import example_oracles

# Deutsch's algorithm as defined in the lecture slides, Weeks 5-6
# Takes in an oracle quantum circuit and outputs a Deutsch's Algorithm circuit
def deutsch(oracle):
    program = qiskit.QuantumCircuit(2, 1)  # 2 qubits, 1 bit

    # Step 1, Apply Pauli-X gate to second qubit. |0> -> |1>
    program.x(1)

    # Step 2, Apply Hadamard gate to each qubit
    program.h(0)
    program.h(1)

    # Making it look better, idea from https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html
    program.barrier()

    # Step 3, Apply Oracle function
    program.compose(oracle, inplace=True)

    program.barrier()

    # Step 4, Apply Hadamard gate for interference
    program.h(0)
    program.measure(0, 0)
    return program

# Deutsch_Jozsa's algorithm for n qubits
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


# Code snipit from Qiskit tutorial: https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html
# It finds a backend that has enough qubits, is not a simulator, and is operational
# It then transpiles the circuit, optimizes it, runs it, monitors the job, and receives the results
def run_on_IBM(circuit, n):
    # IBMQ.save_account("TOKEN")
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= (n+1) and
                                        not x.configuration().simulator and x.status().operational==True))
    print("least busy backend: ", backend)

    transpiled_dj_circuit = transpile(circuit, backend, optimization_level=3)
    job = backend.run(transpiled_dj_circuit)
    job_monitor(job, interval=2)

    results = job.result()
    answer = results.get_counts()

    plot_histogram(answer, filename='IBM_Imgs/histogram2')

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


print("Running it on IBM")
# Try it on real Q-computer:
oracle = example_oracles.example_two()
circuit = deutsch(oracle)
circuit.draw(output="mpl", filename='IBM_Imgs/oracle2')
run_on_IBM(circuit, n)
