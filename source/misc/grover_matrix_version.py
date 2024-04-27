from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Operator
from math import pi, sqrt, floor
import numpy as np

def grovers_circuit(marked: int, num_qubits: int, iteration_num: int = -1) -> QuantumCircuit:
    N = 2**num_qubits

    # Set up registers and circuit
    qubits_in = QuantumRegister(num_qubits)
    classic_bit = ClassicalRegister(1)
    circuit = QuantumCircuit(qubits_in, classic_bit)
    
    # Set up the oracle Uf
    Uf_unitary = np.identity(N)
    Uf_unitary[marked, marked] = -1.0
    Uf = Operator(Uf_unitary)

    # Set up the (diffuser) oracle Uf0
    Uf0_unitary = np.identity(N)
    Uf0_unitary[0, 0] = -1.0
    Uf0 = Operator(Uf0_unitary)

    # Grover's Algorithm

    circuit.h(qubits_in)

    if iteration_num < 0:
        # Optimal iteration number is ≈ π√(N)/4, N = 2**num_qubits
        iteration_num = floor(sqrt(2**num_qubits)*pi/4.0)

    for _ in range(iteration_num):
        # Apply Phase Oracle
        circuit.unitary(Uf, qubits_in)

        # Apply Diffusor/Mean Inversion
        circuit.h(qubits_in)
        circuit.unitary(Uf0, qubits_in)
        circuit.h(qubits_in)

    circuit.measure_all()

    return circuit


if __name__ == "__main__":
    from .. import Runner
    import matplotlib.pyplot as plt

    NUM_QUBITS = 5
    MARKED_ELEMENT = 14 # 14 = 0b01110... So we should measure that a lot!
    qc = grovers_circuit(MARKED_ELEMENT, NUM_QUBITS, iteration_num=1)
    qc.draw("mpl")

    Runner(qc).run(draw_transpiled_circuit=True)

    plt.show()