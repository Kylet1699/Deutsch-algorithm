# Sample Hello World code, works in PyCharm on a Conda environment with Python 3.10 and Qiskit installed
# Unsure if it works with other environments

import qiskit

qr = qiskit.QuantumRegister(2)
cr = qiskit.ClassicalRegister(2)
program = qiskit.QuantumCircuit(qr, cr)

program.h(1)
program.measure(qr,cr)

print(program)

job = qiskit.execute( program, qiskit.BasicAer.get_backend('qasm_simulator'))
print( job.result().get_counts() )