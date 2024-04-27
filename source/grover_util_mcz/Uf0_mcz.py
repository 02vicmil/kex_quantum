from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import MCMT

def Uf0_mcz_oracle(qubit_count: int, name = "Uf0_mcz"):
    in_reg = QuantumRegister(qubit_count, "in")

    oracle = QuantumCircuit(in_reg, name = name)
    oracle.x(in_reg)

    # Flip phase
    oracle.z(0)

    # Multi-Controlled Z. (Since all input is flipped using X, the phase will
    # flip only when all input is zero unmaking the phase-flip from the Z above)
    mcz = MCMT('cz', qubit_count-1, 1) 
    oracle.compose(mcz, in_reg, inplace=True)

    oracle.x(in_reg)
    return oracle

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    NUM_QUBITS = 5
    qc = QuantumCircuit(NUM_QUBITS)

    oracle = Uf0_mcz_oracle(NUM_QUBITS)
    oracle.draw("mpl")

    qc.append(oracle, qc.qubits)
    qc.draw("mpl")

    plt.show()