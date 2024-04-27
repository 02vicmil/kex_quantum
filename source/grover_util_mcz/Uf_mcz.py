from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import MCMT

def Uf_mcz_oracle(marked: int, qubit_count: int, name = "Uf_mcz"):
    in_reg = QuantumRegister(qubit_count, "in")

    oracle = QuantumCircuit(in_reg, name=name)

    # Flip zeroes of marked item using X gates
    marked_ = marked
    for qubit_index in range(0, qubit_count):
        if marked_ & 1 == 0:
            oracle.x(in_reg[qubit_index])
        marked_ >>= 1

    # Multi-Controlled Z
    mcz = MCMT('cz', qubit_count-1, 1) 
    oracle.compose(mcz, in_reg, inplace=True)

    # Unflip the zeroes
    for qubit_index in range(0, qubit_count):
        if marked & 1 == 0:
            oracle.x(in_reg[qubit_index])
        marked >>= 1

    return oracle


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    NUM_QUBITS = 5
    qc = QuantumCircuit(NUM_QUBITS)

    marked_element = 12 # = 0b01100. Must be less than 2**NUM_QUBITS
    oracle = Uf_mcz_oracle(marked_element, NUM_QUBITS)
    oracle.draw("mpl")

    qc.append(oracle, qc.qubits)
    qc.draw("mpl")

    plt.show()